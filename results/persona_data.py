# 부산 지역별 상세 정보 데이터
BUSAN_AREA_DATA = {
    '해운대구': {
        'persona_match': '해안가_라이프스타일형',
        'description': '부산의 대표적인 해안가 지역으로 바다와 가까운 환경에서 가족과 함께하는 라이프스타일을 추구하는 분들에게 최적입니다.',
        'price_range': '5-12억',
        'advantages': [
            '해운대 해수욕장 접근성',
            '우수한 학군 (해운대초, 해운대중)',
            '다양한 문화시설',
            '지하철 2호선 연결'
        ],
        'disadvantages': [
            '여름철 관광객 증가',
            '교통 체증',
            '높은 부동산 가격'
        ],
        'transportation_score': 85,
        'education_score': 90,
        'lifestyle_score': 95,
        'investment_score': 80,
        'nature_score': 95,
        'convenience_score': 85
    },
    
    '서면': {
        'persona_match': '도심_라이프스타일형',
        'description': '부산의 핵심 상업지구로 교통과 생활 편의성이 뛰어나 현대적인 도심 라이프스타일을 추구하는 분들에게 적합합니다.',
        'price_range': '3-8억',
        'advantages': [
            '지하철 1,2호선 교차점',
            '대형 쇼핑몰 밀집',
            '우수한 학군',
            '다양한 업무시설'
        ],
        'disadvantages': [
            '높은 인구밀도',
            '소음 및 교통체증',
            '제한된 주차공간'
        ],
        'transportation_score': 95,
        'education_score': 85,
        'lifestyle_score': 90,
        'investment_score': 90,
        'nature_score': 40,
        'convenience_score': 95
    },
    
    '금정구': {
        'persona_match': '자연친화_크리에이티브형',
        'description': '금정산과 가까운 자연환경이 우수한 지역으로 창작 활동과 개인 공간을 중시하는 분들에게 최적입니다.',
        'price_range': '3-6억',
        'advantages': [
            '금정산 등산로 접근성',
            '조용한 주거환경',
            '넓은 부지 확보 가능',
            '자연친화적 환경'
        ],
        'disadvantages': [
            '대중교통 불편',
            '상업시설 부족',
            '언덕 지역으로 접근성 제한'
        ],
        'transportation_score': 60,
        'education_score': 70,
        'lifestyle_score': 85,
        'investment_score': 70,
        'nature_score': 95,
        'convenience_score': 60
    },
    
    '사상구': {
        'persona_match': '산업도시_자연친화형',
        'description': '산업단지와 자연이 조화된 지역으로 실용성과 자연환경을 모두 고려하는 분들에게 적합합니다.',
        'price_range': '2-5억',
        'advantages': [
            '김해공항 접근성',
            '산업단지 근접',
            '낙동강 근처 자연환경',
            '상대적으로 저렴한 가격'
        ],
        'disadvantages': [
            '공항 소음',
            '제한된 문화시설',
            '교통 체증'
        ],
        'transportation_score': 75,
        'education_score': 65,
        'lifestyle_score': 70,
        'investment_score': 75,
        'nature_score': 70,
        'convenience_score': 70
    },
    
    '남구': {
        'persona_match': '항만_라이프스타일형',
        'description': '부산항과 가까운 항만 지역으로 물류와 해운업계와 관련된 생활을 추구하는 분들에게 최적입니다.',
        'price_range': '3-7억',
        'advantages': [
            '부산항 접근성',
            '해운업계 기회',
            '다양한 문화시설',
            '지하철 1호선 연결'
        ],
        'disadvantages': [
            '항만 소음',
            '제한된 녹지공간',
            '높은 인구밀도'
        ],
        'transportation_score': 80,
        'education_score': 75,
        'lifestyle_score': 80,
        'investment_score': 85,
        'nature_score': 50,
        'convenience_score': 80
    },
    
    '북구': {
        'persona_match': '모던_미니멀형',
        'description': '교통이 편리하고 현대적인 시설이 갖춰진 지역으로 미니멀한 라이프스타일을 추구하는 분들에게 적합합니다.',
        'price_range': '2-6억',
        'advantages': [
            '지하철 1호선 연결',
            '현대적인 아파트 단지',
            '상대적으로 저렴한 가격',
            '편리한 교통망'
        ],
        'disadvantages': [
            '제한된 문화시설',
            '높은 인구밀도',
            '녹지공간 부족'
        ],
        'transportation_score': 85,
        'education_score': 70,
        'lifestyle_score': 75,
        'investment_score': 75,
        'nature_score': 45,
        'convenience_score': 80
    }
}

