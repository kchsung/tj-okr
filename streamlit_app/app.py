from __future__ import annotations
import streamlit as st
import sys
import os

# Streamlit Cloud에서 모듈 경로 문제 해결
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.components import (
    page_header, left_panel, right_panel, show_ai_feedback, show_okr_evaluation
)
from services.ai_validator import validate_okr
from config.settings import settings

# CSS 로드
css_path = os.path.join(os.path.dirname(__file__), "ui", "styles.css")
with open(css_path, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

page_header()

# 세션 상태 초기화
if 'ai_feedback' not in st.session_state:
    st.session_state.ai_feedback = ""

# 좌우 분할 레이아웃
col1, col2 = st.columns([1, 1], gap="large")

# 좌측 패널: OKR 설정
with col1:
    objective, krs, start_date, end_date, progress_percentage = left_panel()

# 우측 패널: 달력 및 수행내역
with col2:
    calendar_date, progress_content, should_validate = right_panel(ai_feedback=st.session_state.ai_feedback)

# AI 검증 처리
if should_validate and progress_content.strip():
    with st.spinner("AI가 수행내역을 검증 중입니다..."):
        # 수행내역 검증을 위한 간단한 프롬프트 구성
        user_prompt = f"다음 수행내역이 OKR 목표 달성에 기여하는지 평가해주세요: {progress_content}"
        st.session_state.ai_feedback = validate_okr(objective, krs, progress_content, user_prompt, model=settings.openai_model)
    
    # 페이지 새로고침하여 AI 검증 결과 표시
    st.rerun()

# OKR 진행 평가 표시 (좌측 하단)
with col1:
    show_okr_evaluation(objective, krs, progress_percentage)

st.caption("Made with Streamlit · OpenAI")
