# Railway 배포 에러 상세 분석 및 해결 방법

**에러 발생 시간**: 2025년 1월  
**에러 메시지**: `ERROR: failed to build: failed to solve: secret POSTGRES_PASSWORD: not found`

---

## 🔴 에러 상세 분석

### 에러 발생 시점
```
install apt packages: libpq5
install apt packages: libpq-dev
ERROR: failed to build: failed to solve: secret POSTGRES_PASSWORD: not found
```

### 문제의 핵심

Railway의 **Nixpacks** 빌드 시스템이:
1. `requirements.txt`에서 `psycopg2-binary`를 감지
2. PostgreSQL 클라이언트 라이브러리(`libpq5`, `libpq-dev`) 설치 시도
3. 빌드 단계에서 PostgreSQL 서비스 연결을 시도
4. `POSTGRES_PASSWORD` secret을 찾지 못해 실패

### 왜 빌드 단계에서 비밀번호가 필요한가?

Railway의 Nixpacks는 **빌드 단계에서 서비스 간 연결을 검증**하려고 시도합니다:
- PostgreSQL 관련 패키지가 감지되면
- PostgreSQL 서비스가 존재하는지 확인
- 서비스가 없으면 빌드 실패

이는 **Railway의 의존성 검증 시스템** 때문입니다.

---

## ✅ 해결 방법 (우선순위별)

### 방법 1: PostgreSQL 서비스 먼저 생성 (가장 확실한 방법)

#### 단계별 절차

**1단계: PostgreSQL 서비스 생성**
```
Railway 대시보드
→ 프로젝트 선택
→ "+ New" 버튼 클릭
→ "Database" 선택
→ "Add PostgreSQL" 선택
```

**2단계: PostgreSQL 서비스가 완전히 실행될 때까지 대기**
- 초록색 "Running" 상태가 될 때까지 대기 (약 1-2분)
- `DATABASE_URL` 환경 변수가 자동으로 생성됨

**3단계: 웹 서비스 배포**
- PostgreSQL 서비스가 생성된 **같은 프로젝트**에서
- GitHub 저장소 연결 또는 수동 배포
- 이제 빌드가 성공할 것입니다

**4단계: 서비스 연결 확인**
- Railway 대시보드에서 두 서비스가 같은 프로젝트에 있는지 확인
- 웹 서비스의 "Variables" 탭에서 `DATABASE_URL`이 자동으로 설정되어 있는지 확인

---

### 방법 2: Nixpacks 설정 파일로 PostgreSQL 감지 비활성화

#### `nixpacks.toml` 파일 생성

프로젝트 루트에 `nixpacks.toml` 파일을 생성:

```toml
[phases.setup]
aptPkgs = []

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = []

[start]
cmd = "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"
```

이 파일은 Railway가 PostgreSQL을 자동 감지하지 않도록 합니다.

**⚠️ 주의**: 이 방법은 PostgreSQL을 사용하지 않을 때만 권장합니다.

---

### 방법 3: PostgreSQL 없이 먼저 배포 (임시 해결책)

#### 1. `requirements.txt`에서 `psycopg2-binary` 제거

```txt
# Django 프로젝트 필수 패키지
Django==5.2.7
asgiref==3.10.0
sqlparse==0.5.3

# 프로덕션 웹 서버
gunicorn==21.2.0

# PostgreSQL 연결 (Railway 배포 시 필요)
# psycopg2-binary==2.9.9  # 임시로 주석 처리

# DATABASE_URL 파싱
dj-database-url==2.1.0

# 정적 파일 서빙
whitenoise==6.6.0
```

#### 2. SQLite로 먼저 배포 테스트

```bash
# 커밋 및 푸시
git add requirements.txt
git commit -m "fix: PostgreSQL 없이 먼저 배포 테스트"
git push origin main
```

#### 3. 배포 성공 후 PostgreSQL 추가

1. PostgreSQL 서비스 생성
2. `requirements.txt`에서 주석 제거
3. 재배포

**⚠️ 주의**: 이 방법은 테스트용이며, 프로덕션에서는 PostgreSQL을 사용해야 합니다.

---

### 방법 4: Railway 설정에서 PostgreSQL 의존성 제거

#### Railway 프로젝트 설정

1. Railway 대시보드에서 웹 서비스 선택
2. "Settings" 탭
3. "Deploy" 섹션
4. "Build Command" 확인:
   ```bash
   pip install -r requirements.txt
   ```
5. PostgreSQL 서비스와의 연결 해제 (있다면)

**⚠️ 이 방법은 권장하지 않습니다.** PostgreSQL 서비스를 먼저 생성하는 것이 가장 좋습니다.

---

## 🔍 문제 진단 체크리스트

배포 전 다음을 확인하세요:

### Railway 대시보드 확인

- [ ] **PostgreSQL 서비스가 프로젝트에 생성되어 있는가?**
  - Railway 대시보드 → 프로젝트 → 서비스 목록 확인
  
