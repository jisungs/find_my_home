# Railway migrate 에러 분석

## 🔴 에러 메시지

```
ModuleNotFoundError: No module named 'psycopg2'
django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 or psycopg module
```

## 📋 에러 원인 분석

### 핵심 문제

**`railway run`이 로컬 환경에서 실행되면서 Railway 환경 변수(`DATABASE_URL`)를 주입하여 PostgreSQL을 사용하려고 하지만, 로컬에 `psycopg2-binary`가 설치되어 있지 않음**

### 상세 원인 분석

1. **Railway CLI의 동작 방식**
   - `railway run`은 원격 서버에서 실행하는 것이 아님
   - 로컬 환경에서 Railway 환경 변수를 주입하여 실행
   - 따라서 로컬 Python 환경과 패키지가 사용됨

2. **환경 변수 주입**
   ```bash
   railway run env | grep DATABASE_URL
   # 출력: DATABASE_URL=postgresql://postgres:...@postgres.railway.internal:5432/railway
   ```
   - Railway의 `DATABASE_URL` 환경 변수가 로컬에 주입됨
   - Django가 `DATABASE_URL`을 감지하여 PostgreSQL 백엔드 사용 시도

3. **Django 설정 파일 동작**
   ```python
   # config/settings.py
   DATABASE_URL = os.environ.get('DATABASE_URL')
   
   if DATABASE_URL and dj_database_url:
       # PostgreSQL 설정 (Railway 배포 시)
       DATABASES = {
           'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
       }
   ```
   - `DATABASE_URL`이 있으면 PostgreSQL 사용
   - PostgreSQL 백엔드를 로드하려면 `psycopg2` 필요

4. **로컬 환경 문제**
   - 로컬 가상환경에 `psycopg2-binary`가 설치되지 않음
   - Python 3.13 호환성 문제로 설치 실패
   - 따라서 `psycopg2` 모듈을 찾을 수 없음

### 에러 발생 흐름

```
railway run python manage.py migrate
  ↓
Railway 환경 변수 주입 (DATABASE_URL 포함)
  ↓
Django가 DATABASE_URL 감지
  ↓
PostgreSQL 백엔드 사용 결정
  ↓
psycopg2 모듈 로드 시도
  ↓
ModuleNotFoundError: No module named 'psycopg2'
  ↓
ImproperlyConfigured 에러 발생
```

---

## ✅ 해결 방법

### 방법 1: Railway 웹 대시보드 터미널 사용 (가장 권장)

**Railway 배포 환경에서는 이미 모든 패키지가 설치되어 있습니다.**

1. Railway 대시보드 접속
   - https://railway.app
   - `renewed-tranquility` 프로젝트 → `web` 서비스

2. 터미널 열기
   - "Deployments" → 최신 배포 선택
   - "View Logs" → "Shell" 탭 선택

3. 명령어 실행 (Railway 원격 환경에서)
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py create_survey_questions
   python manage.py create_persona_types
   python manage.py create_sample_properties
   ```

**장점**:
- Railway 배포 환경에서 실행 (모든 패키지 설치됨)
- PostgreSQL 데이터베이스에 직접 연결
- 실제 배포 환경과 동일한 조건

### 방법 2: 로컬에서 DATABASE_URL 제거 후 SQLite 사용

**로컬 개발/테스트용**

```bash
# Railway 환경 변수 없이 실행
unset DATABASE_URL
python manage.py migrate

# 또는 SQLite 명시적 사용
DATABASE_URL="" python manage.py migrate
```

**⚠️ 주의**: 이 방법은 로컬 SQLite 데이터베이스를 사용합니다. Railway PostgreSQL과는 별개입니다.

### 방법 3: settings.py 수정 (임시 해결책)

**로컬에서만 SQLite 강제 사용**

```python
# config/settings.py
import os

# Railway 환경 확인
RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT')

# Railway 환경이 아니면 SQLite 사용
if not RAILWAY_ENVIRONMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Railway 환경: PostgreSQL 사용
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and dj_database_url:
        DATABASES = {
            'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
        }
```

**⚠️ 주의**: 이 방법은 코드 수정이 필요하며, Railway 배포 환경에서는 정상 작동합니다.

---

## 🔍 문제 진단

### 확인 사항

1. **Railway 환경 변수 확인**
   ```bash
   railway run env | grep DATABASE_URL
   ```
   - `DATABASE_URL`이 설정되어 있으면 PostgreSQL 사용 시도

2. **로컬 패키지 확인**
   ```bash
   source venv/bin/activate
   python -c "import psycopg2; print('OK')" 2>&1
   ```
   - `ModuleNotFoundError`가 발생하면 `psycopg2` 미설치

3. **Django 설정 확인**
   ```python
   # settings.py에서 DATABASE_URL 처리 로직 확인
   ```

---

## 📊 상황별 대응 방법

### 상황 1: Railway 배포 마무리 작업

**권장**: Railway 웹 대시보드 터미널 사용

이유:
- Railway 배포 환경에서 실행
- 모든 패키지가 설치되어 있음
- PostgreSQL 데이터베이스에 직접 연결

### 상황 2: 로컬 개발/테스트

**권장**: SQLite 사용 (DATABASE_URL 없이)

```bash
# Railway 환경 변수 제거
unset DATABASE_URL

# 로컬 SQLite 사용
python manage.py migrate
python manage.py runserver
```

### 상황 3: Railway CLI로 원격 명령 실행

**문제**: `railway run`이 로컬에서 실행되면서 문제 발생

**해결**: Railway 웹 대시보드 터미널 사용 (방법 1)

---

## 🎯 결론

### 현재 에러의 원인

**`railway run`이 로컬 환경에서 Railway 환경 변수를 주입하여 PostgreSQL을 사용하려고 하지만, 로컬에 `psycopg2-binary`가 설치되지 않음**

### 해결 방법

1. **Railway 배포 마무리**: Railway 웹 대시보드 터미널 사용 (가장 권장)
2. **로컬 개발**: DATABASE_URL 제거 후 SQLite 사용

### 중요 사항

**Railway CLI의 `railway run`은 원격 서버에서 실행하는 것이 아닙니다!**
- 로컬 환경에서 Railway 환경 변수를 주입하여 실행
- 따라서 로컬 Python 환경과 패키지가 사용됨
- Railway 배포 환경에서 실행하려면 웹 대시보드 터미널 사용

---

## 📚 참고 자료

- [Railway CLI 문서](https://docs.railway.app/develop/cli)
- [Railway 대시보드](https://railway.app)
- [Django 데이터베이스 설정](https://docs.djangoproject.com/en/stable/ref/settings/#databases)

---

**마지막 업데이트**: 2025년 1월

