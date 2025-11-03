# Django 기반 1주일 MVP 실행계획

## 📋 전체 전략 요약

**핵심 원칙**: Django 개발 → 12문항 설문 → 부산 집중 → 1주일 배포 → 유튜브 콘텐츠

**차별화 포인트**: 
- 12문항 설문 프레임워크 완전 활용
- Django 기반 안정적 서비스
- 부산 집중 전략 (깊이 > 넓이)
- 유튜브 친화적 결과 페이지
- Railway 자동 배포

**핵심 서비스**: 집 찾기 진단 + 부산 맞춤 정보 제공

**실현 가능성**: **85-90%** (Django 기반 안정성)

---

## 🎯 요구사항 분석

### ✅ 변경사항
1. **설문**: 5문항 → **12문항 모두 반영**
2. **기술스택**: No-code → **Django + Railway/PythonAnywhere**
3. **배포**: 1주일 내 완성 및 배포
4. **기존 설문 프레임워크**: 완전 활용

### ⚠️ 도전과제
- **12문항 설문** → 복잡도 증가
- **Django 개발** → 개발 시간 증가
- **1주일 제한** → 매우 타이트한 일정

---

## 🚀 Django 기반 1주일 MVP 실행계획

### 📅 일별 실행 계획 (7일)

**Day 1 (월)**: 프로젝트 설정 & 데이터베이스 설계
- [x] Django 프로젝트 생성
- [x] 데이터베이스 모델 설계 (설문, 결과, 매물)
- [x] 기본 템플릿 구조 설정
- [x] Railway 배포 환경 준비 (requirements.txt, Procfile, runtime.txt, settings.py 프로덕션 설정)

**Day 2 (화)**: 설문 시스템 개발
- [x] 12문항 설문 모델 구현
- [x] 설문 폼 생성 (진행률 표시)
- [x] 설문 결과 저장 로직
- [x] 기본 검증 및 에러 처리
- [x] 설문 템플릿 작성

**Day 3 (수)**: 결과 시스템 개발
- [x] 6개 부산 페르소나별 결과 모델
- [x] 매칭 알고리즘 구현 (IF-THEN 로직)
- [x] 결과 페이지 템플릿
- [x] 레이더 차트 (Chart.js) 연동

**Day 4 (목)**: 매물 시스템 & UI
- [x] 부산 매물 모델 구현
- [x] 매물 목록/상세 페이지
- [x] 매물 필터링 기능
- [x] 모바일 반응형 디자인

**Day 5 (금)**: 통합 테스트 & 완성
- [ ] 전체 흐름 테스트
- [ ] 버그 수정
- [ ] 성능 최적화
- [ ] 베타 테스트 준비

**Day 6 (토)**: 배포 & 유튜브 제작
- [ ] Railway/PythonAnywhere 배포
- [ ] 도메인 연결
- [ ] 유튜브 영상 촬영
- [ ] 편집 & 업로드

**Day 7 (일)**: 런칭 & 홍보
- [ ] 서비스 공식 런칭
- [ ] SNS 홍보
- [ ] 피드백 수집
- [ ] 개선 계획 수립

---

## 🛠️ 기술 스택 & 아키텍처

### 📱 Django 프로젝트 구조
```
find_my_home/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── survey/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
├── results/
│   ├── models.py
│   ├── views.py
│   └── templates/
├── properties/
│   ├── models.py
│   ├── views.py
│   └── templates/
└── static/
    ├── css/
    ├── js/
    └── images/
```

### 🗄️ 데이터베이스 모델 설계

**Survey 모델**:
```python
class Survey(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class SurveyAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=10)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Result 모델**:
```python
class SurveyResult(models.Model):
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)
    persona_type = models.CharField(max_length=50)
    matching_score = models.IntegerField()
    recommended_areas = models.JSONField()
    recommended_properties = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Property 모델**:
