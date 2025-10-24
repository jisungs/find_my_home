from django.core.management.base import BaseCommand
from results.models import PersonaType

class Command(BaseCommand):
    help = '6개 부산 페르소나 타입 데이터를 생성합니다'

    def handle(self, *args, **options):
        # 기존 데이터 삭제
        PersonaType.objects.all().delete()
        
        # 6개 부산 페르소나 타입 데이터 생성
        personas_data = [
            {
                'name': '해안가_라이프스타일형',
                'description': '해운대, 송정 등 해안가 지역을 선호하며, 바다와 가까운 환경에서 가족과 함께하는 라이프스타일을 추구합니다.',
                'color_code': '#4A90E2',
                'icon': '🏖️',
                'characteristics': {
                    'location_preference': '해안가',
                    'lifestyle': '가족 중심',
                    'environment': '자연 친화적',
                    'accessibility': '해변 접근성 중시'
                },
                'recommended_areas': ['해운대구', '송정', '광안리', '남포동']
            },
            {
                'name': '도심_라이프스타일형',
                'description': '서면, 부산진구 등 도심 지역을 선호하며, 교통과 생활 편의성을 중시하는 현대적인 라이프스타일을 추구합니다.',
                'color_code': '#50C878',
                'icon': '🏙️',
                'characteristics': {
                    'location_preference': '도심',
                    'lifestyle': '현대적',
                    'environment': '도시적',
                    'accessibility': '교통 편의성 중시'
                },
                'recommended_areas': ['서면', '부산진구', '동래구', '연제구']
            },
            {
                'name': '자연친화_크리에이티브형',
                'description': '금정구, 연제구 등 자연환경이 우수한 지역을 선호하며, 창작 활동과 개인 공간을 중시합니다.',
                'color_code': '#8B4513',
                'icon': '🌿',
                'characteristics': {
                    'location_preference': '자연환경',
                    'lifestyle': '창작 중심',
                    'environment': '조용한 환경',
                    'accessibility': '개인 공간 중시'
                },
                'recommended_areas': ['금정구', '연제구', '기장군', '수영구']
            },
            {
                'name': '산업도시_자연친화형',
                'description': '사상구, 강서구 등 산업단지와 자연이 조화된 지역을 선호하며, 실용성과 자연환경을 모두 고려합니다.',
                'color_code': '#FF6347',
                'icon': '🏭',
                'characteristics': {
                    'location_preference': '산업단지 근처',
                    'lifestyle': '실용적',
                    'environment': '산업-자연 조화',
                    'accessibility': '업무 접근성 중시'
                },
                'recommended_areas': ['사상구', '강서구', '북구', '사하구']
            },
            {
                'name': '항만_라이프스타일형',
                'description': '남구, 동구 등 항만 지역을 선호하며, 물류와 해운업계와 관련된 생활을 추구합니다.',
                'color_code': '#4169E1',
                'icon': '🚢',
                'characteristics': {
                    'location_preference': '항만 지역',
                    'lifestyle': '물류 중심',
                    'environment': '항만 환경',
                    'accessibility': '항만 접근성 중시'
                },
                'recommended_areas': ['남구', '동구', '영도구', '중구']
            },
            {
                'name': '모던_미니멀형',
                'description': '북구, 사하구 등 교통이 편리하고 현대적인 시설이 갖춰진 지역을 선호하며, 미니멀한 라이프스타일을 추구합니다.',
                'color_code': '#708090',
                'icon': '🏠',
                'characteristics': {
                    'location_preference': '교통 중심',
                    'lifestyle': '미니멀',
                    'environment': '현대적',
                    'accessibility': '통근 최적화'
                },
                'recommended_areas': ['북구', '사하구', '금정구', '연제구']
            }
        ]
        
        # 데이터 생성
        for data in personas_data:
            PersonaType.objects.create(**data)
        
        self.stdout.write(
            self.style.SUCCESS('6개 부산 페르소나 타입 데이터가 성공적으로 생성되었습니다!')
        )
