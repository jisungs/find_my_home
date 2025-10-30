from django.core.management.base import BaseCommand
from property.models import Property

class Command(BaseCommand):
    help = '부산 매물 샘플 데이터를 생성합니다'

    def handle(self, *args, **options):
        # 기존 샘플 데이터 삭제
        Property.objects.filter(is_active=True).delete()
        
        # 부산 매물 샘플 데이터 생성
        properties_data = [
            {
                'title': '해운대 해변 근처 단독주택',
                'property_type': '단독주택',
                'location': '부산광역시 해운대구 우동 123번지',
                'district': '해운대구',
                'price': 850000000,  # 8억 5천만원
                'area': '대지 80평 / 건물 45평',
                'land_area': 80,
                'building_area': 45,
                'rooms': 4,
                'bathrooms': 2,
                'parking': 2,
                'garden_area': 30,
                'description': '''해운대 해변에서 도보 5분 거리의 프리미엄 단독주택입니다.
                
[주소]
부산광역시 해운대구 우동 123번지

[가격]
8억 5천만원

[교통]
- 지하철 2호선 해운대역 도보 10분
- 해운대해수욕장 도보 5분
- 해운대순환버스 정류장 100m
- 부산역까지 30분 (지하철)

[학군]
- 해운대초등학교 인근 (도보 8분)
- 해운대중학교 인근 (도보 10분)
- 해운대고등학교 인근 (도보 15분)
- 부산대학교 해운대캠퍼스 인근

[기타 주변환경]
- 해운대해수욕장 및 마린시티 인근
- 대형마트, 백화점 5분 거리
- 해운대구청, 경찰서 등 공공기관 인접
- 해운대 의료원 근접 (10분)
- 카페 거리 및 레스토랑 다수
- 해운대 온천시설 이용 가능
- 정원 30평으로 여유있는 휴식 공간 제공''',
                'images': [],
                'persona_match': '해안가_라이프스타일형',
                'transportation_score': 90,
                'education_score': 85,
                'lifestyle_score': 95,
                'investment_score': 80,
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': '서면 도심 복층 타운하우스',
                'property_type': '타운하우스',
                'location': '부산광역시 부산진구 전포동 456번지',
                'district': '부산진구',
                'price': 680000000,  # 6억 8천만원
                'area': '대지 60평 / 건물 55평 (복층)',
                'land_area': 60,
                'building_area': 55,
                'rooms': 3,
                'bathrooms': 2,
                'parking': 1,
                'garden_area': 10,
                'description': '''서면 도심 복층 타운하우스입니다. 교통과 생활 편의성이 뛰어납니다.
                
[주소]
부산광역시 부산진구 전포동 456번지

[가격]
6억 8천만원

[교통]
- 지하철 1호선 전포역 도보 3분
- 지하철 2호선 서면역 도보 7분
- 서면 번화가 도보 5분
- 부산역까지 15분 (지하철)
- 광안리 해수욕장까지 20분

[학군]
- 전포초등학교 인근 (도보 5분)
- 개성중학교 인근 (도보 8분)
- 부산중앙고등학교 인근 (도보 12분)
- 부산외국어대학교 인근

[기타 주변환경]
- 서면 상권 인접 (쇼핑, 식당, 카페)
- 대형마트 (이마트, 롯데마트) 근접
- 부산진구청, 세무서 등 공공기관 인근
- 부산의료원 접근 용이
- 전포동 카페거리 근접
- 복층 구조로 공간 활용 극대화''',
                'images': [],
                'persona_match': '도심_라이프스타일형',
                'transportation_score': 95,
                'education_score': 80,
                'lifestyle_score': 90,
                'investment_score': 85,
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': '금정구 자연 속 단독주택',
                'property_type': '단독주택',
                'location': '부산광역시 금정구 청룡동 789번지',
                'district': '금정구',
                'price': 720000000,  # 7억 2천만원
                'area': '대지 120평 / 건물 50평',
                'land_area': 120,
                'building_area': 50,
                'rooms': 3,
                'bathrooms': 2,
                'parking': 3,
                'garden_area': 70,
                'description': '''금정산 자락의 넓은 정원이 있는 단독주택입니다.
                
[주소]
부산광역시 금정구 청룡동 789번지

[가격]
7억 2천만원

[교통]
- 지하철 1호선 범어사역 도보 15분
- 버스 정류장 도보 5분
- 금정구청까지 10분
- 시내 중심가까지 25분

[학군]
- 청룡초등학교 인근 (도보 10분)
- 금정중학교 인근 (도보 12분)
- 부산외국어고등학교 인근
- 부산대학교 신촌캠퍼스 근접

[기타 주변환경]
- 금정산 등산로 근접
- 넓은 정원 70평 (재배 및 휴식 공간)
- 조용한 주거 환경
- 자연 친화적 주변 환경
- 대형마트 10분 거리
- 금정구청 등 공공기관 접근 용이
- 창작 공간으로 활용 가능한 구조''',
                'images': [],
                'persona_match': '자연친화_크리에이티브형',
                'transportation_score': 70,
                'education_score': 75,
                'lifestyle_score': 85,
                'investment_score': 70,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': '사상구 산업단지 근처 단독주택',
                'property_type': '단독주택',
                'location': '부산광역시 사상구 괘법동 234번지',
                'district': '사상구',
                'price': 550000000,  # 5억 5천만원
                'area': '대지 90평 / 건물 40평',
                'land_area': 90,
                'building_area': 40,
                'rooms': 3,
                'bathrooms': 2,
                'parking': 2,
                'garden_area': 50,
                'description': '''사상구 산업단지 근처의 넓은 대지 단독주택입니다.
                
[주소]
부산광역시 사상구 괘법동 234번지

[가격]
5억 5천만원

[교통]
- 지하철 2호선 사상역 도보 12분
- 버스 정류장 도보 3분
- 김해공항까지 30분
- 부산역까지 25분

[학군]
- 괘법초등학교 인근 (도보 8분)
- 덕포중학교 인근 (도보 10분)
- 학산고등학교 인근
- 부산경상대학교 근접

[기타 주변환경]
- 사상산업단지 근접 (출퇴근 편리)
- 넓은 정원 50평
- 자연과 산업이 조화된 환경
- 대형마트 및 생활편의시설 인근
- 사상구청 등 공공기관 접근 용이
- 조용한 주거 환경''',
                'images': [],
                'persona_match': '산업도시_자연친화형',
                'transportation_score': 75,
                'education_score': 70,
                'lifestyle_score': 75,
                'investment_score': 75,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': '영도구 항만 전망 단독주택',
                'property_type': '단독주택',
                'location': '부산광역시 영도구 남항동 567번지',
                'district': '영도구',
                'price': 650000000,  # 6억 5천만원
                'area': '대지 70평 / 건물 42평',
                'land_area': 70,
                'building_area': 42,
                'rooms': 3,
                'bathrooms': 2,
                'parking': 2,
                'garden_area': 28,
                'description': '''영도구 항만 전망이 좋은 단독주택입니다.
                
[주소]
부산광역시 영도구 남항동 567번지

[가격]
6억 5천만원

[교통]
- 버스 정류장 도보 2분
- 부산역까지 20분
- 항만 근접으로 해상교통 편리
- 중구, 남구 접근 용이

[학군]
- 영도초등학교 인근 (도보 7분)
- 영도중학교 인근 (도보 9분)
- 영도고등학교 인근
- 부산해사고등학교 근접

[기타 주변환경]
- 부산항 전망
- 태종대, 이기대 등 관광지 근접
- 해상교통 이용 편리
- 가족 중심 주거 환경
- 영도구청 등 공공기관 접근 용이
- 정원 28평''',
                'images': [],
                'persona_match': '항만_라이프스타일형',
                'transportation_score': 75,
                'education_score': 72,
                'lifestyle_score': 80,
                'investment_score': 70,
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': '남구 미니멀 모던 빌라',
                'property_type': '빌라',
                'location': '부산광역시 남구 대연동 890번지',
                'district': '남구',
                'price': 490000000,  # 4억 9천만원
                'area': '대지 50평 / 건물 35평',
                'land_area': 50,
                'building_area': 35,
                'rooms': 2,
                'bathrooms': 1,
                'parking': 1,
                'garden_area': 15,
                'description': '''남구 대연동의 모던하고 효율적인 공간 구성 빌라입니다.
                
[주소]
부산광역시 남구 대연동 890번지

[가격]
4억 9천만원

[교통]
- 지하철 2호선 대연역 도보 8분
- 버스 정류장 도보 3분
- 광안리 해수욕장 도보 12분
- 시내 중심가까지 20분

[학군]
- 대연초등학교 인근 (도보 6분)
- 대연중학교 인근 (도보 8분)
- 경남고등학교 인근
- 부산대학교 근접

[기타 주변환경]
- 미니멀 라이프스타일에 최적화된 공간
- 효율적인 공간 활용
- 광안리 해수욕장 근접
- 대연공원 인근
- 대형마트 및 생활편의시설 접근 용이
- 남구청 등 공공기관 접근 용이
- 작은 정원 15평''',
                'images': [],
                'persona_match': '모던_미니멀형',
                'transportation_score': 85,
                'education_score': 80,
                'lifestyle_score': 88,
                'investment_score': 80,
                'is_active': True,
                'is_featured': False,
            },
        ]
        
        # 매물 생성
        created_count = 0
        for prop_data in properties_data:
            property_obj, created = Property.objects.get_or_create(
                title=prop_data['title'],
                defaults=prop_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {property_obj.title} 생성 완료')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ {property_obj.title} 이미 존재함')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 총 {created_count}개의 매물 데이터 생성 완료!')
        )