```python
class Property(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    area = models.CharField(max_length=50)
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    parking = models.IntegerField()
    garden_area = models.IntegerField()
    description = models.TextField()
    images = models.JSONField()
    persona_match = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 📝 12문항 설문 구현

### 🔍 설문 구조 (기존 프레임워크 활용)

**STEP 1: 하드 필터 (5문항)**
- Q1. 출퇴근 조건
- Q2. 예산 범위  
- Q3. 자녀 상황
- Q4. 필수 공간 요구사항
- Q5. 생활 패턴

**STEP 2: 감성 프로필 (4문항)**
- Q6. 집의 의미 (우선순위 정렬)
- Q7. 이상적인 주말 시나리오
- Q8. 이웃과의 관계
- Q9. 디자인 스타일 (이미지 선택)

**STEP 3: 현실 제약 (3문항)**
- Q10. 의사결정 타임라인
- Q11. 불편함 수용도
- Q12. 예상 못한 비용 대응

### 🎯 매칭 알고리즘 (IF-THEN 로직)

```python
def calculate_persona_match(survey_answers):
    # 하드 필터 체크
    if not check_hard_filters(survey_answers):
        return None
    
    # 감성 프로필 분석
    emotional_profile = analyze_emotional_profile(survey_answers)
    
    # 현실 제약 고려
    constraints = analyze_constraints(survey_answers)
    
    # 최종 페르소나 매칭
    persona_type = match_persona(emotional_profile, constraints)
    
    return persona_type

def match_persona(emotional_profile, constraints):
    if emotional_profile['home_meaning'] == '안식처' and emotional_profile['weekend'] == '정원':
        return '해안가_라이프스타일형'
    elif emotional_profile['home_meaning'] == '작업공간' and emotional_profile['weekend'] == '서재':
        return '자연친화_크리에이티브형'
    # ... 6개 페르소나 매칭 로직
```

---

## 🎨 UI/UX 디자인 (유튜브 친화적)

### 📱 메인 페이지
- **히어로 섹션**: "나에게 맞는 부산 집은?"
- **설문 시작 버튼**: 큰 CTA 버튼
- **진행률 표시**: 12문항 진행 상황
- **모바일 우선**: 반응형 디자인

### 📊 결과 페이지
- **레이더 차트**: 시각적 임팩트
- **매칭 점수**: 92% 매칭도 표시
- **추천 지역 TOP 3**: 부산 지역별 분석
- **맞춤 매물 3개**: 실제 매물 정보
- **공유 기능**: SNS 연동

### 🏠 매물 상세 페이지
- **사진 갤러리**: 3-5장 이미지
- **상세 정보**: 가격, 면적, 방 개수
- **매칭 이유**: 왜 추천했는지 설명
- **문의하기**: 간단한 연락 폼

---

## 🚀 배포 전략

### 🌐 Railway 배포 (추천)
```yaml
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py runserver 0.0.0.0:$PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

### 📦 requirements.txt
```
Django==4.2.7
Pillow==10.0.1
psycopg2-binary==2.9.7
gunicorn==21.2.0
whitenoise==6.6.0
```

### 🔧 환경 변수 설정
```python
# settings.py
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

ALLOWED_HOSTS = ['your-app.railway.app']
```

---

## 📊 성공 지표 (1주일 목표)

### 🎯 기술적 성공
- [x] Django 앱 배포 완료
- [x] 12문항 설문 작동
- [ ] 결과 페이지 정상 표시
- [ ] 모바일 반응형 100% 작동
- [ ] 버그 없이 10명 테스트 완료

### 🎬 콘텐츠 성공
- [ ] 유튜브 영상 1개 제작
- [ ] 조회수 1,000회 이상
- [ ] 댓글 50개 이상
- [ ] 공유 100회 이상

### 📈 비즈니스 검증
- [ ] 설문 참여자 100명 이상
- [ ] 결과 공유율 30% 이상
- [ ] 재방문율 20% 이상
- [ ] 피드백 수집 20건 이상

