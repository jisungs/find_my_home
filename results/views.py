from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SurveyResult
from .result_generator import get_survey_result_summary

def show_result(request, survey_id):
    """결과 페이지 표시"""
    survey_result = get_object_or_404(SurveyResult, survey_id=survey_id)
    
    # 결과 요약 정보 생성
    result_summary = get_survey_result_summary(survey_result)
    
    context = {
        'survey_result': survey_result,
        'result_summary': result_summary,
        'survey': survey_result.survey
    }
    
    return render(request, 'results/result.html', context)

def share_result(request, survey_id):
    """결과 공유 기능"""
    survey_result = get_object_or_404(SurveyResult, survey_id=survey_id)
    
    # 공유용 데이터 생성
    result_summary = get_survey_result_summary(survey_result)
    
    # 공유 텍스트 생성
    share_text = f"""
🏠 {result_summary['persona_title']} ({result_summary['matching_score']}점 매칭!)

{result_summary['persona_subtitle']}

📊 매칭 이유:
{chr(10).join([f"• {reason}" for reason in result_summary['matching_reasons'][:3]])}

📍 추천 지역:
{chr(10).join([f"• {area['name']}" for area in result_summary['top_areas'][:3]])}

부산 집 찾기 서비스에서 나만의 집 스타일을 확인해보세요!
    """.strip()
    
    context = {
        'survey_result': survey_result,
        'result_summary': result_summary,
        'share_text': share_text,
        'survey': survey_result.survey
    }
    
    return render(request, 'results/share.html', context)
