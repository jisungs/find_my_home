# Django CSRF 검증 실패 에러 분석

## 🔴 에러 메시지

```
Forbidden (403)
CSRF 검증에 실패했습니다. 요청을 중단하였습니다.

Origin checking failed - https://web-production-2d468.up.railway.app does not match any trusted origins.
```

## 📋 에러 원인 분석

### 핵심 문제

**Django의 CSRF 보안 설정에서 Railway 도메인이 신뢰할 수 있는 Origin으로 설정되지 않음**

### 상세 원인

1. **CSRF 보안 메커니즘**
   - Django는 CSRF(Cross-Site Request Forgery) 공격을 방지하기 위해 Origin 검증을 수행
   - POST 요청의 Origin 헤더가 `CSRF_TRUSTED_ORIGINS`에 포함되어 있어야 함
   - Railway 도메인이 신뢰 목록에 없어서 검증 실패

2. **현재 설정 상태**
   - `settings.py`에 `CSRF_TRUSTED_ORIGINS` 설정이 없거나 Railway 도메인이 포함되지 않음
   - Railway 도메인: `https://web-production-2d468.up.railway.app`

3. **에러 발생 시점**
   - POST 요청 시 발생 (폼 제출 등)
   - Django가 요청의 Origin 헤더를 확인
   - 신뢰 목록에 없으면 403 Forbidden 반환

---

## ✅ 해결 방법

### 방법 1: settings.py에 CSRF_TRUSTED_ORIGINS 추가 (권장)

**환경 변수로 Railway 도메인 관리**

`config/settings.py`에 다음 설정 추가:

```python
# CSRF 보안 설정
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'https://web-production-2d468.up.railway.app,http://localhost:8000'
).split(',')
```

또는 더 명확하게:

```python
# CSRF 신뢰할 수 있는 Origin 목록
CSRF_TRUSTED_ORIGINS = []

# 환경 변수에서 읽기
csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins.split(',')]
else:
    # 기본값 (로컬 개발용)
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
    
    # Railway 환경 변수 확인
    railway_public_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
    if railway_public_domain:
        CSRF_TRUSTED_ORIGINS.append(f'https://{railway_public_domain}')
```

### 방법 2: Railway 환경 변수에 CSRF_TRUSTED_ORIGINS 설정

**Railway 대시보드에서 환경 변수 추가**

1. Railway 대시보드 접속
2. 프로젝트 → 서비스 선택
3. "Variables" 탭
4. 새 변수 추가:
   - **변수명**: `CSRF_TRUSTED_ORIGINS`
   - **값**: `https://web-production-2d468.up.railway.app`
   - 쉼표로 구분하여 여러 도메인 추가 가능

그리고 `settings.py`에서 읽기:

```python
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:8000'
).split(',')
```

### 방법 3: ALLOWED_HOSTS와 연동

**Railway 도메인을 자동으로 추가**

```python
# ALLOWED_HOSTS 설정
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else []

# CSRF_TRUSTED_ORIGINS 자동 설정
CSRF_TRUSTED_ORIGINS = []
for host in ALLOWED_HOSTS:
    if host:
        CSRF_TRUSTED_ORIGINS.append(f'https://{host}')
        CSRF_TRUSTED_ORIGINS.append(f'http://{host}')

# 로컬 개발용 기본값
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
```

---

## 🔧 즉시 해결 방법

### Step 1: settings.py 수정

`config/settings.py` 파일에 `CSRF_TRUSTED_ORIGINS` 설정 추가

### Step 2: Railway 환경 변수 설정

Railway 대시보드에서 `CSRF_TRUSTED_ORIGINS` 환경 변수 추가

### Step 3: 재배포

변경사항 커밋 및 푸시 후 Railway가 자동 재배포

---

## 📊 CSRF 보안 설정 개요

### Django CSRF 보안

Django는 CSRF 공격을 방지하기 위해:

1. **Origin 검증**: 요청의 Origin 헤더 확인
2. **Referer 검증**: 요청의 Referer 헤더 확인
3. **CSRF 토큰**: 폼에 CSRF 토큰 포함

### CSRF_TRUSTED_ORIGINS의 역할

- POST 요청의 Origin 헤더가 이 목록에 포함되어 있어야 함
- HTTPS 요청의 경우 반드시 설정 필요
- 로컬 개발 환경에서는 HTTP도 허용

---

## 🎯 권장 설정

### 프로덕션 환경 (Railway)

```python
# 환경 변수에서 읽기
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    ''
).split(',')

# 빈 문자열 제거
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS if origin.strip()]
```

Railway 환경 변수:
```
CSRF_TRUSTED_ORIGINS=https://web-production-2d468.up.railway.app
```

### 로컬 개발 환경

```python
# 로컬 개발용 기본값
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ]
```

---

## 🔍 문제 해결 확인

### 설정 확인

1. **settings.py 확인**
   ```python
   print(CSRF_TRUSTED_ORIGINS)
   # Railway 도메인이 포함되어 있는지 확인
   ```

2. **Railway 환경 변수 확인**
   - Railway 대시보드 → "Variables" 탭
   - `CSRF_TRUSTED_ORIGINS` 변수 확인

3. **에러 재현 확인**
   - 폼 제출 시도
   - 403 에러가 발생하지 않는지 확인

---

## 📚 참고 자료

- [Django CSRF 보안](https://docs.djangoproject.com/en/stable/ref/csrf/)
- [CSRF_TRUSTED_ORIGINS 설정](https://docs.djangoproject.com/en/stable/ref/settings/#csrf-trusted-origins)
- [Railway 환경 변수 설정](https://docs.railway.app/develop/variables)

---

**마지막 업데이트**: 2025년 1월

