import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="AI 멀티 에이전트 프롬프트 토론기", page_icon="🤖", layout="wide")

# 2. Streamlit Secrets에서 API Key 목록 가져오기
api_keys = st.secrets.get("OPENAI_API_KEYS", [])
if not api_keys and st.secrets.get("OPENAI_API_KEY"):
    api_keys = [st.secrets.get("OPENAI_API_KEY")]

# 키를 안전하게 가져오는 함수 (키가 부족하면 재사용)
def get_client(index):
    key = api_keys[index % len(api_keys)]
    return OpenAI(api_key=key)

# 세션 상태 초기화
if "discussion_history" not in st.session_state:
    st.session_state.discussion_history = None

# ---------------------------------------------------------
# 사이드바
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ API 및 에이전트 상태")
    if api_keys:
        st.success(f"🔑 {len(api_keys)}개 API 키로 멀티 에이전트 구성 완료")
    else:
        st.error("⚠️ Streamlit Secrets에 OPENAI_API_KEYS를 설정해주세요!")

# ---------------------------------------------------------
# Agent 토론 로직
# ---------------------------------------------------------
def run_agent_discussion(original_prompt):
    status_box = st.status("🤖 AI 에이전트들이 프롬프트를 두고 토론 중입니다...", expanded=True)
    
    # [1단계] Agent A: 1차 초안 작성
    status_box.write("1️⃣ **Agent A (초안 작성자)**: 원본 프롬프트를 구조화하고 있습니다...")
    client_a = get_client(0)
    prompt_a = f"""
    당신은 프롬프트 초안 작성 전문가입니다. 아래 원본 프롬프트를 분석하여 Role, Context, Instructions, Constraints, Output Format 구조로 1차 보완본을 작성하세요.
    
    [원본 프롬프트]: {original_prompt}
    """
    res_a = client_a.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_a}],
        temperature=0.7
    ).choices[0].message.content
    
    # [2단계] Agent B: 초안 검토 및 비판적 피드백
    status_box.write("2️⃣ **Agent B (검수 및 비평가)**: Agent A의 초안을 검토하고 약점을 찾고 있습니다...")
    client_b = get_client(1)
    prompt_b = f"""
    당신은 깐깐한 프롬프트 검수 전문가입니다. Agent A가 작성한 초안을 보고, 부족한 점, 모호한 부분, 추가해야 할 제약조건이나 예시를 날카롭게 비판하세요.
    
    [Agent A의 초안]:
    {res_a}
    """
    res_b = client_b.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_b}],
        temperature=0.7
    ).choices[0].message.content

    # [3단계] Agent C: 토론 내용 종합 및 최종 완벽 프롬프트 생성
    status_box.write("3️⃣ **Agent C (최종 중재자)**: 초안과 피드백을 종합하여 최종 완성본을 만드는 중입니다...")
    client_c = get_client(2)
    prompt_c = f"""
    당신은 수석 프롬프트 엔지니어입니다. 
    Agent A의 1차 초안과 Agent B의 비판적 피드백을 모두 종합하여, 완성도가 가장 높은 최종 프롬프트를 작성해주세요.

    [원본 프롬프트]: {original_prompt}
    [Agent A의 초안]: {res_a}
    [Agent B의 피드백]: {res_b}

    [출력 양식]
    ### 💬 에이전트 토론 요약
    - **Agent A 주요 의견**: (한 줄 요약)
    - **Agent B 지적 사항**: (한 줄 요약)

    ---

    ### ✨ 토론을 통해 최종 완성된 프롬프트
    ```
    (완성된 최종 프롬프트 전체)
    ```

    ---

    ### 💡 토론을 통해 개선된 핵심 포인트
    (2~3가지 요약)
    """
    res_c = client_c.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_c}],
        temperature=0.5
    ).choices[0].message.content

    status_box.update(label="✅ 에이전트 토론 완료!", state="complete", expanded=False)
    
    return {
        "agent_a": res_a,
        "agent_b": res_b,
        "final": res_c
    }

# ---------------------------------------------------------
# 메인 화면
# ---------------------------------------------------------
st.title("🤖 멀티 AI 집단지성 프롬프트 보완기")
st.write("여러 AI 에이전트(키)가 초안 작성 ➔ 비판/검수 ➔ 최종 합의 과정을 거쳐 최고의 프롬프트를 만들어냅니다.")

st.markdown("---")

input_prompt = st.text_area(
    "보완하고 싶은 원본 프롬프트를 입력하세요:", 
    height=150,
    placeholder="예: 인스타그램에 올릴 제주도 여행 카드뉴스 문구 짜줘."
)

if st.button("🚀 AI 에이전트 토론 시작하기", type="primary", use_container_width=True):
    if not api_keys:
        st.error("⚠️ Secrets에 API 키를 설정해주세요!")
    elif not input_prompt.strip():
        st.warning("⚠️ 프롬프트를 입력해 주세요.")
    else:
        st.session_state.discussion_history = run_agent_discussion(input_prompt)

# 결과 및 토론 과정 출력
if st.session_state.discussion_history:
    results = st.session_state.discussion_history
    
    st.markdown("---")
    st.markdown(results["final"])
    
    # AI들의 내부 토론 과정을 펼쳐볼 수 있는 탭 제공
    with st.expander("🔍 AI 에이전트들의 상세 토론 과정 보기"):
        tab1, tab2 = st.tabs(["1차 초안 (Agent A)", "검수 및 피드백 (Agent B)"])
        with tab1:
            st.markdown(results["agent_a"])
        with tab2:
            st.markdown(results["agent_b"])