---

## 🚨 핵심 리스크 & 대응책

### ⚠️ 주요 리스크
1. **1주일 시간 부족** → 기능 우선순위 설정
2. **12문항 복잡도** → 단계별 구현
3. **Django 개발 시간** → 템플릿 활용
4. **배포 이슈** → Railway 자동 배포

### ✅ 대응 전략
1. **기능 우선순위**: 핵심 기능만 구현
2. **단계별 구현**: Day별 명확한 목표
3. **템플릿 활용**: Bootstrap, Chart.js
4. **자동 배포**: Railway CI/CD

---

## 🎬 유튜브 콘텐츠 전략

### 📺 영상 구성 (7-10분)
1. **오프닝** (1분): "나에게 맞는 부산 집은?"
2. **설문 소개** (2분): 12문항 간단 설명
3. **실제 테스트** (3분): 진행 과정 보여주기
4. **결과 공개** (3분): 매칭 결과 시각화
5. **마무리** (1분): 댓글로 결과 공유 유도

### 🎯 바이럴 포인트
- **"너도 해봐! 나는 '해안가 라이프스타일형'이래"**
- **결과 공유** → 친구 유입 → 네트워크 효과
- **부산 지역민** 타겟팅 → 지역 커뮤니티 반응

---

## 🎯 핵심 성공 요인

### 1. **시간 관리** (가장 중요)
- Day별 명확한 목표 설정
- 기능 우선순위 명확화
- 완벽보다 완성 우선

### 2. **Django 최적화**
- 템플릿 활용으로 개발 시간 단축
- Railway 자동 배포로 배포 시간 절약
- 모바일 우선 반응형 디자인

### 3. **12문항 설문 완전 활용**
- 기존 프레임워크 100% 반영
- 복잡한 매칭 알고리즘 구현
- 정확한 결과 제공

### 4. **유튜브 친화적 디자인**
- 시각적 임팩트 있는 결과
- 공유하기 쉬운 형태
- 재미있는 요소 강화

---

## 📅 상세 실행 일정

### **Day 1 (월)**: 프로젝트 설정
- [x] Django 프로젝트 생성
- [x] 가상환경 설정
- [x] requirements.txt 작성
- [x] 기본 앱 구조 생성 (survey, results, properties)
- [x] 데이터베이스 모델 설계
- [ ] Railway 프로젝트 생성

### **Day 2 (화)**: 설문 시스템
- [x] Survey, SurveyAnswer 모델 구현
- [x] 12문항 설문 폼 생성
- [x] 설문 진행률 표시 기능
- [x] 설문 결과 저장 로직
- [x] 기본 검증 및 에러 처리
- [x] 설문 템플릿 작성

### **Day 3 (수)**: 결과 시스템
- [x] SurveyResult 모델 구현
- [x] PersonaType 모델 구현 및 데이터 생성
- [x] 매칭 알고리즘 구현
- [x] 6개 부산 페르소나별 결과 로직
- [x] 결과 페이지 템플릿
- [x] Chart.js 레이더 차트 연동
- [x] 결과 공유 기능
- [x] 매칭 이유와 추천 지역 일치성 개선

### **Day 4 (목)**: 매물 시스템 & UI (완료 ✅)
- [x] Property 모델 구현
- [x] 부산 매물 데이터 입력 (관리 명령어로 6개 샘플 데이터 생성)
- [x] 매물 목록/상세 페이지
- [x] 매물 필터링 기능 (지역, 페르소나, 검색)
- [x] 매물 문의 페이지
- [x] Bootstrap 5 CSS 적용
- [x] Light Bootstrap Dashboard 적용
- [x] 부산 테마 커스텀 CSS 생성
- [x] 히어로 섹션 배경 이미지 슬라이더 (Crossfade + Zoom Out 효과)
- [x] 홈페이지, 설문, 결과 페이지 디자인 업그레이드
- [x] 모바일 반응형 디자인

