from django.db import models
from survey.models import Survey, SurveyAnswer
from results.models import PersonaType
import json

# 페르소나별 매칭 규칙 정의
PERSONA_RULES = {
    '해안가_라이프스타일형': {
        'hard_filters': {
            'Q1': ['대중교통 30분 이내', '자차 30분 이내'],  # 출퇴근 조건
            'Q2': ['5-8억', '8-12억', '12억 이상'],  # 예산 범위
            'Q3': ['유아 (0-6세)', '초등학생', '중고등학생'],  # 자녀 상황
        },
        'emotional_profile': {
            'Q6': ['안식처', '가족 공간'],  # 집의 의미 우선순위
            'Q7': ['정원 가꾸기', '가족과 시간'],  # 이상적인 주말
            'Q9': ['자연스러운 나무톤', '클래식한 전통'],  # 디자인 스타일
        },
        'constraints': {
            'Q8': [0, 40],  # 이웃과의 관계 (독립적)
            'Q11': ['교통 불편', '상업시설 부족'],  # 수용 가능한 불편함
        },
        'weights': {
            'hard_filters': 0.4,
            'emotional_profile': 0.4,
            'constraints': 0.2
        }
    },
    
    '도심_라이프스타일형': {
        'hard_filters': {
            'Q1': ['대중교통 30분 이내', '자차 30분 이내'],
            'Q2': ['3-5억', '5-8억', '8-12억'],
            'Q3': ['초등학생', '중고등학생', '성인 자녀'],
        },
        'emotional_profile': {
            'Q6': ['작업공간', '투자 자산'],
            'Q7': ['친구들과 파티', '혼자만의 시간'],
            'Q9': ['모던 미니멀', '인더스트리얼'],
        },
        'constraints': {
            'Q8': [40, 80],  # 이웃과의 관계 (중간)
            'Q11': ['소음', '주차 어려움'],
        },
        'weights': {
            'hard_filters': 0.4,
            'emotional_profile': 0.4,
            'constraints': 0.2
        }
    },
    
    '자연친화_크리에이티브형': {
        'hard_filters': {
            'Q1': ['대중교통 1시간 이내', '자차 1시간 이내', '시간 제약 없음'],
            'Q2': ['3-5억', '5-8억'],
            'Q3': ['자녀 없음', '유아 (0-6세)'],
        },
        'emotional_profile': {
            'Q6': ['작업공간', '자아 표현'],
            'Q7': ['서재에서 독서', '혼자만의 시간'],
            'Q9': ['자연스러운 나무톤', '컬러풀한 개성'],
        },
        'constraints': {
            'Q8': [0, 30],  # 이웃과의 관계 (매우 독립적)
            'Q11': ['교통 불편', '상업시설 부족', '노후 시설'],
        },
        'weights': {
            'hard_filters': 0.3,
            'emotional_profile': 0.5,
            'constraints': 0.2
        }
    },
    
    '산업도시_자연친화형': {
        'hard_filters': {
            'Q1': ['자차 30분 이내', '자차 1시간 이내'],
            'Q2': ['3억 이하', '3-5억', '5-8억'],
            'Q3': ['자녀 없음', '유아 (0-6세)', '초등학생'],
        },
        'emotional_profile': {
            'Q6': ['안식처', '작업공간'],
            'Q7': ['정원 가꾸기', '서재에서 독서'],
            'Q9': ['자연스러운 나무톤', '모던 미니멀'],
        },
        'constraints': {
            'Q8': [20, 60],  # 이웃과의 관계 (중간)
            'Q11': ['교통 불편', '소음', '상업시설 부족'],
        },
        'weights': {
            'hard_filters': 0.4,
            'emotional_profile': 0.3,
            'constraints': 0.3
        }
    },
    
    '항만_라이프스타일형': {
        'hard_filters': {
            'Q1': ['대중교통 30분 이내', '자차 30분 이내'],
            'Q2': ['3-5억', '5-8억'],
            'Q3': ['초등학생', '중고등학생', '성인 자녀'],
        },
        'emotional_profile': {
            'Q6': ['가족 공간', '투자 자산'],
            'Q7': ['가족과 시간', '친구들과 파티'],
            'Q9': ['클래식한 전통', '모던 미니멀'],
        },
        'constraints': {
            'Q8': [30, 70],  # 이웃과의 관계 (중간)
            'Q11': ['소음', '주차 어려움', '학군 부족'],
        },
        'weights': {
            'hard_filters': 0.4,
            'emotional_profile': 0.4,
            'constraints': 0.2
        }
    },
    
    '모던_미니멀형': {
        'hard_filters': {
            'Q1': ['대중교통 30분 이내', '자차 30분 이내'],
            'Q2': ['3억 이하', '3-5억', '5-8억'],
            'Q3': ['자녀 없음', '유아 (0-6세)'],
        },
        'emotional_profile': {
            'Q6': ['작업공간', '자아 표현'],
            'Q7': ['혼자만의 시간', '서재에서 독서'],
            'Q9': ['모던 미니멀', '인더스트리얼'],
        },
        'constraints': {
            'Q8': [20, 50],  # 이웃과의 관계 (독립적)
            'Q11': ['소음', '주차 어려움', '상업시설 부족'],
        },
        'weights': {
            'hard_filters': 0.3,
            'emotional_profile': 0.5,
            'constraints': 0.2
        }
    }
}