# 페르소나별 매칭 이유 생성
def get_matching_reasons(answers, persona_type):
    """사용자 답변을 바탕으로 매칭 이유 생성"""
    reasons = []
    
    if persona_type == '해안가_라이프스타일형':
        if answers.get('Q7') == '정원 가꾸기':
            reasons.append('정원 가꾸기를 선호하시는 것으로 보아 자연친화적인 환경을 원하시는군요!')
        if answers.get('Q6') and '안식처' in str(answers.get('Q6')):
            reasons.append('집을 안식처로 생각하시는 마음이 해안가의 평화로운 환경과 잘 맞습니다.')
        if answers.get('Q3') in ['유아 (0-6세)', '초등학생', '중고등학생']:
            reasons.append('자녀가 있으시니 해운대의 우수한 학군이 큰 장점이 될 것입니다.')
    
    elif persona_type == '도심_라이프스타일형':
        if answers.get('Q7') == '친구들과 파티':
            reasons.append('친구들과의 모임을 즐기시는 성향이 도심의 활기찬 분위기와 잘 맞습니다!')
        if answers.get('Q6') and '작업공간' in str(answers.get('Q6')):
            reasons.append('집을 작업공간으로 활용하시려는 계획이 서면의 업무환경과 잘 맞습니다.')
        if answers.get('Q1') == '대중교통 30분 이내':
            reasons.append('대중교통을 중시하시는 점이 서면의 교통편리성과 완벽하게 맞습니다.')
    
    elif persona_type == '자연친화_크리에이티브형':
        if answers.get('Q7') == '서재에서 독서':
            reasons.append('독서를 즐기시는 취향이 금정구의 조용한 환경과 잘 맞습니다!')
        if answers.get('Q6') and '작업공간' in str(answers.get('Q6')):
            reasons.append('창작 활동을 위한 공간을 원하시는 점이 금정구의 넓은 부지와 잘 맞습니다.')
        if answers.get('Q8') and int(answers.get('Q8', 50)) < 30:
            reasons.append('독립적인 생활을 선호하시는 성향이 금정구의 조용한 환경과 잘 맞습니다.')
    
    elif persona_type == '산업도시_자연친화형':
        if answers.get('Q1') in ['자차 30분 이내', '자차 1시간 이내']:
            reasons.append('자차 이용을 선호하시는 점이 사상구의 접근성과 잘 맞습니다!')
        if answers.get('Q7') == '정원 가꾸기':
            reasons.append('정원 가꾸기를 즐기시는 취향이 사상구의 자연환경과 잘 맞습니다.')
        if answers.get('Q2') in ['3억 이하', '3-5억']:
            reasons.append('합리적인 예산 계획이 사상구의 가격대와 잘 맞습니다.')
    
    elif persona_type == '항만_라이프스타일형':
        if answers.get('Q6') and '가족 공간' in str(answers.get('Q6')):
            reasons.append('가족 중심의 생활을 원하시는 점이 남구의 가족친화적 환경과 잘 맞습니다!')
        if answers.get('Q7') == '가족과 시간':
            reasons.append('가족과의 시간을 중시하시는 마음이 남구의 분위기와 잘 맞습니다.')
        if answers.get('Q3') in ['초등학생', '중고등학생', '성인 자녀']:
            reasons.append('자녀 교육을 고려하시는 점이 남구의 교육환경과 잘 맞습니다.')
    
    elif persona_type == '모던_미니멀형':
        if answers.get('Q9') == '모던 미니멀':
            reasons.append('모던 미니멀 스타일을 선호하시는 점이 북구의 현대적인 환경과 잘 맞습니다!')
        if answers.get('Q7') == '혼자만의 시간':
            reasons.append('개인 시간을 중시하시는 성향이 북구의 분위기와 잘 맞습니다.')
        if answers.get('Q2') in ['3억 이하', '3-5억']:
            reasons.append('합리적인 예산 계획이 북구의 가격대와 잘 맞습니다.')
    
    return reasons

