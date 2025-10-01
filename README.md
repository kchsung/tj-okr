# OKR Mini Program (Streamlit + OpenAI)

OKR(목표와 핵심 결과) 관리 및 AI 검증을 위한 Streamlit 애플리케이션입니다.

## 🚀 로컬 개발 환경 설정

### 1) 준비
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp env.example .env
# .env에 OPENAI_API_KEY 입력
```

### 2) 실행
```bash
streamlit run streamlit_app/app.py
```

## ☁️ Streamlit Cloud 배포

### 1) GitHub 저장소 설정
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/kchsung/tj-okr.git
git push -u origin main
```

### 2) Streamlit Cloud 배포
1. [Streamlit Cloud](https://share.streamlit.io/)에 로그인
2. "New app" 클릭
3. Repository: `kchsung/tj-okr` 선택
4. Main file path: `streamlit_app/app.py` 입력
5. Advanced settings에서 환경변수 설정:
   - `OPENAI_API_KEY`: OpenAI API 키
   - `OPENAI_MODEL`: `gpt-4o-mini` (선택사항)
   - `DB_URL`: `sqlite:///okr.db` (선택사항)

### 3) 데이터베이스 주의사항
- **Streamlit Cloud는 임시 파일 시스템을 사용**하므로 SQLite 데이터는 앱 재시작 시 초기화됩니다
- 영구 데이터 저장이 필요한 경우 클라우드 데이터베이스 서비스 사용을 권장합니다
- 현재는 데모/프로토타입 용도로 SQLite를 사용합니다

## 📋 기능

* Objective & KR 입력
* 주간 수행내역 입력
* OpenAI 기반 AI 검증(시스템 프롬프트 하드코딩 + 사용자 추가 프롬프트)
* SQLite 데이터베이스 기반 데이터 저장
* 반응형 UI 컴포넌트

## 🔧 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite (로컬), 확장 가능한 구조
- **AI**: OpenAI GPT API
- **ORM**: SQLAlchemy

## 📁 프로젝트 구조

```
streamlit_app/
├── app.py              # 메인 애플리케이션
├── config/
│   └── settings.py     # 설정 관리
├── db/
│   ├── models.py       # 데이터베이스 모델
│   └── repository.py   # 데이터 접근 계층
├── services/
│   └── ai_validator.py # AI 검증 서비스
└── ui/
    ├── components.py   # UI 컴포넌트
    └── styles.css      # 스타일시트
```

## 🔮 확장 아이디어

* KR별 진행현황(도넛/게이지) 시각화
* 사용자/조직 관리(회사/조직/권한)
* 주간 체크인 캘린더/리마인더
* 템플릿(OKR 예시, 산업별 가이드)
* 클라우드 데이터베이스 연동 (PostgreSQL, MySQL 등)
