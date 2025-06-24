# U-Guinong Backend

FastAPI, PostgreSQL, LangGraph 기반으로 구축된 "유, 귀농" 백엔드 시스템입니다.  
LLM 기반 챗봇, 문서 기반 RAG 검색 등을 하나의 통합 API로 제공하며, 모든 기능은 네이버 클라우드 플랫폼 상에 배포되어 운영됩니다.

---

## 개발 환경
- Python 3.13.2
- postgresql 14.18

---

## 디렉토리 구조

```
u-guinong-backend/
├─ src/
│  ├─ auth/         # 사용자 인증 (JWT, OAuth)
│  ├─ chat/         # 채팅 세션 및 메시지 관리
│  ├─ core/         # 설정 파일 (환경변수, OAuth 키 등)
│  ├─ llm/          # LangGraph 기반 LLM workflow 처리
│  ├─ rag/          # 문서 임베딩 및 검색 (RAG)
│  ├─ vision/       # 이미지 분석 관련 처리 (향후 확장)
│  ├─ database.py   # DB 연결 및 초기화
│  ├─ models.py     # 공통 DB 모델
│  └─ main.py       # FastAPI 앱 엔트리포인트
````

---

## 실행 방법

```bash
# 1. 리포지토리 클론
git clone https://github.com/SogangCapstone-Team6/u-guinong-backend.git
cd u-guinong-backend

# 2. 가상환경 설정
python -m venv .venv
source .venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. DB 세팅
alembic init migrations
alembic revision --autogenerate -m "{message}"
alembic upgrade head

# 5. 리소스 파일 추가 (data/)

# 6. 설정파일 설정 

# 7. 서버 실행
uvicorn -p "PORT" -h "HOST" src.main:app  
````

---

## 기능별 구현 상세

### API docs
> **자세한 API 문서는 서버 실행 후 /docs 를 통해 확인 가능** 

### 회원 시스템 (Auth)

* FastAPI 기반 JWT 인증 시스템 구축
* 이메일과 비밀번호를 이용한 회원가입 및 로그인 구현
* 비밀번호는 해시 처리되어 DB에 저장되며, 로그인 시 JWT 발급
* JWT를 통해 유저 인증 후 API 접근 제어

| Endpoint           | Method | 설명          |
| ------------------ | ------ | ----------- |
| `/api/auth/signup` | POST   | 회원가입        |
| `/api/auth/login`  | POST   | 로그인 및 토큰 발급 |

---

### 채팅 시스템 (Chat)

* 사용자의 채팅방 목록 확인, 새 채팅방 생성, 채팅 내역 조회 및 메시지 전송 기능 포함
* 모든 요청은 JWT 인증을 통해 사용자 식별 후 처리
* 채팅방 ID는 UUID 기반으로 생성, 사용자-채팅방 매핑은 외래키로 관리

| Endpoint         | Method | 설명              |
| ---------------- | ------ | --------------- |
| `/api/chat/`     | GET    | 채팅방 목록 조회       |
| `/api/chat/`     | POST   | 새로운 채팅방 생성      |
| `/api/chat/{id}` | GET    | 해당 채팅방 대화 내역 조회 |
| `/api/chat/{id}` | POST   | 해당 채팅방에 메시지 전송  |

---

### LLM Workflow (LangGraph)

* LangGraph 프레임워크를 활용해 LLM 기반 질문 응답 워크플로우 구현
* OpenAI GPT-4o-mini 모델 사용
* 질의가 농작물 관련인지 판단 → 관련 시 RAG 수행, 아니라면 LLM 직접 호출

**LLM Workflow Logic**

1. 사용자 질문이 농작물 관련인지 LLM을 통해 판별
2. 관련 있으면 RAG 검색 → 검색 결과 포함하여 GPT 호출
3. 관련 없으면 바로 GPT 호출


---

### RAG 시스템

* 농촌진흥청 농업과학도서관의 PDF 자료를 기반으로 문서 임베딩 구축
* Sentence Transformers를 이용해 문서 임베딩 생성 후 FAISS/Chroma로 인덱싱
* 사용자 질문과 유사한 문서 검색 → LLM 응답에 포함

**구성 요소**

* `embedding_model.py`: 텍스트 임베딩 생성
* `fine_search.py`: 문서 검색 (Top-K 유사 문단)
* `setup.py`: 문서 인덱스 초기화 및 생성