def analyze_survey_answers(survey):
    """설문 답변을 분석하여 딕셔너리로 반환"""
    answers = {}
    for answer in survey.surveyanswer_set.all():
        question_id = answer.question.question_id
        answer_text = answer.answer
        
        # JSON 형태의 답변 파싱 (드래그 정렬, 다중 선택)
        if answer.question.question_type in ['drag', 'multiple']:
            try:
                answers[question_id] = json.loads(answer_text)
            except:
                answers[question_id] = answer_text
        else:
            answers[question_id] = answer_text
    
    return answers

def check_hard_filters(answers, persona_rules):
    """하드 필터 체크"""
    score = 0
    total_checks = 0
    
    for question_id, expected_answers in persona_rules.items():
        if question_id in answers:
            user_answer = answers[question_id]
            total_checks += 1
            
            # 단일 선택의 경우
            if isinstance(user_answer, str):
                if user_answer in expected_answers:
                    score += 1
            # 다중 선택의 경우
            elif isinstance(user_answer, list):
                if any(ans in expected_answers for ans in user_answer):
                    score += 1
    
    return (score / total_checks * 100) if total_checks > 0 else 0

def analyze_emotional_profile(answers, persona_rules):
    """감성 프로필 분석"""
    score = 0
    total_checks = 0
    
    for question_id, expected_answers in persona_rules.items():
        if question_id in answers:
            user_answer = answers[question_id]
            total_checks += 1
            
            # 드래그 정렬의 경우 (우선순위)
            if question_id == 'Q6' and isinstance(user_answer, list):
                # 상위 3개 항목 중 매칭되는 것이 있는지 확인
                top_3 = user_answer[:3]
                if any(ans in expected_answers for ans in top_3):
                    score += 1
            # 단일 선택의 경우
            elif isinstance(user_answer, str):
                if user_answer in expected_answers:
                    score += 1
    
    return (score / total_checks * 100) if total_checks > 0 else 0

def consider_constraints(answers, persona_rules):
    """현실 제약 고려"""
    score = 0
    total_checks = 0
    
    for question_id, expected_value in persona_rules.items():
        if question_id in answers:
            user_answer = answers[question_id]
            total_checks += 1
            
            # 슬라이더의 경우 (Q8)
            if question_id == 'Q8':
                try:
                    slider_value = int(user_answer)
                    if expected_value[0] <= slider_value <= expected_value[1]:
                        score += 1
                except:
                    pass
            # 다중 선택의 경우 (Q11)
            elif isinstance(user_answer, list):
                if any(ans in expected_value for ans in user_answer):
                    score += 1
    
    return (score / total_checks * 100) if total_checks > 0 else 0

def calculate_persona_score(answers, persona_type):
    """특정 페르소나에 대한 점수 계산"""
    if persona_type not in PERSONA_RULES:
        return 0
    
    rules = PERSONA_RULES[persona_type]
    weights = rules['weights']
    
    # 각 카테고리별 점수 계산
    hard_filter_score = check_hard_filters(answers, rules['hard_filters'])
    emotional_score = analyze_emotional_profile(answers, rules['emotional_profile'])
    constraint_score = consider_constraints(answers, rules['constraints'])
    
    # 가중치 적용하여 최종 점수 계산
    final_score = (
        hard_filter_score * weights['hard_filters'] +
        emotional_score * weights['emotional_profile'] +
        constraint_score * weights['constraints']
    )
    
    return min(int(final_score), 100)  # 최대 100점

def match_persona(survey):
    """설문 결과를 바탕으로 최적의 페르소나 매칭"""
    answers = analyze_survey_answers(survey)
    persona_scores = {}
    
    # 모든 페르소나에 대해 점수 계산
    for persona_type in PERSONA_RULES.keys():
        score = calculate_persona_score(answers, persona_type)
        persona_scores[persona_type] = score
    
    # 가장 높은 점수의 페르소나 선택
    best_persona = max(persona_scores, key=persona_scores.get)
    best_score = persona_scores[best_persona]
    
    return {
        'persona_type': best_persona,
        'matching_score': best_score,
        'all_scores': persona_scores
    }
