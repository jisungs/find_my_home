# Railway hostname 에러 분석

## 🔴 에러 메시지

```
psycopg2.OperationalError: could not translate host name "postgres.railway.internal" to address: 
nodename nor servname provided, or not known

django.db.utils.OperationalError: could not translate host name "postgres.railway.internal" to address
```

## 📋 에러 원인 분석

### 핵심 문제

**`railway run`이 로컬 환경에서 실행되면서 Railway의 내부 호스트명(`postgres.railway.internal`)에 접근하려고 하지만, 이 호스트는 Railway의 내부 네트워크에서만 접근 가능함**

### 상세 원인 분석

1. **Railway 내부 네트워크 호스트명**
   ```
   DATABASE_URL=postgresql://postgres:...@postgres.railway.internal:5432/railway
   ```
   - `postgres.railway.internal`은 Railway의 **내부 네트워크 호스트명**
   - Railway 서비스 간 통신에만 사용됨
   - 외부(로컬 환경)에서는 접근 불가능

2. **Railway CLI의 동작 방식**
   - `railway run`은 원격 서버에서 실행하는 것이 아님
   - 로컬 환경에서 Railway 환경 변수를 주입하여 실행
   - 로컬 네트워크에서 `postgres.railway.internal` 호스트를 찾을 수 없음

3. **DNS 해석 실패**
   - 로컬 환경에서 `postgres.railway.internal`을 DNS 조회
   - 이 호스트명은 Railway의 내부 DNS에만 존재
   - 로컬 DNS에서는 찾을 수 없어서 에러 발생

### 에러 발생 흐름

```
railway run python manage.py migrate
  ↓
Railway 환경 변수 주입 (DATABASE_URL 포함)
  ↓
DATABASE_URL = postgresql://...@postgres.railway.internal:5432/railway
  ↓
psycopg2가 PostgreSQL 연결 시도
  ↓
postgres.railway.internal 호스트명 DNS 조회
  ↓
로컬 DNS에서 호스트를 찾을 수 없음
  ↓
OperationalError: could not translate host name
```

### 이전 에러와의 차이점

**이전 에러**:
- `ModuleNotFoundError: No module named 'psycopg2'`
- `psycopg2`가 설치되지 않음

**현재 에러**:
- `psycopg2`는 설치됨 (에러 메시지에 `psycopg2/__init__.py` 나타남)
- 하지만 Railway 내부 호스트명에 접근할 수 없음

---

## ✅ 해결 방법

### 방법 1: Railway 웹 대시보드 터미널 사용 (가장 권장)

**Railway 배포 환경에서는 내부 네트워크를 통해 PostgreSQL에 접근할 수 있습니다.**

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
- Railway 내부 네트워크에서 실행
- `postgres.railway.internal` 호스트에 접근 가능
- PostgreSQL 데이터베이스에 직접 연결

### 방법 2: 로컬에서 DATABASE_URL 제거 후 SQLite 사용

**로컬 개발/테스트용**

```bash
# Railway 환경 변수 제거
unset DATABASE_URL

# 로컬 SQLite 사용
python manage.py migrate
python manage.py runserver
```

**⚠️ 주의**: 이 방법은 로컬 SQLite 데이터베이스를 사용합니다. Railway PostgreSQL과는 별개입니다.

### 방법 3: Railway CLI로 원격 셸 접속 (대안)

Railway CLI가 원격 셸 접속을 지원한다면:

```bash
# 원격 셸 접속 (Railway CLI가 지원하는 경우)
railway shell

# 셸에서 명령어 실행
python manage.py migrate
python manage.py collectstatic --noinput
```

**⚠️ 주의**: Railway CLI의 `shell` 명령어는 로컬 서브셸을 열어서 환경 변수만 주입하는 것이므로, 여전히 로컬에서 실행됩니다.

---

## 🔍 Railway 호스트명 설명

### Railway 내부 네트워크

Railway는 서비스 간 통신을 위해 내부 네트워크를 사용합니다:

- **내부 호스트명**: `postgres.railway.internal`
- **외부 접근**: 불가능 (Railway 내부 네트워크에서만 접근 가능)
- **용도**: Railway 서비스 간 통신

### Railway 외부 접근

만약 외부에서 PostgreSQL에 접근하려면:

- **공개 URL**: Railway 대시보드에서 제공하는 공개 URL 사용
- **포트 포워딩**: Railway CLI 또는 대시보드에서 설정
- **직접 연결**: Railway의 공개 엔드포인트 사용

---

## 📊 상황별 대응 방법

### 상황 1: Railway 배포 마무리 작업

**권장**: Railway 웹 대시보드 터미널 사용

이유:
- Railway 내부 네트워크에서 실행
- `postgres.railway.internal` 호스트에 접근 가능
- PostgreSQL 데이터베이스에 직접 연결

### 상황 2: 로컬 개발/테스트

**권장**: SQLite 사용 (DATABASE_URL 제거)

```bash
# Railway 환경 변수 제거
unset DATABASE_URL

# 로컬 SQLite 사용
python manage.py migrate
python manage.py runserver
```

### 상황 3: Railway CLI로 원격 명령 실행

**문제**: `railway run`이 로컬에서 실행되면서 내부 호스트명에 접근할 수 없음

**해결**: Railway 웹 대시보드 터미널 사용 (방법 1)

---

## 🎯 결론

### 현재 에러의 원인

**`railway run`이 로컬 환경에서 실행되면서 Railway의 내부 호스트명(`postgres.railway.internal`)에 접근하려고 하지만, 이 호스트는 Railway의 내부 네트워크에서만 접근 가능함**

### 해결 방법

1. **Railway 배포 마무리**: Railway 웹 대시보드 터미널 사용 (가장 권장)
2. **로컬 개발**: DATABASE_URL 제거 후 SQLite 사용

### 중요 사항

**Railway CLI의 `railway run`은 원격 서버에서 실행하는 것이 아닙니다!**
- 로컬 환경에서 Railway 환경 변수를 주입하여 실행
- 따라서 Railway 내부 네트워크 호스트명에 접근할 수 없음
- Railway 배포 환경에서 실행하려면 **웹 대시보드 터미널**을 사용해야 함

---

## 📚 참고 자료

- [Railway 내부 네트워크](https://docs.railway.app/develop/services)
- [Railway CLI 문서](https://docs.railway.app/develop/cli)
- [Railway 대시보드](https://railway.app)

---

**마지막 업데이트**: 2025년 1월

