# Railway 배포 마무리 가이드 (Railway CLI 사용)

이 문서는 Railway CLI를 사용하여 Django 프로젝트 배포를 마무리하는 방법을 안내합니다.

---

## 📋 배포 마무리 작업 목록

배포 후 다음 작업들을 순서대로 실행해야 합니다:

1. ✅ 마이그레이션 실행
2. ✅ 정적 파일 수집
3. ✅ 초기 데이터 생성 (설문 문항, 페르소나, 샘플 매물)
4. ✅ 슈퍼유저 생성 (선택사항)

---

## 🚀 Railway CLI 사용 방법

### 1. Railway CLI 설치 확인

```bash
# Railway CLI 버전 확인
railway --version

# Railway 로그인 (이미 완료됨)
railway login

# 프로젝트 연결 (이미 완료됨)
railway link
```

### 2. Railway 환경에서 명령 실행

Railway CLI를 사용하면 **Railway의 원격 환경**에서 명령을 실행할 수 있습니다.

**중요**: `railway run` 명령은 로컬 환경이 아니라 **Railway의 원격 서버**에서 실행됩니다.

---

## 📝 배포 마무리 명령어 (순서대로 실행)

### Step 1: 마이그레이션 실행

```bash
railway run python manage.py migrate
```

**설명**: 데이터베이스 스키마를 생성합니다.

**예상 출력**:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, survey, results, property
Running migrations:
  ...
```

### Step 2: 정적 파일 수집

```bash
railway run python manage.py collectstatic --noinput
```

**설명**: 정적 파일(CSS, JS, 이미지)을 `staticfiles` 디렉토리에 수집합니다.

**예상 출력**:
```
Copying '/app/static/...'
...
X static files copied to '/app/staticfiles'.
```

### Step 3: 초기 데이터 생성

#### 3-1. 설문 문항 생성

```bash
railway run python manage.py create_survey_questions
```

**설명**: 12개의 설문 문항을 생성합니다.

#### 3-2. 페르소나 타입 생성

```bash
railway run python manage.py create_persona_types
```

**설명**: 6개의 페르소나 타입을 생성합니다.

#### 3-3. 샘플 매물 데이터 생성 (선택사항)

```bash
railway run python manage.py create_sample_properties
```

**설명**: 테스트용 샘플 매물 데이터를 생성합니다.

### Step 4: 슈퍼유저 생성 (선택사항)

```bash
railway run python manage.py createsuperuser
```

**설명**: Django 관리자 페이지 접근용 슈퍼유저를 생성합니다.

**입력 항목**:
- Username
- Email address
- Password (입력 시 보이지 않음)
- Password (again)

---

## 🔍 명령어 실행 확인

### Railway 로그 확인

명령어 실행 결과를 확인하려면:

```bash
# Railway 대시보드에서 확인
# 또는 Railway CLI로 로그 확인
railway logs
```

### 배포 상태 확인

```bash
# 현재 연결된 프로젝트 확인
railway status

# 서비스 목록 확인
railway service
```

---

## 🚨 문제 해결

### 문제 1: "ModuleNotFoundError: No module named 'django'"

**원인**: 로컬에서 `python manage.py`를 실행한 경우

**해결**: `railway run`을 사용하여 Railway 환경에서 실행해야 합니다.

```bash
# ❌ 잘못된 방법 (로컬 실행)
python manage.py migrate

# ✅ 올바른 방법 (Railway 원격 실행)
railway run python manage.py migrate
```

### 문제 2: "No service found"

**원인**: 프로젝트가 연결되지 않았거나 서비스가 선택되지 않음

**해결**:
```bash
# 프로젝트 다시 연결
railway link

# 서비스 선택
# 대화형 메뉴에서 "web" 서비스 선택
```

### 문제 3: 마이그레이션 오류

**원인**: 데이터베이스 연결 문제 또는 마이그레이션 파일 문제

**해결**:
```bash
# 마이그레이션 상태 확인
railway run python manage.py showmigrations

# 특정 마이그레이션만 실행
railway run python manage.py migrate <app_name> <migration_name>
```

### 문제 4: 정적 파일 수집 실패

**원인**: `STATIC_ROOT` 설정 문제 또는 권한 문제

**해결**:
```bash
# 설정 확인
railway run python manage.py collectstatic --noinput --dry-run

# 상세 로그와 함께 실행
railway run python manage.py collectstatic --noinput --verbosity 2
```

---

## 📋 전체 배포 마무리 스크립트

한 번에 모든 작업을 실행하려면:

```bash
# 1. 마이그레이션
railway run python manage.py migrate

# 2. 정적 파일 수집
railway run python manage.py collectstatic --noinput

# 3. 초기 데이터 생성
railway run python manage.py create_survey_questions
railway run python manage.py create_persona_types
railway run python manage.py create_sample_properties

# 4. 슈퍼유저 생성 (선택사항, 대화형)
railway run python manage.py createsuperuser
```

---

## ✅ 배포 완료 확인

배포가 완료되었는지 확인:

1. **웹사이트 접속**
   - Railway 대시보드에서 제공하는 도메인으로 접속
   - 예: `https://your-app-name.railway.app`

2. **설문 시작 페이지 확인**
   - 홈페이지가 정상적으로 로드되는지 확인
   - 설문 시작 버튼이 작동하는지 확인

3. **관리자 페이지 확인**
   - `/admin` 경로로 접속
   - 슈퍼유저로 로그인 가능한지 확인

4. **데이터 확인**
   - 관리자 페이지에서 설문 문항이 생성되었는지 확인
   - 페르소나 타입이 생성되었는지 확인

---

## 🎯 다음 단계

배포 마무리가 완료되면:

1. **기능 테스트**
   - 설문 시작 → 진행 → 완료 플로우 테스트
   - 결과 페이지 확인
   - 매물 목록 확인

2. **성능 확인**
   - 페이지 로딩 속도 확인
   - 정적 파일이 제대로 로드되는지 확인

3. **모니터링 설정**
   - Railway 대시보드에서 로그 모니터링
   - 에러 발생 시 알림 설정

---

## 📚 참고 자료

- [Railway CLI 문서](https://docs.railway.app/develop/cli)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

**마지막 업데이트**: 2025년 1월

