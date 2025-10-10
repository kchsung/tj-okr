from __future__ import annotations
from typing import List, Optional
import os

# OpenAI SDK (>=1.x)
try:
    from openai import OpenAI
except Exception:  # 호환성 대비
    OpenAI = None  # type: ignore

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings

DEFAULT_MODEL = settings.openai_model

# System Prompt: 하드코딩(요청사항)
SYSTEM_PROMPT = (
    """
You are an OKR auditor for enterprises. Your job is to evaluate Objectives and Key Results against
weekly execution notes. Focus on: clarity, alignment, measurability, realism, redundancy, and traceability
from actions→results.

Return a concise, actionable review in Korean with the following sections:
1) 진단 요약 (bullets)
2) 정합성 점검 (Objective↔KR↔진행내역)
3) 수치화/측정 보완 제안 (각 KR별)
4) 다음 주 우선과제 Top 3
5) 위험요인 및 가드레일

평가는 간결하지만 구체적으로. 불필요한 장황함을 피하고, 바로 실행 가능한 문장으로 작성.
    """
)


def _client() -> Optional["OpenAI"]:
    if OpenAI is None:
        return None
    
    api_key = settings.openai_api_key
    if not api_key:
        return None
    
    # API 키 형식 검증
    if not api_key.startswith("sk-"):
        return None
        
    try:
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def validate_okr(
    objective: str,
    key_results: List[str],
    progress_notes: str,
    user_prompt: str = "",
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> str:
    """# === SYSTEM PROMPT (Daily OKR Gap-Finder, No Scoring) ===
당신은 기업용 OKR 데일리 로그의 **결함 탐지·구체화 코치**입니다. 
오직 사용자가 입력한 내용만을 근거로, 무엇이 **부족/누락/모호**한지 지적하고
다시 쓸 수 있도록 **구체적 가이드와 예시 문장**을 제공합니다. 
절대 평가점수·등급을 매기지 않습니다.

## 검토 범위 (하루 1개의 KR 로그에 한함)
필드: KR, 오늘 한 일(Action), 수치 변화(Metrics: Baseline→Today / Target + 단위, 증거 링크),
배운 점(Insight), 내일 할 일(Next 24–48h), Blocker, 상태(G/Y/R), Confidence(%), 시간(hrs),
협업자, 실험/이슈 ID

## 확인·지적 원칙
- **단일 KR 원칙**: 한 로그에 다수 KR이 섞이면 분리 제안.
- **Outcome 중심**: 산출물 나열이 아니라 지표 변화·영향이 드러나는지 확인.
- **수치 명확성**: Baseline/Today/Target, **단위**, **근거 URL**이 있는지.
- **인과성 언어**: “~인 듯”, “영향 준 것 같다”처럼 모호하면 **검증 필요**로 표시.
- **다음 액션**: 24–48시간 내 수행 가능한 **행동 단위**로 다시 쓰게 지도.
- **일관성**: 상태/Confidence와 서술 내용이 충돌하면 정렬 방안 제시.
- **사실 충실**: 추정·창작 금지. 증거 링크가 없으면 “추가 필요”만 지시.

## 출력 형식 (섹션 제목 고정, 점수/등급 금지)
1) 부족/누락 항목
   - 각 항목에 대해: **무엇이 부족한지 → 왜 중요한지 → 어떻게 보완할지(한 문장 지시)**

2) 모호·비구체 항목과 개선안
   - 각 필드별로 `원문 → 더 구체적인 예시` 형식 (가능하면 수치/단위/대상/범위 포함)

3) 다시 작성 가이드 (사용자에게 직접 지시)
   - 불릿 3–6개: **필수 기재 요소**(KR 1개, Baseline/Today/Target+단위, 증거 URL, 다음 액션을 행동 단위로 등)
   - “이렇게 쓰면 좋다” 형식의 간단 규칙

4) 다시 작성 템플릿 (복붙용, Markdown)
   - KR / 오늘 한 일 / 수치(B→T/Target + 단위) / 증거 링크 / 배운 점 / 내일 할 일(24–48h) /
     Blocker / 상태 / Confidence / 시간 / 협업자 / 실험ID

5) 확인 질문(필요 시, 최대 5개)
   - 모호 지점만 겨냥한 **예/아니오 또는 짧은 수치로 답할 질문**

## 금지 사항
- 점수/등급/평가어(예: 우수/부족/점수)를 사용 금지.
- 사용자가 쓰지 않은 데이터·링크를 상상해서 추가 금지.
- JSON을 출력할 경우 **한 개**만, 섹션 6에서만.
(끝)"""
    model = model or DEFAULT_MODEL
    client = _client()
    if client is None:
        return """
## ⚠️ OpenAI 설정 오류

OpenAI SDK가 설치되지 않았거나 API 키가 설정되지 않았습니다.

### 해결 방법:
1. **API 키 확인**: Streamlit Cloud의 "Manage app" → "Secrets"에서 `OPENAI_API_KEY` 설정 확인
2. **환경변수 확인**: `OPENAI_API_KEY` 환경변수가 올바르게 설정되었는지 확인
3. **API 키 형식**: `sk-`로 시작하는 올바른 형식인지 확인

### 임시 테스트용 피드백:
**진단 요약:**
- Objective가 명확하고 구체적임
- KR들이 실행 가능한 채널을 제시함
- 진행상황이 추적 가능함

**정합성 점검:**
- Objective와 KR들이 잘 연결되어 있음
- 수행내역이 목표 달성에 기여함

**수치화/측정 보완 제안:**
- 각 KR별 구체적인 수치 목표 설정 필요
- 진행률 측정 방법 구체화 필요

**다음 주 우선과제 Top 3:**
1. 각 채널별 구체적인 배포 수량 목표 설정
2. 배포 후 피드백 수집 방법 구축
3. 사용자 참여도 측정 지표 정의

**위험요인 및 가드레일:**
- 학생들의 관심도가 낮을 수 있음
- 배포 채널의 접근성 제한 가능성
- 피드백 수집의 어려움
        """

    user_content = (
        "# Objective\n" + objective.strip() + "\n\n" +
        "# Key Results\n- " + "\n- ".join(kr.strip() for kr in key_results if kr.strip()) + "\n\n" +
        "# Progress Notes (최근 수행내역)\n" + progress_notes.strip() + "\n\n" +
        (f"# 추가 요구사항\n{user_prompt.strip()}\n" if user_prompt.strip() else "")
    )

    # gpt-5 모델은 temperature 파라미터를 지원하지 않으므로 조건부로 처리
    use_temperature = not model.startswith("gpt-5")
    
    # 우선 Responses API 시도, 실패 시 Chat Completions로 폴백
    try:
        if use_temperature:
            resp = client.responses.create(  # type: ignore
                model=model,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                temperature=temperature,
            )
        else:
            resp = client.responses.create(  # type: ignore
                model=model,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
            )
        # SDK 1.x Responses 출력 포맷 가정
        txt = resp.output_text  # type: ignore[attr-defined]
        if txt:
            return txt
    except Exception:
        pass

    # Fallback: Chat Completions
    try:
        if use_temperature:
            resp = client.chat.completions.create(  # type: ignore
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                temperature=temperature,
            )
        else:
            resp = client.chat.completions.create(  # type: ignore
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
            )
        return resp.choices[0].message.content or ""
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg:
            return """
## ⚠️ OpenAI API 키 설정이 필요합니다

현재 API 키가 설정되지 않았거나 잘못되었습니다.

### 해결 방법:
1. [OpenAI Platform](https://platform.openai.com/api-keys)에서 API 키 발급
2. `.env` 파일에서 `OPENAI_API_KEY=your_actual_key_here`로 수정
3. 앱 재시작

### 임시 테스트용 피드백:
**진단 요약:**
- Objective가 명확하고 구체적임
- KR들이 실행 가능한 채널을 제시함
- 진행상황이 추적 가능함

**정합성 점검:**
- Objective와 KR들이 잘 연결되어 있음
- 각 KR이 목표 달성에 기여함

**수치화/측정 보완 제안:**
- KR #1: 인천대 학생 배포 수량 목표 설정 (예: 300명)
- KR #2: 수원대 학생 배포 수량 목표 설정 (예: 300명)  
- KR #3: 오픈채팅방 배포 수량 목표 설정 (예: 400명)

**다음 주 우선과제 Top 3:**
1. 각 채널별 구체적인 배포 수량 목표 설정
2. 배포 후 피드백 수집 방법 구축
3. 사용자 참여도 측정 지표 정의

**위험요인 및 가드레일:**
- 학생들의 관심도가 낮을 수 있음
- 배포 채널의 접근성 제한 가능성
- 피드백 수집의 어려움
            """
        else:
            return f"""
## ⚠️ OpenAI API 호출 오류

API 호출 중 오류가 발생했습니다: {error_msg}

### 해결 방법:
1. **API 키 확인**: Streamlit Cloud의 "Manage app" → "Secrets"에서 `OPENAI_API_KEY` 설정 확인
2. **API 키 형식**: `sk-`로 시작하는 올바른 형식인지 확인
3. **API 사용량**: OpenAI 계정의 사용량 한도 확인
4. **네트워크 연결**: 인터넷 연결 상태 확인

### 임시 테스트용 피드백:
**진단 요약:**
- Objective가 명확하고 구체적임
- KR들이 실행 가능한 채널을 제시함
- 진행상황이 추적 가능함

**정합성 점검:**
- Objective와 KR들이 잘 연결되어 있음
- 수행내역이 목표 달성에 기여함

**수치화/측정 보완 제안:**
- 각 KR별 구체적인 수치 목표 설정 필요
- 진행률 측정 방법 구체화 필요

**다음 주 우선과제 Top 3:**
1. 각 채널별 구체적인 배포 수량 목표 설정
2. 배포 후 피드백 수집 방법 구축
3. 사용자 참여도 측정 지표 정의

**위험요인 및 가드레일:**
- 학생들의 관심도가 낮을 수 있음
- 배포 채널의 접근성 제한 가능성
- 피드백 수집의 어려움
            """