### **Day 5 (금)**: 통합 테스트 & 버그 수정
- [ ] 전체 흐름 테스트
- [x] 버그 수정
  - [x] Q4 다중 선택 체크박스 선택 안되는 문제 해결
  - [x] 매칭 이유와 추천 지역 불일치 문제 해결 (모던_미니멀형)
  - [x] 설문 옵션 전체 영역 클릭 가능하도록 개선
- [x] UI/UX 개선
  - [x] 주요 버튼 텍스트 흰색으로 가독성 개선
  - [x] 설문 답변 텍스트 크기 및 색상 개선
  - [x] SNS 공유 버튼 색상 개선 (페이스북, X)
- [ ] 성능 최적화
- [ ] 베타 테스트 5명 진행
- [ ] 피드백 수집 및 개선
- [ ] 최종 점검

### **Day 6 (토)**: 배포 & 유튜브
- [x] Railway 배포 준비 완료
  - [x] requirements.txt 생성 (Django, gunicorn, psycopg2-binary, whitenoise, dj-database-url)
  - [x] Procfile 생성 (gunicorn 설정)
  - [x] runtime.txt 생성 (Python 3.13.5)
  - [x] settings.py 프로덕션 설정 (환경변수, PostgreSQL, WhiteNoise, 보안 설정)
  - [x] .gitignore 업데이트 (staticfiles 추가)
  - [x] RAILWAY_DEPLOYMENT.md 배포 가이드 작성
- [ ] Railway 배포 실행
- [ ] 도메인 연결
- [ ] SSL 인증서 설정
- [ ] 유튜브 영상 촬영
- [ ] 편집 & 업로드
- [ ] 썸네일 제작

### **Day 7 (일)**: 런칭 & 홍보
- [ ] 서비스 공식 런칭
- [ ] SNS 홍보 (인스타그램, 카카오톡)
- [ ] 커뮤니티 공유
- [ ] 피드백 수집
- [ ] 개선 계획 수립
- [ ] Phase 1.5 계획 수립

---

## 🎓 결론

이 **Django 기반 1주일 MVP**는 기존 요구사항을 모두 반영하면서도 **실현 가능한 범위**로 설계되었습니다.

**핵심 전략**:
1. **12문항 설문** → 기존 프레임워크 완전 활용
2. **Django 개발** → 템플릿 활용으로 시간 단축
3. **Railway 배포** → 자동 배포로 배포 시간 절약
4. **부산 집중** → 지역 특화
5. **유튜브 최적화** → 시각적, 공유 가능

**성공 기준**:
- 1주일 내 Django 앱 배포 완료
- 12문항 설문 정상 작동
- 유튜브 영상 1개 제작
- 설문 참여자 100명 이상

이 MVP를 통해 **기술적 완성도**와 **콘텐츠 제작**을 동시에 달성할 수 있습니다! 🚀

---

## 📚 참고 자료

- [Django 공식 문서](https://docs.djangoproject.com/)
- [Railway 배포 가이드](https://docs.railway.app/)
- [Bootstrap CSS 프레임워크](https://getbootstrap.com/)
- [Chart.js 차트 라이브러리](https://www.chartjs.org/)
- [부산 부동산 정보](https://www.land.molit.go.kr/)

---

## 🔄 다음 단계 (Phase 1.5)

### 📈 확장 계획
1. **구독 모델** 추가
2. **커미션 시스템** 구현
3. **CRM 연동** (Airtable, Zapier)
4. **고급 필터링** 기능
5. **지도 뷰** 연동

### 🎯 성장 지표
- 월 활성 사용자 500명
- 구독 전환율 15%
- 커미션 성사 월 3건
- 고객 만족도 4.5/5.0

---

**작성일**: 2025년 1월
**버전**: v1.1
**상태**: Day 1-4 완료 (100%), Day 5 진행 중 (버그 수정 및 UI 개선 완료), Day 6 배포 준비 완료