def get_recommended_areas(persona_type):
    """페르소나별 추천 지역 반환"""
    recommended_areas = []
    
    for area_name, area_data in BUSAN_AREA_DATA.items():
        if area_data['persona_match'] == persona_type:
            recommended_areas.append({
                'name': area_name,
                'description': area_data['description'],
                'price_range': area_data['price_range'],
                'advantages': area_data['advantages'],
                'disadvantages': area_data['disadvantages'],
                'scores': {
                    'transportation': area_data['transportation_score'],
                    'education': area_data['education_score'],
                    'lifestyle': area_data['lifestyle_score'],
                    'investment': area_data['investment_score'],
                    'nature': area_data['nature_score'],
                    'convenience': area_data['convenience_score']
                }
            })
    
    return recommended_areas

def get_persona_description(persona_type):
    """페르소나별 상세 설명 반환"""
    descriptions = {
        '해안가_라이프스타일형': {
            'title': '해안가 라이프스타일형',
            'subtitle': '바다와 함께하는 가족 중심의 삶',
            'description': '해운대, 송정 등 해안가 지역을 선호하며, 바다와 가까운 환경에서 가족과 함께하는 라이프스타일을 추구합니다. 자연친화적이고 평화로운 환경을 중시하며, 자녀 교육과 가족 시간을 중요하게 생각합니다.',
            'characteristics': [
                '자연친화적 환경 선호',
                '가족 중심의 라이프스타일',
                '해변 접근성 중시',
                '평화로운 주거환경 추구'
            ],
            'ideal_lifestyle': '주말에는 가족과 함께 해변을 산책하고, 정원을 가꾸며 자연과 함께하는 시간을 즐깁니다.',
            'color': '#4A90E2',
            'icon': '🏖️'
        },
        
        '도심_라이프스타일형': {
            'title': '도심 라이프스타일형',
            'subtitle': '현대적이고 활기찬 도시 생활',
            'description': '서면, 부산진구 등 도심 지역을 선호하며, 교통과 생활 편의성을 중시하는 현대적인 라이프스타일을 추구합니다. 다양한 문화시설과 편의시설에 쉽게 접근할 수 있는 환경을 원합니다.',
            'characteristics': [
                '교통 편의성 중시',
                '현대적인 도시 생활',
                '문화시설 접근성',
                '활기찬 분위기 선호'
            ],
            'ideal_lifestyle': '친구들과의 모임을 즐기고, 다양한 문화활동에 참여하며 도심의 활기를 느끼는 생활을 합니다.',
            'color': '#50C878',
            'icon': '🏙️'
        },
        
        '자연친화_크리에이티브형': {
            'title': '자연친화 크리에이티브형',
            'subtitle': '조용한 환경에서 창작하는 삶',
            'description': '금정구, 연제구 등 자연환경이 우수한 지역을 선호하며, 창작 활동과 개인 공간을 중시합니다. 조용하고 독립적인 환경에서 자신만의 작업을 할 수 있는 공간을 원합니다.',
            'characteristics': [
                '조용한 환경 선호',
                '창작 활동 중시',
                '개인 공간 중시',
                '자연환경 추구'
            ],
            'ideal_lifestyle': '서재에서 독서하고 창작활동을 하며, 자연과 함께하는 조용한 시간을 즐깁니다.',
            'color': '#8B4513',
            'icon': '🌿'
        },
        
        '산업도시_자연친화형': {
            'title': '산업도시 자연친화형',
            'subtitle': '실용성과 자연의 조화',
            'description': '사상구, 강서구 등 산업단지와 자연이 조화된 지역을 선호하며, 실용성과 자연환경을 모두 고려합니다. 업무 접근성과 자연환경을 동시에 만족시킬 수 있는 균형잡힌 환경을 원합니다.',
            'characteristics': [
                '업무 접근성 중시',
                '자연환경 추구',
                '실용적 사고',
                '균형잡힌 라이프스타일'
            ],
            'ideal_lifestyle': '업무와 자연을 모두 고려하여 실용적이면서도 자연친화적인 생활을 추구합니다.',
            'color': '#FF6347',
            'icon': '🏭'
        },
        
        '항만_라이프스타일형': {
            'title': '항만 라이프스타일형',
            'subtitle': '바다와 함께하는 가족 중심의 삶',
            'description': '남구, 동구 등 항만 지역을 선호하며, 물류와 해운업계와 관련된 생활을 추구합니다. 바다와 가까운 환경에서 가족과 함께하는 시간을 중시하며, 항만의 활기와 가족의 평화를 동시에 원합니다.',
            'characteristics': [
                '항만 접근성 중시',
                '가족 중심 생활',
                '바다 환경 선호',
                '물류업계 기회'
            ],
            'ideal_lifestyle': '가족과 함께 바다를 바라보며 평화로운 시간을 보내고, 항만의 활기를 느끼는 생활을 합니다.',
            'color': '#4169E1',
            'icon': '🚢'
        },
        
        '모던_미니멀형': {
            'title': '모던 미니멀형',
            'subtitle': '간결하고 효율적인 현대적 삶',
            'description': '북구, 사하구 등 교통이 편리하고 현대적인 시설이 갖춰진 지역을 선호하며, 미니멀한 라이프스타일을 추구합니다. 불필요한 것 없이 간결하고 효율적인 생활을 원합니다.',
            'characteristics': [
                '미니멀 라이프스타일',
                '효율성 중시',
                '현대적 시설 선호',
                '간결한 생활'
            ],
            'ideal_lifestyle': '불필요한 것 없이 간결하고 효율적인 생활을 하며, 개인 시간을 중시합니다.',
            'color': '#708090',
            'icon': '🏠'
        }
    }
    
    return descriptions.get(persona_type, {})

