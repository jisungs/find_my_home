# Railway 프로덕션 배포 에러 분석

## 🔴 에러 메시지

```
ImportError: /app/.venv/lib/python3.13/site-packages/psycopg2/_psycopg.cpython-313-x86_64-linux-gnu.so: 
undefined symbol: _PyInterpreterState_Get

django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 or psycopg module

Worker failed to boot.
```

## 📋 에러 원인 분석

### 핵심 문제

**Railway 배포 환경에서 Python 3.13과 `psycopg2-binary 2.9.9`의 호환성 문제**

### 상세 원인

1. **에러 발생 위치**
   - Railway 배포 환경 (`/app/.venv/` 경로)
   - gunicorn 워커가 Django 애플리케이션을 로드하는 과정
   - Django가 PostgreSQL 백엔드를 초기화하는 시점

2. **Python 3.13 호환성 문제**
   ```
   undefined symbol: _PyInterpreterState_Get
   ```
   - Python 3.13에서 `_PyInterpreterState_Get()` 함수가 변경됨
   - `psycopg2-binary 2.9.9`는 Python 3.13을 지원하지 않음
   - 컴파일된 바이너리가 Python 3.13의 심볼을 찾을 수 없음

3. **Railway의 Python 버전**
   - `runtime.txt`에서 Python 3.13.5 지정
   - Railway가 Python 3.13.5로 빌드
   - `psycopg2-binary 2.9.9`가 Python 3.13과 호환되지 않음

4. **에러 발생 시점**
   - 배포 시 `psycopg2-binary`가 설치됨 (빌드는 성공)
   - 하지만 런타임에 모듈 로드 시 심볼을 찾을 수 없음
   - gunicorn 워커가 시작하지 못함

### 에러 발생 흐름

```
Railway 배포 시작
  ↓
Python 3.13.5 환경에서 빌드
  ↓
psycopg2-binary 2.9.9 설치 (빌드 성공)
  ↓
gunicorn 시작
  ↓
Django 애플리케이션 로드
  ↓
PostgreSQL 백엔드 초기화
  ↓
psycopg2 모듈 로드 시도
  ↓
undefined symbol: _PyInterpreterState_Get
  ↓
ImportError 발생
  ↓
Worker failed to boot
```

---

## ✅ 해결 방법

### 방법 1: Python 버전 다운그레이드 (권장)

**Python 3.13 → Python 3.12로 변경**

`runtime.txt` 파일 수정:

```txt
python-3.12.7
```

또는:

```txt
python-3.11.9
```

**이유**:
- Python 3.12/3.11은 `psycopg2-binary 2.9.9`와 호환됨
- 안정적이고 검증된 조합

**장점**:
- `psycopg2-binary` 버전 변경 불필요
- 가장 빠른 해결 방법
- 안정성 확보

### 방법 2: psycopg2-binary 버전 업그레이드

**Python 3.13 호환 버전 사용**

`requirements.txt` 파일 수정:

```txt
# PostgreSQL 연결 (Python 3.13 호환)
psycopg2-binary>=2.9.10
```

또는 최신 버전:

```txt
psycopg2-binary>=3.0.0
```

**⚠️ 주의**: 
- 최신 버전이 Python 3.13을 지원하는지 확인 필요
- 버전 업그레이드 시 다른 호환성 문제 발생 가능

### 방법 3: psycopg (psycopg3) 사용

**psycopg2 대신 psycopg3 사용**

`requirements.txt` 파일 수정:

```txt
# PostgreSQL 연결 (psycopg3 사용)
psycopg[binary]>=3.1.0
```

**⚠️ 주의**: 
- Django 설정 변경 필요할 수 있음
- `dj-database-url`와의 호환성 확인 필요

---

## 🔧 즉시 해결 방법 (가장 권장)

### Step 1: Python 버전 변경

`runtime.txt` 파일 수정:

```txt
python-3.12.7
```

### Step 2: 변경사항 커밋 및 푸시

```bash
git add runtime.txt
git commit -m "fix: Python 3.13 → 3.12로 변경 (psycopg2 호환성 문제 해결)"
git push origin main
```

### Step 3: Railway 재배포

- Railway가 자동으로 재배포 시작
- Python 3.12 환경에서 빌드 및 실행
- `psycopg2-binary 2.9.9`가 정상 작동

---

## 🔍 문제 진단

### 확인 사항

1. **Python 버전 확인**
   ```bash
   cat runtime.txt
   # python-3.13.5 → 문제 원인
   ```

2. **psycopg2-binary 버전 확인**
   ```bash
   cat requirements.txt | grep psycopg
   # psycopg2-binary==2.9.9 → Python 3.13 미지원
   ```

3. **에러 로그 확인**
   - Railway 대시보드 → "View Logs"
   - `undefined symbol: _PyInterpreterState_Get` 확인
   - `Worker failed to boot` 확인

---

## 📊 Python 버전별 호환성

| Python 버전 | psycopg2-binary 2.9.9 | 권장 |
|------------|----------------------|------|
| Python 3.11 | ✅ 호환 | ✅ 권장 |
| Python 3.12 | ✅ 호환 | ✅ 권장 |
| Python 3.13 | ❌ 미지원 | ❌ 문제 발생 |

---

## 🎯 결론

### 현재 에러의 원인

**Railway 배포 환경에서 Python 3.13과 `psycopg2-binary 2.9.9`의 호환성 문제**

### 해결 방법

1. **Python 버전 다운그레이드**: `runtime.txt`에서 Python 3.12로 변경 (가장 권장)
2. **psycopg2-binary 업그레이드**: Python 3.13 호환 버전 사용
3. **psycopg3 사용**: psycopg2 대신 psycopg3 사용

### 권장 사항

**Python 3.12로 변경하는 것이 가장 빠르고 안정적인 해결책입니다.**

---

## 📚 참고 자료

- [psycopg2 Python 3.13 호환성 이슈](https://github.com/psycopg/psycopg2/issues)
- [Python 3.13 변경사항](https://docs.python.org/3.13/whatsnew/3.13.html)
- [Railway Python 버전 설정](https://docs.railway.app/guides/python)

---

**마지막 업데이트**: 2025년 1월

