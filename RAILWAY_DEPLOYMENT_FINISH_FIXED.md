# Railway 배포 마무리 가이드 (수정 버전)

## ⚠️ 문제 상황

`railway run` 명령어가 로컬 환경에서 실행되면서 PostgreSQL 연결을 시도하지만, 로컬에 `psycopg2-binary`가 설치되어 있지 않아 실패합니다.

## ✅ 해결 방법

Railway CLI의 `railway run`은 로컬 환경에서 Railway 환경 변수를 주입해서 실행합니다. 따라서 **Railway 웹 대시보드의 터미널**을 사용하는 것이 가장 확실합니다.

---

## 🚀 방법 1: Railway 웹 대시보드 터미널 사용 (권장)

### 1. Railway 대시보드 접속

1. https://railway.app 접속
2. 로그인
3. `renewed-tranquility` 프로젝트 선택
4. `web` 서비스 선택

### 2. 터미널 열기

1. 서비스 페이지에서 **"Deployments"** 탭 선택
2. 최신 배포 선택
3. **"View Logs"** 클릭
4. **"Shell"** 탭 선택 (또는 터미널 아이콘 클릭)

### 3. 명령어 실행

Railway의 원격 터미널에서 다음 명령어들을 순서대로 실행:

```bash
# 1. 마이그레이션 실행
python manage.py migrate

# 2. 정적 파일 수집
python manage.py collectstatic --noinput

# 3. 초기 데이터 생성
python manage.py create_survey_questions
python manage.py create_persona_types
python manage.py create_sample_properties

# 4. 슈퍼유저 생성 (선택사항, 대화형)
python manage.py createsuperuser
```

---

## 🚀 방법 2: Railway CLI - 원격 셸 접속 (대안)

Railway CLI로 원격 셸에 직접 접속할 수 있다면:

```bash
# 원격 셸 접속 (Railway CLI가 지원하는 경우)
railway shell

# 셸에서 명령어 실행
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_survey_questions
python manage.py create_persona_types
python manage.py create_sample_properties
python manage.py createsuperuser
```

---

## 📋 배포 마무리 명령어 (전체)

### Step 1: 마이그레이션 실행

```bash
python manage.py migrate
```

**예상 출력**:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, survey, results, property
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 2: 정적 파일 수집

```bash
python manage.py collectstatic --noinput
```

**예상 출력**:
```
Copying '/app/static/...'
...
X static files copied to '/app/staticfiles'.
```

### Step 3: 초기 데이터 생성

#### 3-1. 설문 문항 생성

```bash
python manage.py create_survey_questions
```

**예상 출력**:
```
설문 문항 생성 완료: 12개
```

#### 3-2. 페르소나 타입 생성

```bash
python manage.py create_persona_types
```

**예상 출력**:
```
페르소나 타입 생성 완료: 6개
```

#### 3-3. 샘플 매물 데이터 생성 (선택사항)

```bash
python manage.py create_sample_properties
```

**예상 출력**:
```
샘플 매물 데이터 생성 완료: X개
```

### Step 4: 슈퍼유저 생성 (선택사항)

```bash
python manage.py createsuperuser
```

**입력 항목**:
- Username: (관리자 이름 입력)
- Email address: (이메일 입력)
- Password: (비밀번호 입력, 화면에 표시되지 않음)
- Password (again): (비밀번호 재입력)

---

## ✅ 배포 완료 확인

### 1. 웹사이트 접속 테스트

Railway 대시보드에서 제공하는 도메인으로 접속:
- 예: `https://your-app-name.railway.app`

### 2. 주요 페이지 확인

- ✅ 홈페이지: `/`
- ✅ 설문 시작: `/survey/start/`
- ✅ 관리자 페이지: `/admin/` (슈퍼유저로 로그인)

### 3. 데이터 확인

관리자 페이지(`/admin/`)에서:
- ✅ 설문 문항이 12개 생성되었는지 확인
- ✅ 페르소나 타입이 6개 생성되었는지 확인
- ✅ 샘플 매물이 생성되었는지 확인 (선택사항)

---

## 🔍 문제 해결

### 문제: "ModuleNotFoundError: No module named 'psycopg2'"

**원인**: `railway run`이 로컬 환경에서 실행되면서 발생

**해결**: Railway 웹 대시보드의 터미널을 사용하세요. 이 방법은 Railway의 원격 환경에서 실행되므로 모든 패키지가 설치되어 있습니다.

### 문제: "No migrations to apply"

**원인**: 마이그레이션이 이미 적용됨

**해결**: 정상입니다. 다음 단계로 진행하세요.

### 문제: "collectstatic: command not found"

**원인**: Django가 설치되지 않음

**해결**: Railway 웹 대시보드 터미널을 사용하면 Django가 이미 설치되어 있습니다.

---

## 📚 참고 자료

- [Railway 대시보드](https://railway.app)
- [Railway CLI 문서](https://docs.railway.app/develop/cli)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

**마지막 업데이트**: 2025년 1월

