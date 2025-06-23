# 🌾 U-Guinong Backend

청년 귀농인을 위한 AI 농업 도우미 앱  "유, 귀농" 의 FastAPI 기반 백엔드입니다.  
이미지 기반 작물 분석, 대화형 질의응답, 문서 기반 정보 검색 등 다양한 기능을 제공하여  
기존 농업 정보 시스템의 한계를 보완합니다.

---

## 🧩 주요 기능

- 🔐 **소셜 로그인 및 JWT 인증** (Google, Kakao 등)
- 💬 **대화형 챗봇** (LLM 기반 질문 응답 + 대화 흐름 유지)
- 📚 **RAG (문서 기반 질의응답)**  
  - 농촌진흥청 PDF를 벡터화해 관련 정보를 검색하고 응답 생성
- 🌱 **Vision 모델 결과 수신 및 처리**  
  - YOLOv5s + MobileNetV2 기반 추론 결과 수신 → 질병 분석
- 🗃️ **채팅 세션, 히스토리, 사용자 정보 관리**

---

## 🛠️ 기술 스택

| 영역 | 스택 |
|------|------|
| Web Framework | FastAPI, Uvicorn |
| 인증 | OAuth2, JWT |
| DB | SQLAlchemy + SQLite/PostgreSQL |
| LLM | OpenAI GPT API (GPT-4o 등) |
| 문서 검색 | FAISS / Chroma + Sentence Transformers |
| Vision 모델 | YOLOv5s + MobileNetV2 → TFLite 변환 |
| 배포 환경 | Docker, Naver Cloud |

---

## ⚙️ 설치 및 실행

```bash
# 1. 리포지토리 클론
git clone https://github.com/SogangCapstone-Team6/u-guinong-backend.git
cd u-guinong-backend

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 서버 실행
uvicorn src.main:app --reload
