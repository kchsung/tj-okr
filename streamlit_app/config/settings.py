from __future__ import annotations
import os
import streamlit as st
from dataclasses import dataclass
from dotenv import load_dotenv

# 로컬 개발 환경에서만 .env 파일 로드
if os.path.exists(".env"):
    load_dotenv()

@dataclass(frozen=True)
class Settings:
    # Streamlit Cloud에서는 환경변수나 secrets를 사용
    db_url: str = os.getenv("DB_URL", "sqlite:///okr.db")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5-nano")
    
    @property
    def openai_api_key(self) -> str:
        """OpenAI API 키를 가져옵니다. Streamlit Cloud에서는 secrets를 우선 사용합니다."""
        # Streamlit Cloud의 secrets.toml에서 가져오기 시도
        try:
            if hasattr(st, 'secrets') and 'openai' in st.secrets:
                return st.secrets["openai"]["api_key"]
        except Exception:
            pass
        
        # 환경변수에서 가져오기
        return os.getenv("OPENAI_API_KEY", "")

settings = Settings()
