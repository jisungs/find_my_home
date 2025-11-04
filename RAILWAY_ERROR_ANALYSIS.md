# Railway 배포 에러 분석 및 해결 방법

## 🔴 에러 메시지

```
install apt packages: libpq5
ERROR: failed to build: failed to solve: secret POSTGRES_PASSWORD: not found
```

## 📋 문제 원인 분석

### 1. **에러 발생 시점**
- **빌드 단계**에서 발생
- PostgreSQL 클라이언트 라이브러리(`libpq5`) 설치 중
- Railway의 Railpack 시스템이 PostgreSQL 관련 패키지를 설치하려고 시도

### 2. **근본 원인**

Railway가 다음을 감지하고 자동으로 PostgreSQL 설정을 시도한 것으로 보입니다:

1. **`requirements.txt`에 `psycopg2-binary` 포함**
   - Railway가 PostgreSQL이 필요하다고 판단
   - 빌드 단계에서 PostgreSQL 관련 패키지 설치 시도

2. **PostgreSQL 서비스 미생성 또는 미연결**
   - Railway 대시보드에서 PostgreSQL 서비스를 추가하지 않았거나
   - 웹 서비스와 PostgreSQL 서비스가 연결되지 않았을 가능성

3. **서비스 순서 문제**
   - PostgreSQL 서비스가 생성되기 전에 웹 서비스 빌드가 시도됨
   - 빌드 단계에서 PostgreSQL 비밀번호를 찾지 못함

### 3. **왜 빌드 단계에서 비밀번호가 필요한가?**

일반적으로 빌드 단계에서는 PostgreSQL 비밀번호가 필요 없습니다. 하지만 Railway의 Railpack 시스템이:
- PostgreSQL 클라이언트 라이브러리 설치 시
- 서비스 간 연결을 미리 설정하려고 시도
- 이 과정에서 `POSTGRES_PASSWORD` secret을 찾으려고 함

## ✅ 해결 방법

### 방법 1: PostgreSQL 서비스 먼저 생성 (권장)

**단계별 절차:**

1. **Railway 대시보드에서 PostgreSQL 서비스 추가**
   ```
   Railway 대시보드 → 프로젝트 선택 → "+ New" → "Database" → "Add PostgreSQL"
   ```

2. **PostgreSQL 서비스가 완전히 생성될 때까지 대기**
   - 초록색 상태가 될 때까지 (약 1-2분)
   - `DATABASE_URL` 환경 변수가 자동으로 설정됨

3. **웹 서비스 배포**
   - GitHub 저장소 연결 또는 수동 배포
   - PostgreSQL 서비스와 같은 프로젝트에 있어야 함

4. **서비스 연결 확인**
   - Railway 대시보드에서 두 서비스가 같은 프로젝트에 있는지 확인
   - 웹 서비스가 PostgreSQL 서비스를 참조하는지 확인

### 방법 2: PostgreSQL 없이 먼저 배포 (테스트용)

**임시 해결책:**

1. **`requirements.txt`에서 `psycopg2-binary` 제거 (임시)**
   ```txt
   Django==5.2.7
   asgiref==3.10.0
   sqlparse==0.5.3
   gunicorn==21.2.0
   # psycopg2-binary==2.9.9  # 임시로 주석 처리
   whitenoise==6.6.0
   dj-database-url==2.1.0
   ```

2. **SQLite로 먼저 배포 테스트**
   - 배포가 성공하면 PostgreSQL 서비스 추가
   - 다시 `psycopg2-binary` 추가

3. **PostgreSQL 서비스 추가 후**
   - `requirements.txt`에서 주석 제거
   - 재배포

**⚠️ 주의**: 이 방법은 테스트용이며, 프로덕션에서는 PostgreSQL을 사용해야 합니다.

### 방법 3: Railway 설정 파일 생성 (명시적 설정)

**`railway.json` 파일 생성:**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

이 파일을 프로젝트 루트에 생성하면 Railway가 명시적으로 설정을 따릅니다.

### 방법 4: 환경 변수 명시적 설정

**Railway 대시보드에서:**

1. 웹 서비스 선택
2. "Variables" 탭
3. PostgreSQL 서비스의 `DATABASE_URL`이 자동으로 설정되어 있는지 확인
4. 없다면 PostgreSQL 서비스 → "Connect" → `DATABASE_URL` 복사 후 웹 서비스에 추가

## 🔍 확인 사항 체크리스트

배포 전 다음을 확인하세요:

- [ ] PostgreSQL 서비스가 Railway 프로젝트에 생성되어 있음
- [ ] PostgreSQL 서비스 상태가 "Running" (초록색)
- [ ] 웹 서비스와 PostgreSQL 서비스가 같은 프로젝트에 있음
- [ ] `DATABASE_URL` 환경 변수가 자동으로 설정됨
- [ ] `requirements.txt`에 `psycopg2-binary`가 포함되어 있음
- [ ] `dj-database-url` 패키지가 설치되어 있음

## 🚀 권장 배포 순서

### 1단계: PostgreSQL 서비스 생성
```
Railway 대시보드 → 프로젝트 → "+ New" → "Database" → "Add PostgreSQL"
```

### 2단계: 환경 변수 설정
```
웹 서비스 → "Variables" 탭
- SECRET_KEY: 생성된 키 입력
- DEBUG: False
- ALLOWED_HOSTS: your-app-name.railway.app,*.railway.app
- DATABASE_URL: (자동 설정됨, 확인만)
```

### 3단계: GitHub 저장소 연결 및 배포
```
Railway 대시보드 → 프로젝트 → "+ New" → "GitHub Repo"
→ 저장소 선택 → 자동 배포 시작
```

### 4단계: 배포 후 작업
```bash
# Railway 터미널에서
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_survey_questions
python manage.py create_persona_types
python manage.py create_sample_properties
```

## 📝 추가 참고사항

### Railway의 자동 감지 기능

Railway는 다음을 자동으로 감지합니다:
- `requirements.txt` → Python 패키지 설치
- `Procfile` → 시작 명령어
- `runtime.txt` → Python 버전
- `psycopg2-binary` → PostgreSQL 필요성 감지

### PostgreSQL 서비스 연결

PostgreSQL 서비스를 추가하면:
- `DATABASE_URL` 환경 변수가 자동으로 설정됨
- 다른 서비스에서 이 환경 변수를 참조할 수 있음
- 웹 서비스가 PostgreSQL 서비스와 연결됨

### 서비스 순서

Railway는 서비스 간 의존성을 자동으로 감지하지만, 때로는:
1. PostgreSQL 서비스를 먼저 생성
2. 그 다음 웹 서비스 배포

이 순서를 따르는 것이 안전합니다.

## 🆘 문제가 계속되면

1. **Railway 로그 확인**
   - Railway 대시보드 → "View Logs"
   - 상세 에러 메시지 확인

2. **서비스 재생성**
   - PostgreSQL 서비스 삭제 후 재생성
   - 웹 서비스 재배포

3. **Railway 지원팀 문의**
   - Railway Discord 또는 이메일 지원

---

**마지막 업데이트**: 2025년 1월

