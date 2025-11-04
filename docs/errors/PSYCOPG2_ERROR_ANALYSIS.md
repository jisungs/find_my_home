# psycopg2-binary 빌드 에러 분석

## 🔴 에러 메시지

```
psycopg/utils.c:397:12: error: call to undeclared function '_PyInterpreterState_Get'
ERROR: Failed building wheel for psycopg2-binary
```

## 📋 에러 원인 분석

### 핵심 문제

**Python 3.13과 `psycopg2-binary 2.9.9` 호환성 문제**

### 상세 원인

1. **Python 3.13 내부 API 변경**
   - Python 3.13에서 `_PyInterpreterState_Get()` 함수가 변경됨
   - `psycopg2-binary 2.9.9`는 Python 3.13을 지원하지 않음
   - 컴파일 시 undefined function 에러 발생

2. **에러 발생 위치**
   ```c
   psycopg/utils.c:397:12: error: call to undeclared function '_PyInterpreterState_Get'
   ```
   - `psycopg2`의 C 확장 모듈 빌드 중 발생
   - Python 3.13의 내부 API 변경으로 인한 호환성 문제

3. **Railway CLI의 동작 방식**
   - `railway run`은 로컬 환경에서 Railway 환경 변수를 주입하여 실행
   - 로컬 Python 3.13을 사용하여 `psycopg2-binary` 빌드 시도
   - Python 3.13 호환성 문제로 빌드 실패

---

## ✅ 해결 방법

### 방법 1: Railway 웹 대시보드 터미널 사용 (가장 권장)

**Railway 배포 환경에서는 이미 패키지가 설치되어 있습니다.**

1. Railway 대시보드 접속
   - https://railway.app
   - `renewed-tranquility` 프로젝트 → `web` 서비스

2. 터미널 열기
   - "Deployments" → 최신 배포 → "View Logs" → "Shell" 탭

3. 명령어 실행 (Railway 원격 환경에서)
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py create_survey_questions
   python manage.py create_persona_types
   ```

**장점**:
- Railway 배포 환경에서 실행 (Python 버전 호환됨)
- 모든 패키지가 이미 설치되어 있음
- `psycopg2-binary` 빌드 문제 없음

### 방법 2: psycopg2-binary 버전 업그레이드 (로컬 개발용)

**Python 3.13 호환 버전 사용**

`requirements.txt` 수정:

```txt
# PostgreSQL 연결 (Python 3.13 호환 버전)
psycopg2-binary>=2.9.10  # 또는 최신 버전
```

또는 `psycopg` (psycopg3) 사용:

```txt
# psycopg2-binary 대신 psycopg 사용
psycopg[binary]>=3.1.0
```

**⚠️ 주의**: `psycopg3`는 Django 설정이 다를 수 있습니다.

### 방법 3: 로컬에서 psycopg2-binary 설치 건너뛰기

**로컬 개발 시 SQLite 사용**

```bash
# psycopg2-binary 없이 설치
pip install Django==5.2.7 gunicorn==21.2.0 dj-database-url==2.1.0 whitenoise==6.6.0

# 로컬에서는 SQLite 사용 (DATABASE_URL 없음)
python manage.py migrate
```

**Railway 배포 시**:
- Railway 배포 환경에서는 `psycopg2-binary`가 정상적으로 설치됨
- Railway의 Python 버전은 3.13.5이지만, 빌드 환경이 다름

---

## 🔍 상황별 대응

### 상황 1: Railway 배포 마무리 작업

**권장**: Railway 웹 대시보드 터미널 사용

```bash
# Railway 대시보드 → Shell 탭에서
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_survey_questions
python manage.py create_persona_types
```

### 상황 2: 로컬 개발/테스트

**권장**: psycopg2-binary 없이 SQLite 사용

```bash
# 가상환경 활성화
source venv/bin/activate

# psycopg2-binary 제외하고 설치
pip install Django==5.2.7 gunicorn==21.2.0 dj-database-url==2.1.0 whitenoise==6.6.0

# 로컬 SQLite 사용
python manage.py migrate
python manage.py runserver
```

### 상황 3: Railway CLI로 원격 명령 실행

**문제**: `railway run`이 로컬에서 실행되면서 Python 3.13 호환성 문제 발생

**해결**: Railway 웹 대시보드 터미널 사용 (방법 1)

---

## 📊 Python 버전별 호환성

| psycopg2-binary 버전 | Python 3.11 | Python 3.12 | Python 3.13 |
|---------------------|-------------|-------------|-------------|
| 2.9.9 | ✅ | ✅ | ❌ |
| 2.9.10+ | ✅ | ✅ | ✅ (예상) |

---

## 🎯 결론

### 현재 에러의 원인

**Python 3.13과 `psycopg2-binary 2.9.9`의 호환성 문제**

### 해결 방법

1. **Railway 배포 마무리**: Railway 웹 대시보드 터미널 사용 (권장)
2. **로컬 개발**: psycopg2-binary 없이 SQLite 사용
3. **패키지 업그레이드**: psycopg2-binary 최신 버전 사용

### 중요 사항

**Railway 배포 환경에서는 문제가 없습니다!**
- Railway 배포 시 `psycopg2-binary`가 정상적으로 설치됨
- Railway의 빌드 환경이 Python 3.13 호환성을 지원
- 따라서 로컬에서 설치가 실패해도 Railway 배포에는 영향 없음

**로컬 개발 시**:
- `psycopg2-binary` 없이 개발 가능 (SQLite 사용)
- Railway 배포 시에만 PostgreSQL 사용

---

## 📚 참고 자료

- [psycopg2 Python 3.13 호환성 이슈](https://github.com/psycopg/psycopg2/issues)
- [Python 3.13 변경사항](https://docs.python.org/3.13/whatsnew/3.13.html)
- [Railway 배포 가이드](https://docs.railway.app)

---

**마지막 업데이트**: 2025년 1월

