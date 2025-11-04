# 환경 변수 설정 가이드

이 문서는 프로젝트의 환경 변수 설정 방법을 안내합니다.

## 📋 목차

1. [로컬 개발 환경 설정](#로컬-개발-환경-설정)
2. [Railway 배포 환경 설정](#railway-배포-환경-설정)
3. [환경 변수 목록](#환경-변수-목록)
4. [보안 주의사항](#보안-주의사항)

---

## 🖥️ 로컬 개발 환경 설정

### 1. .env 파일 생성

프로젝트 루트 디렉토리에 `.env` 파일이 이미 생성되어 있습니다.

만약 `.env` 파일이 없다면:

```bash
# .env.example 파일을 복사하여 생성
cp .env.example .env
```

### 2. SECRET_KEY 생성

`.env` 파일의 `SECRET_KEY`는 이미 새로 생성된 키로 설정되어 있습니다.

새로운 SECRET_KEY를 생성하려면:

```bash
# 가상환경 활성화 후
source venv/bin/activate

# SECRET_KEY 생성
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

생성된 키를 `.env` 파일의 `SECRET_KEY` 값으로 사용하세요.

### 3. 환경 변수 확인

`.env` 파일이 올바르게 설정되었는지 확인:

```bash
cat .env
```

기본 설정:
- `DEBUG=True` (로컬 개발)
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `DATABASE_URL=` (비어있으면 SQLite 사용)

---

## 🚀 Railway 배포 환경 설정

### 1. Railway 프로젝트 생성

1. [Railway](https://railway.app) 접속 및 로그인
2. "New Project" 클릭
3. GitHub 저장소 연결

### 2. PostgreSQL 데이터베이스 추가

1. Railway 대시보드에서 프로젝트 선택
2. "+ New" 버튼 클릭
3. "Database" → "Add PostgreSQL" 선택
4. PostgreSQL 인스턴스 생성 (자동으로 `DATABASE_URL` 환경 변수 설정됨)

### 3. 환경 변수 설정

Railway 대시보드의 **"Variables"** 탭에서 다음 환경 변수를 설정:

#### 필수 환경 변수

| 변수명 | 설명 | 예시 값 |
|--------|------|---------|
| `SECRET_KEY` | Django 시크릿 키 | `f5b9xp2)99vr(&b53ae9u8%@umj0b4_jp6y5+efou&tnykst$^` |
| `DEBUG` | 디버그 모드 | `False` (프로덕션) |
| `ALLOWED_HOSTS` | 허용된 호스트 | `your-app-name.railway.app,*.railway.app` |

**SECRET_KEY 생성 방법:**

```bash
# 로컬에서 실행
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

생성된 키를 Railway 환경 변수에 설정하세요.

#### 자동 설정되는 환경 변수

| 변수명 | 설명 | 설정 방법 |
|--------|------|-----------|
| `DATABASE_URL` | PostgreSQL 연결 URL | PostgreSQL 서비스 추가 시 자동 설정 |

### 4. 배포 후 작업

배포 완료 후 Railway 터미널에서 다음 명령 실행:

```bash
# 1. 마이그레이션 실행
python manage.py migrate

# 2. 정적 파일 수집
python manage.py collectstatic --noinput

# 3. 초기 데이터 생성
python manage.py create_survey_questions
python manage.py create_persona_types
python manage.py create_sample_properties

# 4. 슈퍼유저 생성 (선택사항)
python manage.py createsuperuser
```

---

## 📝 환경 변수 목록

### 필수 환경 변수

#### SECRET_KEY
- **설명**: Django 보안을 위한 시크릿 키
- **로컬**: `.env` 파일에 설정
- **Railway**: Variables 탭에서 설정
- **생성**: `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- **보안**: 절대 공개하지 마세요!

#### DEBUG
- **설명**: 디버그 모드 활성화 여부
- **로컬**: `True`
- **Railway**: `False` (프로덕션)
- **형식**: `True` 또는 `False` (문자열)

#### ALLOWED_HOSTS
- **설명**: 접근 허용된 호스트 목록
- **로컬**: `localhost,127.0.0.1`
- **Railway**: `your-app-name.railway.app,*.railway.app`
- **형식**: 쉼표로 구분된 호스트 목록 (공백 없이)

#### DATABASE_URL
- **설명**: 데이터베이스 연결 URL
- **로컬**: 비워두면 SQLite 사용
- **Railway**: PostgreSQL 서비스 추가 시 자동 설정
- **형식**: `postgresql://user:password@host:port/dbname`

### 선택 환경 변수 (향후 확장용)

#### SITE_URL
- **설명**: 사이트의 전체 URL (결과 공유 등에 사용)
- **로컬**: `http://localhost:8000`
- **Railway**: `https://your-app-name.railway.app`
- **현재 상태**: 미사용 (향후 구현 예정)

#### EMAIL 설정 (향후 이메일 전송 기능 구현 시)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### Stripe 결제 설정 (향후 구독 모델 구현 시)
```
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 🔒 보안 주의사항

### ⚠️ 절대 하지 말아야 할 것

1. **SECRET_KEY를 Git에 커밋하지 마세요**
   - `.env` 파일은 `.gitignore`에 포함되어 있습니다
   - `settings.py`에 하드코딩하지 마세요

2. **프로덕션에서 DEBUG=True 사용하지 마세요**
   - 보안 취약점이 발생할 수 있습니다
   - Railway에서는 반드시 `DEBUG=False`로 설정

3. **환경 변수를 공개 저장소에 공유하지 마세요**
   - `.env` 파일은 로컬에서만 사용
   - Railway 환경 변수는 팀원과만 공유

### ✅ 권장 사항

1. **SECRET_KEY 정기 변경**
   - 정기적으로 SECRET_KEY를 변경하세요
   - 변경 시 세션 데이터가 무효화될 수 있습니다

2. **.env.example 파일 사용**
   - 실제 값 없이 템플릿만 제공
   - 팀원과 공유 가능

3. **환경별 설정 분리**
   - 로컬: `.env` 파일 사용
   - 프로덕션: Railway 환경 변수 사용

---

## 📚 참고 자료

- [Django 환경 변수 설정](https://docs.djangoproject.com/en/stable/topics/settings/#using-environment-variables)
- [Railway 환경 변수 설정](https://docs.railway.app/develop/variables)
- [python-decouple 라이브러리](https://github.com/henriquebastos/python-decouple) (향후 고려 가능)

---

## 🆘 문제 해결

### .env 파일이 작동하지 않을 때

1. **파일 위치 확인**
   - `.env` 파일이 프로젝트 루트 디렉토리에 있는지 확인
   - `manage.py`와 같은 위치에 있어야 합니다

2. **환경 변수 로드 확인**
   - Django는 `os.environ.get()`을 사용하여 환경 변수를 읽습니다
   - 터미널에서 직접 설정: `export SECRET_KEY=your-key`

3. **Railway 환경 변수 확인**
   - Railway 대시보드의 Variables 탭에서 설정 확인
   - 변수명과 값에 오타가 없는지 확인

### SECRET_KEY 관련 오류

- `SECRET_KEY`가 설정되지 않았을 때: Django가 기본값을 사용하지만 경고가 발생할 수 있습니다
- 프로덕션에서 하드코딩된 키 사용 시: 보안 위험! 반드시 환경 변수로 변경하세요

---

**마지막 업데이트**: 2025년 1월

