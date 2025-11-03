# Railway 배포 가이드

이 문서는 부산 집 찾기 서비스(Find My Home)를 Railway에 배포하기 위한 가이드입니다.

## 📋 배포 준비 사항

### ✅ 완료된 작업
- [x] `requirements.txt` 생성 (필수 패키지 포함)
- [x] `Procfile` 생성 (gunicorn 웹 서버)
- [x] `runtime.txt` 생성 (Python 3.13.5)
- [x] `settings.py` 프로덕션 설정 업데이트
- [x] `.gitignore` 업데이트 (staticfiles 제외)

## 🚀 Railway 배포 단계

### 1. Railway 계정 및 프로젝트 생성

1. **Railway 가입 및 로그인**
   - https://railway.app 접속
   - GitHub 계정으로 로그인 권장

2. **새 프로젝트 생성**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - GitHub 저장소 연결

### 2. PostgreSQL 데이터베이스 추가

1. Railway 대시보드에서 프로젝트 선택
2. "+ New" 버튼 클릭
3. "Database" → "Add PostgreSQL" 선택
4. PostgreSQL 인스턴스가 생성되면 자동으로 `DATABASE_URL` 환경변수가 설정됩니다

### 3. 환경 변수 설정

Railway 대시보드의 "Variables" 탭에서 다음 환경 변수를 설정합니다:

| 변수명 | 설명 | 예시 값 |
|--------|------|---------|
| `SECRET_KEY` | Django 시크릿 키 | `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`로 생성 |
| `DEBUG` | 디버그 모드 (프로덕션에서는 False) | `False` |
| `ALLOWED_HOSTS` | 허용된 호스트 (Railway 도메인) | `your-app-name.railway.app,*.railway.app` |

**SECRET_KEY 생성 방법:**
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. 빌드 설정

Railway는 자동으로 다음을 감지합니다:
- `Procfile`: 웹 서버 실행 방법
- `requirements.txt`: Python 패키지 설치
- `runtime.txt`: Python 버전

### 5. 배포 후 작업

배포가 완료되면 Railway 터미널 또는 로컬에서 다음 명령을 실행해야 합니다:

```bash
# 1. 마이그레이션 실행
python manage.py migrate

# 2. 정적 파일 수집
python manage.py collectstatic --noinput

# 3. 슈퍼유저 생성 (선택사항)
python manage.py createsuperuser

# 4. 초기 데이터 생성 (필요한 경우)
python manage.py create_survey_questions
python manage.py create_persona_types
python manage.py create_sample_properties
```

**Railway 터미널 사용 방법:**
1. Railway 대시보드에서 프로젝트 선택
2. "View Logs" 클릭
3. "Deploy Logs" 탭에서 터미널 사용 가능

또는 Railway CLI 사용:
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
```

### 6. Build Command 설정 (선택사항)

Railway 대시보드의 "Settings" → "Deploy"에서 Build Command를 설정할 수 있습니다:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### 7. Start Command 설정

Railway가 `Procfile`을 자동으로 인식하므로 별도 설정이 필요 없습니다. 하지만 수동으로 설정하려면:

```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

## 🔍 배포 확인

1. **배포 로그 확인**
   - Railway 대시보드의 "Deploy Logs" 확인
   - 에러가 없는지 확인

2. **서비스 접속 테스트**
   - Railway에서 제공하는 도메인으로 접속
   - 각 페이지가 정상 작동하는지 확인

3. **환경 변수 확인**
   - Railway 대시보드의 "Variables" 탭에서 모든 변수가 설정되었는지 확인

## ⚠️ 문제 해결

### 정적 파일이 로드되지 않는 경우

1. `collectstatic` 명령이 실행되었는지 확인
2. `STATIC_ROOT` 설정 확인
3. WhiteNoise 미들웨어가 설치되어 있는지 확인

### 데이터베이스 연결 오류

1. PostgreSQL 서비스가 실행 중인지 확인
2. `DATABASE_URL` 환경변수가 설정되었는지 확인
3. Railway가 자동으로 `DATABASE_URL`을 설정했는지 확인

### 500 에러 발생

1. `DEBUG=False`로 설정된 경우, 로그에서 실제 에러 확인
2. Railway 로그에서 상세 에러 메시지 확인
3. 환경 변수가 올바르게 설정되었는지 확인

### 마이그레이션 오류

1. 로컬에서 `python manage.py makemigrations` 실행
2. 변경사항 커밋 및 푸시
3. Railway에서 자동으로 마이그레이션 실행되도록 설정하거나 수동 실행

## 📚 참고 자료

- [Railway 공식 문서](https://docs.railway.app/)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn 문서](https://docs.gunicorn.org/)
- [WhiteNoise 문서](http://whitenoise.evans.io/)

## 🔒 보안 체크리스트

- [x] `SECRET_KEY` 환경변수로 설정
- [x] `DEBUG=False` 프로덕션에서 설정
- [x] `ALLOWED_HOSTS` 올바르게 설정
- [x] HTTPS 리다이렉트 활성화 (프로덕션)
- [x] 보안 쿠키 설정 (프로덕션)
- [x] CSRF 보호 활성화

## 💡 추가 팁

1. **자동 배포**: GitHub에 푸시하면 자동으로 재배포됩니다
2. **커스텀 도메인**: Railway에서 커스텀 도메인을 연결할 수 있습니다
3. **로그 모니터링**: Railway 대시보드에서 실시간 로그 확인 가능
4. **환경 분리**: Development, Staging, Production 환경을 분리하여 관리 가능

