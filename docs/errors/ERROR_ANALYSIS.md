# 에러 분석: ModuleNotFoundError: No module named 'django'

## 🔴 에러 메시지

```
ModuleNotFoundError: No module named 'django'

ImportError: Couldn't import Django. Are you sure it's installed and available 
in your PYTHONPATH environment variable? Did you forget to activate a virtual environment?
```

## 📋 에러 원인 분석

### 원인 1: 가상환경 미활성화 (가장 가능성 높음)

**문제 상황**:
- 로컬 환경에서 `python manage.py migrate`를 실행
- 가상환경(`venv`)이 활성화되지 않음
- 시스템 Python을 사용하여 Django가 설치되지 않은 환경

**확인 방법**:
```bash
# 가상환경 활성화 여부 확인
echo $VIRTUAL_ENV
# 출력이 비어있으면 가상환경이 활성화되지 않음

# Python 경로 확인
which python
# /usr/bin/python 또는 /opt/homebrew/bin/python3 → 시스템 Python
# /Users/jisungs/Documents/dev/sideprojects/find_my_home/venv/bin/python → 가상환경 Python
```

### 원인 2: Railway CLI의 `railway run` 명령어 문제

**문제 상황**:
- `railway run python manage.py migrate`를 실행
- Railway CLI가 로컬 환경에서 실행하면서 로컬 Python 사용
- 로컬 가상환경이 활성화되지 않아 Django를 찾을 수 없음

**Railway CLI의 동작 방식**:
- `railway run`은 로컬 환경에서 Railway 환경 변수를 주입하여 실행
- 원격 Railway 서버에서 실행하는 것이 아님
- 따라서 로컬에 Django가 설치되어 있어야 함

### 원인 3: Django 미설치

**문제 상황**:
- 가상환경은 활성화되었지만 Django가 설치되지 않음
- `requirements.txt`의 패키지가 설치되지 않음

**확인 방법**:
```bash
# 가상환경 활성화 후
source venv/bin/activate

# Django 설치 확인
python -c "import django; print(django.get_version())"
# ModuleNotFoundError가 발생하면 Django가 설치되지 않음
```

---

## ✅ 해결 방법

### 해결 방법 1: 가상환경 활성화 후 실행 (로컬 개발용)

**로컬에서 Django 관리 명령어를 실행하려면**:

```bash
# 1. 가상환경 활성화
cd /Users/jisungs/Documents/dev/sideprojects/find_my_home
source venv/bin/activate

# 2. Django 설치 확인
python -c "import django; print('Django:', django.get_version())"

# 3. 명령어 실행 (로컬 SQLite 사용)
python manage.py migrate
```

**⚠️ 주의**: 로컬에서 실행하면 로컬 SQLite 데이터베이스를 사용합니다. Railway의 PostgreSQL 데이터베이스와는 별개입니다.

### 해결 방법 2: Railway 웹 대시보드 터미널 사용 (권장)

**Railway 배포 마무리 작업을 하려면**:

1. Railway 대시보드 접속
   - https://railway.app
   - `renewed-tranquility` 프로젝트 → `web` 서비스 선택

2. 터미널 열기
   - "Deployments" 탭 → 최신 배포 선택
   - "View Logs" → "Shell" 탭

3. 명령어 실행 (Railway 원격 환경에서)
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py create_survey_questions
   python manage.py create_persona_types
   python manage.py create_sample_properties
   ```

**장점**:
- Railway의 원격 환경에서 실행 (모든 패키지 설치됨)
- PostgreSQL 데이터베이스에 직접 연결
- 실제 배포 환경과 동일한 조건

### 해결 방법 3: Railway CLI 환경 변수 주입 후 로컬 실행

**로컬에서 Railway 환경 변수를 사용하려면**:

```bash
# 1. 가상환경 활성화
source venv/bin/activate

# 2. Railway 환경 변수 주입하여 실행
railway run python manage.py migrate
```

**⚠️ 문제점**:
- 로컬에 `psycopg2-binary`가 설치되어 있어야 함 (Python 3.13 호환성 문제)
- 로컬 SQLite 대신 Railway PostgreSQL 사용 시도

---

## 🔍 상황별 대응 방법

### 상황 1: 로컬 개발/테스트를 하려는 경우

```bash
# 가상환경 활성화
source venv/bin/activate

# 로컬 SQLite 사용 (DATABASE_URL 없음)
python manage.py migrate
python manage.py runserver
```

### 상황 2: Railway 배포 마무리를 하려는 경우

**Railway 웹 대시보드 터미널 사용** (가장 확실한 방법)

### 상황 3: Railway 환경 변수를 로컬에서 테스트하려는 경우

```bash
# 가상환경 활성화
source venv/bin/activate

# Django 설치 확인
pip install -r requirements.txt

# Railway 환경 변수 주입하여 실행
railway run python manage.py migrate
```

**⚠️ 주의**: `psycopg2-binary`가 Python 3.13에서 설치되지 않을 수 있습니다.

---

## 📊 에러 발생 시나리오

### 시나리오 1: 가상환경 미활성화

```bash
# ❌ 잘못된 방법
python manage.py migrate
# ModuleNotFoundError: No module named 'django'

# ✅ 올바른 방법
source venv/bin/activate
python manage.py migrate
```

### 시나리오 2: Railway CLI 사용 시

```bash
# ❌ 잘못된 방법 (가상환경 미활성화)
railway run python manage.py migrate
# ModuleNotFoundError: No module named 'django'

# ✅ 올바른 방법 1: 가상환경 활성화 후
source venv/bin/activate
railway run python manage.py migrate

# ✅ 올바른 방법 2: Railway 웹 대시보드 터미널 사용 (권장)
```

---

## 🎯 결론

### 현재 에러의 원인

**가장 가능성 높은 원인**: 가상환경이 활성화되지 않은 상태에서 명령어 실행

### 해결 방법

1. **로컬 개발/테스트**: 가상환경 활성화 후 실행
2. **Railway 배포 마무리**: Railway 웹 대시보드 터미널 사용 (권장)

### 권장 사항

Railway 배포 마무리 작업은 **Railway 웹 대시보드 터미널**을 사용하는 것이 가장 확실합니다:
- 모든 패키지가 설치되어 있음
- PostgreSQL 데이터베이스에 직접 연결
- 실제 배포 환경과 동일

---

**마지막 업데이트**: 2025년 1월