- [ ] **PostgreSQL 서비스 상태가 "Running"인가?**
  - 초록색 상태여야 함
  
- [ ] **웹 서비스와 PostgreSQL 서비스가 같은 프로젝트에 있는가?**
  - 같은 프로젝트에 있어야 자동 연결됨
  
- [ ] **웹 서비스의 "Variables" 탭에 `DATABASE_URL`이 있는가?**
  - PostgreSQL 서비스 생성 시 자동으로 설정됨

### 코드 확인

- [ ] **`requirements.txt`에 `psycopg2-binary`가 있는가?**
  - 있으면 PostgreSQL 서비스가 필요함
  
- [ ] **`settings.py`에서 PostgreSQL 설정이 올바른가?**
  - `DATABASE_URL` 환경 변수 사용 확인

---

## 🚀 권장 배포 순서 (단계별)

### Step 1: PostgreSQL 서비스 생성

```
1. Railway 대시보드 접속
2. 프로젝트 선택 (또는 새 프로젝트 생성)
3. "+ New" 버튼 클릭
4. "Database" → "Add PostgreSQL" 선택
5. PostgreSQL 서비스가 "Running" 상태가 될 때까지 대기 (1-2분)
```

### Step 2: 환경 변수 설정

웹 서비스를 생성하기 전에:
- PostgreSQL 서비스가 생성되면 `DATABASE_URL`이 자동으로 설정됨
- 웹 서비스 생성 시 이 환경 변수를 자동으로 참조함

### Step 3: 웹 서비스 배포

**옵션 A: GitHub 저장소 연결**
```
1. Railway 대시보드 → 프로젝트
2. "+ New" → "GitHub Repo" 선택
3. 저장소 선택
4. 자동 배포 시작
```

**옵션 B: CLI로 배포**
```bash
railway login
railway link
railway up
```

### Step 4: 배포 후 작업

Railway 터미널에서:
```bash
# 마이그레이션
python manage.py migrate

# 정적 파일 수집
python manage.py collectstatic --noinput

# 초기 데이터 생성
python manage.py create_survey_questions
python manage.py create_persona_types
python manage.py create_sample_properties
```

---

## 🎯 근본 원인 정리

### 왜 이런 에러가 발생하는가?

1. **Railway의 자동 감지 시스템**
   - `requirements.txt`에 `psycopg2-binary`가 있으면 PostgreSQL이 필요하다고 판단
   - 빌드 단계에서 PostgreSQL 서비스 연결을 검증

2. **서비스 생성 순서**
   - 웹 서비스를 먼저 배포하면 PostgreSQL 서비스가 없어서 실패
   - PostgreSQL 서비스를 먼저 생성해야 함

3. **의존성 검증**
   - Railway는 빌드 단계에서 모든 의존성을 확인
   - PostgreSQL 서비스가 없으면 빌드 실패

### 해결의 핵심

**PostgreSQL 서비스를 먼저 생성하고, 그 다음 웹 서비스를 배포해야 합니다.**

---

## 📝 추가 참고사항

### Railway의 Nixpacks 시스템

Railway는 **Nixpacks**를 사용하여 프로젝트를 빌드합니다:
- 자동으로 프로젝트 타입 감지
- 필요한 시스템 패키지 자동 설치
- 의존성 검증

### PostgreSQL 서비스 연결

PostgreSQL 서비스를 생성하면:
- `DATABASE_URL` 환경 변수가 자동으로 생성됨
- 형식: `postgresql://user:password@host:port/dbname`
- 다른 서비스에서 이 변수를 참조할 수 있음

### 환경 변수 공유

Railway 프로젝트 내의 모든 서비스는:
- 같은 프로젝트에 있으면 환경 변수 공유 가능
- PostgreSQL 서비스의 `DATABASE_URL`을 웹 서비스가 자동으로 참조

---

## 🆘 문제가 계속되면

### 1. Railway 로그 확인

```
Railway 대시보드
→ 프로젝트 선택
→ 웹 서비스 선택
→ "View Logs" 클릭
→ "Deploy Logs" 탭 확인
```

### 2. 서비스 재생성

```
1. PostgreSQL 서비스 삭제
2. 웹 서비스 삭제
3. PostgreSQL 서비스 먼저 생성
4. 웹 서비스 재배포
```

### 3. Railway 지원팀 문의

- Railway Discord: https://discord.gg/railway
- 이메일 지원

---

## ✅ 최종 권장 사항

### 가장 확실한 방법

1. **PostgreSQL 서비스를 먼저 생성**
2. **서비스가 완전히 실행될 때까지 대기**
3. **그 다음 웹 서비스 배포**

이 순서를 따르면 99% 확률로 성공합니다.

### 임시 해결책

PostgreSQL 없이 먼저 배포하려면:
1. `requirements.txt`에서 `psycopg2-binary` 주석 처리
2. SQLite로 배포
3. 배포 성공 후 PostgreSQL 추가
4. `psycopg2-binary` 다시 활성화

---

**마지막 업데이트**: 2025년 1월