def get_recommended_properties(persona_type):
    """페르소나별 추천 매물 타입 반환"""
    property_recommendations = {
        '해안가_라이프스타일형': [
            {
                'type': '단독주택',
                'description': '넓은 정원이 있는 단독주택',
                'features': ['정원', '테라스', '주차공간', '넓은 거실'],
                'price_range': '5-12억'
            },
            {
                'type': '타운하우스',
                'description': '가족 친화적인 타운하우스',
                'features': ['공용 정원', '주차공간', '넓은 거실', '아이방'],
                'price_range': '4-8억'
            }
        ],
        
        '도심_라이프스타일형': [
            {
                'type': '빌라',
                'description': '교통편리한 빌라',
                'features': ['지하철 접근성', '주차공간', '현대적 시설', '편의시설 근접'],
                'price_range': '3-6억'
            },
            {
                'type': '연립주택',
                'description': '도심 연립주택',
                'features': ['교통편리', '상업시설 근접', '현대적 시설', '학군 우수'],
                'price_range': '2-5억'
            }
        ],
        
        '자연친화_크리에이티브형': [
            {
                'type': '단독주택',
                'description': '넓은 부지의 단독주택',
                'features': ['넓은 부지', '독립된 서재', '자연환경', '조용한 환경'],
                'price_range': '3-6억'
            },
            {
                'type': '빌라',
                'description': '자연친화적 빌라',
                'features': ['자연환경', '조용한 환경', '넓은 공간', '창작공간'],
                'price_range': '2-4억'
            }
        ],
        
        '산업도시_자연친화형': [
            {
                'type': '단독주택',
                'description': '실용적인 단독주택',
                'features': ['넓은 부지', '주차공간', '자연환경', '업무 접근성'],
                'price_range': '2-5억'
            },
            {
                'type': '빌라',
                'description': '균형잡힌 빌라',
                'features': ['자연환경', '업무 접근성', '현대적 시설', '주차공간'],
                'price_range': '2-4억'
            }
        ],
        
        '항만_라이프스타일형': [
            {
                'type': '단독주택',
                'description': '가족 친화적 단독주택',
                'features': ['넓은 거실', '아이방', '주차공간', '가족 공간'],
                'price_range': '3-7억'
            },
            {
                'type': '타운하우스',
                'description': '가족 중심 타운하우스',
                'features': ['가족 공간', '아이방', '주차공간', '공용 시설'],
                'price_range': '3-6억'
            }
        ],
        
        '모던_미니멀형': [
            {
                'type': '빌라',
                'description': '미니멀한 빌라',
                'features': ['현대적 시설', '효율적 공간', '교통편리', '간결한 디자인'],
                'price_range': '2-4억'
            },
            {
                'type': '연립주택',
                'description': '효율적인 연립주택',
                'features': ['교통편리', '현대적 시설', '효율적 공간', '미니멀 디자인'],
                'price_range': '2-3억'
            }
        ]
    }
    
    return property_recommendations.get(persona_type, [])
