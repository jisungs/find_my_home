from django.core.management.base import BaseCommand
from survey.models import SurveyQuestion

class Command(BaseCommand):
    help = '12문항 설문 데이터를 생성합니다'

    def handle(self, *args, **options):
        # 기존 데이터 삭제
        SurveyQuestion.objects.all().delete()
        
        # 12문항 설문 데이터 생성
        questions_data = [
            # STEP 1: 하드 필터 (5문항)
            {
                'question_id': 'Q1',
                'question_text': '출퇴근 조건은 어떻게 되시나요?',
                'question_type': 'single',
                'options': ['대중교통 30분 이내', '자차 30분 이내', '대중교통 1시간 이내', '자차 1시간 이내', '시간 제약 없음'],
                'step': 1,
                'order': 1
            },
            {
                'question_id': 'Q2',
                'question_text': '예산 범위는 어떻게 되시나요?',
                'question_type': 'single',
                'options': ['3억 이하', '3-5억', '5-8억', '8-12억', '12억 이상'],
                'step': 1,
                'order': 2
            },
            {
                'question_id': 'Q3',
                'question_text': '자녀 상황은 어떻게 되시나요?',
                'question_type': 'single',
                'options': ['자녀 없음', '유아 (0-6세)', '초등학생', '중고등학생', '성인 자녀'],
                'step': 1,
                'order': 3
            },
            {
                'question_id': 'Q4',
                'question_text': '필수 공간 요구사항을 선택해주세요.',
                'question_type': 'multiple',
                'options': ['넓은 거실', '독립된 서재', '큰 주방', '정원/테라스', '차고/주차공간', '다용도실'],
                'step': 1,
                'order': 4
            },
            {
                'question_id': 'Q5',
                'question_text': '주로 언제 집에서 시간을 보내시나요?',
                'question_type': 'single',
                'options': ['주말만', '평일 저녁', '평일 오후', '거의 매일', '불규칙적'],
                'step': 1,
                'order': 5
            },
            
            # STEP 2: 감성 프로필 (4문항)
            {
                'question_id': 'Q6',
                'question_text': '집의 의미를 우선순위로 정렬해주세요.',
                'question_type': 'drag',
                'options': ['안식처', '작업공간', '가족 공간', '투자 자산', '자아 표현'],
                'step': 2,
                'order': 1
            },
            {
                'question_id': 'Q7',
                'question_text': '이상적인 주말 시나리오는 무엇인가요?',
                'question_type': 'single',
                'options': ['정원 가꾸기', '서재에서 독서', '가족과 시간', '친구들과 파티', '혼자만의 시간'],
                'step': 2,
                'order': 2
            },
            {
                'question_id': 'Q8',
                'question_text': '이웃과의 관계는 어떻게 생각하시나요?',
                'question_type': 'slider',
                'options': ['완전히 독립', '친밀한 이웃'],
                'step': 2,
                'order': 3
            },
            {
                'question_id': 'Q9',
                'question_text': '선호하는 디자인 스타일은 무엇인가요?',
                'question_type': 'single',
                'options': ['모던 미니멀', '자연스러운 나무톤', '클래식한 전통', '인더스트리얼', '컬러풀한 개성'],
                'step': 2,
                'order': 4
            },
            
            # STEP 3: 현실 제약 (3문항)
            {
                'question_id': 'Q10',
                'question_text': '의사결정 타임라인은 어떻게 되시나요?',
                'question_type': 'single',
                'options': ['1개월 이내', '3개월 이내', '6개월 이내', '1년 이내', '1년 이후'],
                'step': 3,
                'order': 1
            },
            {
                'question_id': 'Q11',
                'question_text': '어떤 불편함을 수용할 수 있나요?',
                'question_type': 'multiple',
                'options': ['교통 불편', '소음', '주차 어려움', '학군 부족', '상업시설 부족', '노후 시설'],
                'step': 3,
                'order': 2
            },
            {
                'question_id': 'Q12',
                'question_text': '예상 못한 비용이 발생했을 때 대응 방법은?',
                'question_type': 'single',
                'options': ['즉시 해결', '단계적 해결', '우선순위 정해서 해결', '최소한만 해결', '미뤄두기'],
                'step': 3,
                'order': 3
            }
        ]
        
        # 데이터 생성
        for data in questions_data:
            SurveyQuestion.objects.create(**data)
        
        self.stdout.write(
            self.style.SUCCESS('12문항 설문 데이터가 성공적으로 생성되었습니다!')
        )
