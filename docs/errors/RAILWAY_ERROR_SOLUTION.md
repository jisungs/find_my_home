# Railway 에러 해결 가이드

## 🎯 문제 요약

`railway run` 명령어를 로컬에서 실행하면 Railway 내부 호스트명(`postgres.railway.internal`)에 접근할 수 없어서 에러가 발생합니다.

---

## ✅ 해결 방법 (우선순위별)

### 방법 1: Railway 웹 대시보드 터미널 사용 (가장 권장)

**Railway 배포 환경에서 직접 실행하는 방법**

#### Step 1: Railway 대시보드 접속

1. https://railway.app 접속
2. 로그인
3. `renewed-tranquility` 프로젝트 선택
4. `web` 서비스 선택

#### Step 2: 터미널 열기

1. 상단 메뉴에서 **"Deployments"** 탭 클릭
2. 최신 배포(가장 위에 있는 것) 선택
3. **"View Logs"** 버튼 클릭
4. **"Shell"** 탭 선택 (또는 터미널 아이콘 클릭)

#### Step 3: 명령어 실행

Railway의 원격 터미널에서 다음 명령어들을 순서대로 실행:

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

**장점**:
- ✅ Railway 내부 네트워크에서 실행
- ✅ `postgres.railway.internal` 호스트에 접근 가능
- ✅ PostgreSQL 데이터베이스에 직접 연결
- ✅ 모든 패키지가 이미 설치되어 있음

---

### 방법 2: Python 버전 변경 후 재배포

**이미 `runtime.txt`를 Python 3.12로 변경했으므로 커밋하고 푸시**

#### Step 1: 변경사항 확인

```bash
git status
git diff runtime.txt
```

#### Step 2: 커밋 및 푸시

```bash
git add runtime.txt
git commit -m "fix: Python 3.13 → 3.12로 변경 (psycopg2 호환성 문제 해결)"
git push origin main
```

#### Step 3: Railway 자동 재배포 대기

- Railway가 자동으로 변경사항을 감지하고 재배포 시작
- Python 3.12 환경에서 빌드 및 실행
- `psycopg2-binary 2.9.9`가 정상 작동

#### Step 4: 재배포 후 Railway 웹 대시보드 터미널에서 마이그레이션 실행

재배포가 완료되면 방법 1의 Step 2-3을 따라 Railway 웹 대시보드 터미널에서 마이그레이션을 실행하세요.

---

### 방법 3: 로컬 개발용 (임시 해결책)

**로컬에서 테스트할 때만 사용**

```bash
# Railway 환경 변수 제거
unset DATABASE_URL

# 로컬 SQLite 사용
python manage.py migrate
python manage.py runserver
```

**⚠️ 주의**: 
- 이 방법은 로컬 SQLite 데이터베이스를 사용합니다
- Railway PostgreSQL과는 별개입니다
- 실제 배포 마무리 작업에는 사용하지 마세요

---

## 🚀 권장 실행 순서

### 즉시 실행 (배포 마무리)

1. **Python 버전 변경사항 커밋 및 푸시**
   ```bash
   git add runtime.txt
   git commit -m "fix: Python 3.13 → 3.12로 변경"
   git push origin main
   ```

2. **Railway 재배포 완료 대기** (약 2-3분)

3. **Railway 웹 대시보드 터미널 사용**
   - Railway 대시보드 → 프로젝트 → 서비스
   - "Deployments" → "View Logs" → "Shell" 탭
   - 명령어 실행:
     ```bash
     python manage.py migrate
     python manage.py collectstatic --noinput
     python manage.py create_survey_questions
     python manage.py create_persona_types
     python manage.py create_sample_properties
     ```

---

## 📋 체크리스트

### Railway 배포 마무리 작업

- [ ] `runtime.txt` Python 3.12로 변경 확인
- [ ] 변경사항 커밋 및 푸시
- [ ] Railway 재배포 완료 대기
- [ ] Railway 웹 대시보드 터미널 접속
- [ ] 마이그레이션 실행 완료
- [ ] 정적 파일 수집 완료
- [ ] 초기 데이터 생성 완료
- [ ] 웹사이트 접속 테스트

---

## 🔍 문제 해결 확인

### 배포 성공 확인

1. **Railway 로그 확인**
   - Railway 대시보드 → "View Logs"
   - 에러 메시지가 없는지 확인
   - "Worker booted successfully" 메시지 확인

2. **웹사이트 접속 테스트**
   - Railway가 제공하는 도메인으로 접속
   - 예: `https://your-app-name.railway.app`
   - 홈페이지가 정상적으로 로드되는지 확인

3. **데이터베이스 확인**
   - Railway 대시보드 터미널에서:
     ```bash
     python manage.py dbshell
     # PostgreSQL 셸 접속 확인
     ```

---

## ⚠️ 중요 사항

### Railway CLI의 한계

**`railway run`은 원격 서버에서 실행하지 않습니다!**

- 로컬 환경에서 Railway 환경 변수를 주입하여 실행
- 따라서 Railway 내부 네트워크 호스트명에 접근할 수 없음
- 배포 마무리 작업은 **반드시 Railway 웹 대시보드 터미널**을 사용해야 함

### 왜 Railway 웹 대시보드 터미널을 사용해야 하는가?

1. **내부 네트워크 접근**
   - Railway 내부 네트워크에서 실행
   - `postgres.railway.internal` 호스트에 접근 가능

2. **패키지 설치 상태**
   - 모든 패키지가 이미 설치되어 있음
   - Python 버전이 올바르게 설정됨

3. **데이터베이스 연결**
   - PostgreSQL 데이터베이스에 직접 연결
   - 실제 배포 환경과 동일한 조건

---

## 🎯 결론

### 가장 확실한 해결 방법

1. **Python 버전 변경사항 커밋 및 푸시** (이미 완료)
2. **Railway 재배포 완료 대기**
3. **Railway 웹 대시보드 터미널에서 마이그레이션 실행**

이 순서를 따르면 100% 문제가 해결됩니다.

---

**마지막 업데이트**: 2025년 1월

