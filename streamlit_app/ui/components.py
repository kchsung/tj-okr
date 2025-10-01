from __future__ import annotations
import streamlit as st
from typing import List, Optional
from datetime import datetime, date, timedelta

PRIMARY_BTN = {"use_container_width": True}


def page_header():
    st.markdown("""
        <div class="header">
          <h2>OKR Mini Program</h2>
          <p>간단한 OKR 관리 + AI 검증</p>
        </div>
    """, unsafe_allow_html=True)


def left_panel() -> tuple[str, List[str], date, date, float]:
    """좌측 패널: OKR 입력 및 기간 설정"""
    st.subheader("📋 OKR 설정")
    
    # 기본값 설정
    default_objective = "큐런 베타 서비스를 대학생 취준생 대상 1000명을 확보 후 서비스 사용성 측면, 문제 퀄리티(문제 난이도, 문제 유형, 문제 품질), 평가 결과 측면(사용자가 납득할만한 평가가 있는지, 사용자에게 유용한 평가를 하는지)를 받을 것"
    default_krs = [
        "인천스타트업 파크를 통한 인천대 학생 배포",
        "수원대 교수님을 통한 수원대 학생 배포", 
        "대학생 취업준비생이 많이 있는 카페나, 오픈채팅방에 배포"
    ]
    
    objective = st.text_input("🎯 Objective", value=default_objective, help="달성하고자 하는 목표를 명확하게 작성하세요")
    
    st.subheader("📊 Key Results")
    kr_count = st.number_input("KR 개수", min_value=1, max_value=10, value=3, step=1)
    krs: List[str] = []
    for i in range(int(kr_count)):
        default_kr = default_krs[i] if i < len(default_krs) else ""
        krs.append(st.text_input(f"KR #{i+1}", key=f"kr_{i}", value=default_kr, placeholder="예) 2주 체험 전환율 ≥ 12%"))
    
    st.subheader("📅 OKR 기간")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작일", value=date.today(), help="OKR 시작 날짜")
    with col2:
        end_date = st.date_input("종료일", value=date.today() + timedelta(days=90), help="OKR 종료 날짜")
    
    st.subheader("📈 진행률")
    progress_percentage = st.slider("전체 진행률 (%)", 0, 100, 25, help="현재까지의 전체 진행률")
    
    # 진행바 표시
    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>진행률</span>
            <span><strong>{progress_percentage}%</strong></span>
        </div>
        <div class="progress-bar" style="width: {progress_percentage}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    return objective, krs, start_date, end_date, progress_percentage


def right_panel(selected_date: Optional[date] = None, ai_feedback: str = ""):
    """우측 패널: 달력 및 수행내역"""
    st.subheader("📅 달력")
    
    # 달력 표시
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    calendar_date = st.date_input("날짜 선택", value=selected_date or date.today(), help="수행내역을 확인할 날짜를 선택하세요")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 선택된 날짜의 수행내역
    st.subheader(f"📝 {calendar_date} 수행내역")
    
    # 수행내역 입력/수정
    progress_content = st.text_area(
        "오늘의 수행내역", 
        placeholder="오늘 진행한 작업과 성과를 입력하세요...",
        height=150,
        key=f"progress_{calendar_date}"
    )
    
    # AI 검증 버튼
    should_validate = False
    if st.button("🤖 AI에 피드백받기", type="primary", **PRIMARY_BTN):
        if progress_content.strip():
            should_validate = True
        else:
            st.warning("수행내역을 입력해주세요.")
    
    # 기존 수행내역 표시 (임시 데이터)
    if calendar_date == date.today():
        st.markdown("""
        <div class="progress-card">
            <h4>오늘의 수행내역</h4>
            <p>AI관련 오픈채팅방 리서치를 진행했습니다. 총 15개 채팅방을 조사하고, 
            대학생들이 많이 활동하는 채널 3개를 식별했습니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI 검증 결과 표시
    if ai_feedback:
        st.subheader("🤖 AI 검증 결과")
        st.markdown(f"""
        <div class="ai-feedback">
            {ai_feedback}
        </div>
        """, unsafe_allow_html=True)
    
    return calendar_date, progress_content, should_validate


def show_ai_feedback(text: str):
    """AI 검증 결과 표시"""
    st.markdown(f"""
    <div class="ai-feedback">
        <h4>🤖 AI 검증 결과</h4>
        {text}
    </div>
    """, unsafe_allow_html=True)


def show_okr_evaluation(objective: str, krs: List[str], progress_percentage: float):
    """OKR 목표 대비 현재 진행 상황 AI 평가"""
    st.subheader("📊 OKR 진행 평가")
    
    # 간단한 평가 로직 (실제로는 AI를 통해 평가)
    if progress_percentage >= 80:
        status = "🟢 우수"
        message = "목표 달성을 위한 진행이 매우 좋습니다!"
    elif progress_percentage >= 50:
        status = "🟡 보통"
        message = "목표 달성을 위해 더 집중이 필요합니다."
    else:
        status = "🔴 주의"
        message = "목표 달성을 위해 전략 재검토가 필요합니다."
    
    st.markdown(f"""
    <div class="progress-card">
        <h4>현재 상태: {status}</h4>
        <p>{message}</p>
        <p><strong>전체 진행률:</strong> {progress_percentage}%</p>
    </div>
    """, unsafe_allow_html=True)


# 기존 함수들 (호환성 유지)
def objective_form() -> tuple[str, List[str], str, str]:
    """기존 함수 - 호환성 유지용"""
    st.subheader("1) Objective & Key Results 입력")
    
    default_objective = "큐런 베타 서비스를 대학생 취준생 대상 1000명을 확보 후 서비스 사용성 측면, 문제 퀄리티(문제 난이도, 문제 유형, 문제 품질), 평가 결과 측면(사용자가 납득할만한 평가가 있는지, 사용자에게 유용한 평가를 하는지)를 받을 것"
    default_krs = [
        "인천스타트업 파크를 통한 인천대 학생 배포",
        "수원대 교수님을 통한 수원대 학생 배포", 
        "대학생 취업준비생이 많이 있는 카페나, 오픈채팅방에 배포"
    ]
    default_progress = "AI관련 오픈채팅방 리서치"
    
    objective = st.text_input("Objective", value=default_objective)
    kr_count = st.number_input("KR 개수", min_value=1, max_value=10, value=3, step=1)
    krs: List[str] = []
    for i in range(int(kr_count)):
        default_kr = default_krs[i] if i < len(default_krs) else ""
        krs.append(st.text_input(f"KR #{i+1}", key=f"kr_{i}", value=default_kr, placeholder="예) 2주 체험 전환율 ≥ 12%"))
    progress = st.text_area("최근 수행내역(Progress Notes)", value=default_progress, height=150)
    user_prompt = st.text_area("AI 검증에 보낼 추가 요청사항(선택)", placeholder="예) 측정 가능성 강화 포인트 위주로")
    return objective, krs, progress, user_prompt


def run_validate_button() -> bool:
    return st.button("AI로 검증하기", type="primary", **PRIMARY_BTN)
