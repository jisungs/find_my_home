# 에러 분석 문서

이 폴더에는 프로젝트 배포 및 개발 중 발생한 에러들의 분석 문서가 포함되어 있습니다.

## 📋 문서 목록

### 1. ERROR_ANALYSIS.md
- **주제**: Django 모듈 import 에러
- **에러**: `ModuleNotFoundError: No module named 'django'`
- **원인**: 가상환경 미활성화 또는 Railway CLI 사용 시 문제
- **해결**: 가상환경 활성화 또는 Railway 웹 대시보드 터미널 사용

### 2. PSYCOPG2_ERROR_ANALYSIS.md
- **주제**: psycopg2-binary 빌드 에러
- **에러**: `call to undeclared function '_PyInterpreterState_Get'`
- **원인**: Python 3.13과 psycopg2-binary 2.9.9 호환성 문제
- **해결**: Railway 웹 대시보드 터미널 사용 또는 패키지 업그레이드

### 3. RAILWAY_ERROR_ANALYSIS.md
- **주제**: Railway 배포 초기 에러
- **에러**: `secret POSTGRES_PASSWORD: not found`
- **원인**: PostgreSQL 서비스 미생성 또는 서비스 순서 문제
- **해결**: PostgreSQL 서비스를 먼저 생성 후 웹 서비스 배포

### 4. RAILWAY_ERROR_DETAILED_ANALYSIS.md
- **주제**: Railway 배포 에러 상세 분석
- **에러**: `secret POSTGRES_PASSWORD: not found` (상세 버전)
- **원인**: Railway Nixpacks 빌드 시스템의 의존성 검증 문제
- **해결**: PostgreSQL 서비스 먼저 생성, Nixpacks 설정, 또는 임시 해결책

### 5. RAILWAY_HOSTNAME_ERROR_ANALYSIS.md
- **주제**: Railway 호스트명 에러
- **에러**: `could not translate host name "postgres.railway.internal" to address`
- **원인**: Railway 내부 네트워크 호스트명에 로컬 환경에서 접근 불가
- **해결**: Railway 웹 대시보드 터미널 사용

### 6. RAILWAY_MIGRATE_ERROR_ANALYSIS.md
- **주제**: Railway migrate 에러
- **에러**: `ModuleNotFoundError: No module named 'psycopg2'` 또는 호스트명 에러
- **원인**: Railway CLI가 로컬에서 실행되면서 PostgreSQL 연결 시도
- **해결**: Railway 웹 대시보드 터미널 사용

### 7. DATABASE_TABLE_NOT_FOUND.md
- **주제**: 데이터베이스 테이블 없음 에러
- **에러**: `relation "survey_survey" does not exist`
- **원인**: 마이그레이션이 실행되지 않아 테이블이 생성되지 않음
- **해결**: Railway 웹 대시보드 터미널에서 마이그레이션 실행

### 8. CSRF_ERROR_ANALYSIS.md
- **주제**: Django CSRF 검증 실패
- **에러**: `Origin checking failed - does not match any trusted origins`
- **원인**: `CSRF_TRUSTED_ORIGINS`에 Railway 도메인이 포함되지 않음
- **해결**: `settings.py`에 `CSRF_TRUSTED_ORIGINS` 설정 추가

### 9. DJ_DATABASE_URL_WARNING.md
- **주제**: IDE import 경고 메시지
- **에러**: `가져오기 "dj_database_url"을(를) 확인할 수 없습니다.`
- **원인**: IDE가 올바른 Python 인터프리터를 인식하지 못함
- **해결**: IDE 인터프리터 설정 확인 및 캐시 무효화

### 10. LOCAL_RAILWAY_DATABASE_ERROR.md
- **주제**: 로컬 개발 환경에서 Railway PostgreSQL 연결 에러
- **에러**: `could not translate host name "postgres.railway.internal" to address`
- **원인**: `.env` 파일에 Railway 내부 호스트명이 설정되어 로컬에서 접근 시도
- **해결**: `settings.py`에서 Railway 내부 호스트명 자동 감지 또는 `.env`에서 주석 처리

---

## 🎯 빠른 참조

### Railway 배포 관련 에러
- PostgreSQL 서비스 미생성: `RAILWAY_ERROR_ANALYSIS.md`
- 내부 호스트명 접근 불가: `RAILWAY_HOSTNAME_ERROR_ANALYSIS.md`
- 마이그레이션 에러: `RAILWAY_MIGRATE_ERROR_ANALYSIS.md`

### 개발 환경 관련 에러
- Django 모듈 import: `ERROR_ANALYSIS.md`
- psycopg2 설치: `PSYCOPG2_ERROR_ANALYSIS.md`
- IDE import 경고: `DJ_DATABASE_URL_WARNING.md`

---

## 📚 참고

대부분의 Railway 배포 관련 에러는 **Railway 웹 대시보드 터미널**을 사용하면 해결됩니다:

1. Railway 대시보드 접속
2. 프로젝트 → 서비스 선택
3. "Deployments" → "View Logs" → "Shell" 탭
4. 원격 환경에서 명령어 실행

---

**마지막 업데이트**: 2025년 1월

