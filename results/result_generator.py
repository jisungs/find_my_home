from .matching_algorithm import match_persona, analyze_survey_answers
from .persona_data import (
    get_matching_reasons, 
    get_recommended_areas, 
    get_persona_description, 
    get_recommended_properties
)
from .models import SurveyResult, PersonaType
import json

def generate_persona_result(survey):
    """설문 결과를 바탕으로 페르소나 결과 생성"""
    # 매칭 알고리즘으로 최적 페르소나 찾기
    matching_result = match_persona(survey)
    persona_type_name = matching_result['persona_type']
    matching_score = matching_result['matching_score']
    
    # PersonaType 객체 가져오기
    try:
        persona_type = PersonaType.objects.get(name=persona_type_name)
    except PersonaType.DoesNotExist:
        # 기본 페르소나 사용
        persona_type = PersonaType.objects.first()
        persona_type_name = persona_type.name if persona_type else '해안가_라이프스타일형'
    
    # 설문 답변 분석
    answers = analyze_survey_answers(survey)
    
    # 매칭 이유 생성
    matching_reasons = get_matching_reasons(answers, persona_type_name)
    
    # 추천 지역 정보
    recommended_areas = get_recommended_areas(persona_type_name)
    
    # 페르소나 상세 설명
    persona_description = get_persona_description(persona_type_name)
    
    # 추천 매물 정보
    recommended_properties = get_recommended_properties(persona_type_name)
    
    # 레이더 차트 데이터 생성
    radar_chart_data = generate_radar_chart_data(persona_type_name, recommended_areas)
    
    # 결과 데이터 구성
    result_data = {
        'persona_type': persona_type,
        'matching_score': matching_score,
        'matching_reasons': matching_reasons,
        'persona_description': persona_description,
        'recommended_areas': recommended_areas,
        'recommended_properties': recommended_properties,
        'radar_chart_data': radar_chart_data,
        'all_scores': matching_result['all_scores']
    }
    
    return result_data

def generate_radar_chart_data(persona_type_name, recommended_areas):
    """레이더 차트용 데이터 생성"""
    if not recommended_areas:
        return {
            'labels': ['교통', '교육', '생활', '투자', '자연환경', '편의시설'],
            'datasets': [{
                'label': persona_type_name,
                'data': [50, 50, 50, 50, 50, 50],
                'backgroundColor': 'rgba(74, 144, 226, 0.2)',
                'borderColor': 'rgba(74, 144, 226, 1)',
                'borderWidth': 2
            }]
        }
    
    # 추천 지역들의 평균 점수 계산
    avg_scores = {
        'transportation': 0,
        'education': 0,
        'lifestyle': 0,
        'investment': 0,
        'nature': 0,
        'convenience': 0
    }
    
    for area in recommended_areas:
        scores = area['scores']
        for key in avg_scores:
            avg_scores[key] += scores[key]
    
    # 평균 계산
    area_count = len(recommended_areas)
    for key in avg_scores:
        avg_scores[key] = int(avg_scores[key] / area_count)
    
    # 페르소나별 색상 설정
    persona_colors = {
        '해안가_라이프스타일형': {'bg': 'rgba(74, 144, 226, 0.2)', 'border': 'rgba(74, 144, 226, 1)'},
        '도심_라이프스타일형': {'bg': 'rgba(80, 200, 120, 0.2)', 'border': 'rgba(80, 200, 120, 1)'},
        '자연친화_크리에이티브형': {'bg': 'rgba(139, 69, 19, 0.2)', 'border': 'rgba(139, 69, 19, 1)'},
        '산업도시_자연친화형': {'bg': 'rgba(255, 99, 71, 0.2)', 'border': 'rgba(255, 99, 71, 1)'},
        '항만_라이프스타일형': {'bg': 'rgba(65, 105, 225, 0.2)', 'border': 'rgba(65, 105, 225, 1)'},
        '모던_미니멀형': {'bg': 'rgba(112, 128, 144, 0.2)', 'border': 'rgba(112, 128, 144, 1)'}
    }
    
    colors = persona_colors.get(persona_type_name, persona_colors['해안가_라이프스타일형'])
    
    return {
        'labels': ['교통', '교육', '생활', '투자', '자연환경', '편의시설'],
        'datasets': [{
            'label': persona_type_name,
            'data': [
                avg_scores['transportation'],
                avg_scores['education'],
                avg_scores['lifestyle'],
                avg_scores['investment'],
                avg_scores['nature'],
                avg_scores['convenience']
            ],
            'backgroundColor': colors['bg'],
            'borderColor': colors['border'],
            'borderWidth': 2,
            'pointBackgroundColor': colors['border'],
            'pointBorderColor': '#fff',
            'pointHoverBackgroundColor': '#fff',
            'pointHoverBorderColor': colors['border']
        }]
    }

def create_survey_result(survey):
    """설문 결과를 SurveyResult 모델에 저장"""
    # 기존 결과가 있으면 삭제
    SurveyResult.objects.filter(survey=survey).delete()
    
    # 새로운 결과 생성
    result_data = generate_persona_result(survey)
    
    # SurveyResult 객체 생성
    survey_result = SurveyResult.objects.create(
        survey=survey,
        persona_type=result_data['persona_type'],
        matching_score=result_data['matching_score'],
        recommended_areas=result_data['recommended_areas'],
        recommended_properties=result_data['recommended_properties'],
        detailed_analysis={
            'matching_reasons': result_data['matching_reasons'],
            'persona_description': result_data['persona_description'],
            'radar_chart_data': result_data['radar_chart_data'],
            'all_scores': result_data['all_scores']
        }
    )
    
    return survey_result

def get_survey_result_summary(survey_result):
    """설문 결과 요약 정보 반환"""
    persona_desc = survey_result.detailed_analysis.get('persona_description', {})
    
    return {
        'persona_name': survey_result.persona_type.name,
        'persona_title': persona_desc.get('title', ''),
        'persona_subtitle': persona_desc.get('subtitle', ''),
        'matching_score': survey_result.matching_score,
        'matching_reasons': survey_result.detailed_analysis.get('matching_reasons', []),
        'recommended_areas': survey_result.recommended_areas,  # 모든 추천 지역
        'top_areas': survey_result.recommended_areas[:3],  # 상위 3개 지역 (하위 호환성)
        'recommended_properties': survey_result.recommended_properties[:2],  # 상위 2개 매물 타입
        'radar_chart_data': survey_result.detailed_analysis.get('radar_chart_data', {}),
        'persona_characteristics': persona_desc.get('characteristics', []),
        'ideal_lifestyle': persona_desc.get('ideal_lifestyle', ''),
        'persona_color': persona_desc.get('color', '#4A90E2'),
        'persona_icon': persona_desc.get('icon', '🏠')
    }
