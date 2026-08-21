import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="AI 프롬프트 보완기", page_icon="🪄", layout="wide")

# 2. Streamlit Secrets에서 API Key 가져오기
api_key = st.secrets.get("OPENAI_API_KEY")

# 세션 상태 초기화 (대화 기록 및 보완 내역 유지)
if "enhanced_result" not in st.session_state:
    st.session_state.enhanced_result = None
if "original_prompt" not in st.session_state:
    st.session_state.original_prompt = ""

# ---------------------------------------------------------
# 사이드바: 설정 및 직접 피드백 기능
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ API 상태")
    if api_key:
        st.success("🔑 API Key 연동 완료")
    else:
        st.error("⚠️ Streamlit Secrets에 OPENAI_API_KEY를 설정해주세요!")
        
    st.markdown("---")
    st.header("💬 프롬프트 피드백 & 수정")
    st.caption("AI가 만든 프롬프트가 목적과 다르면, 아래에 직접 피드백을 적고 다시 수정해보세요!")
    
    feedback_text = st.text_area(
        "피드백 / 추가 요구사항", 
        placeholder="예: '출력 형식을 JSON 표로 바꿔줘', '조금 더 격식 있는 톤으로 수정해줘'",
        height=120
    )
    
    refine_button = st.button("🔄 피드백 반영해서 재보완하기", use_container_width=True)

# ---------------------------------------------------------
# AI 호출 함수
# ---------------------------------------------------------
def enhance_prompt(client, original_prompt, feedback=""):
    system_instruction = """
    너는 세계 최고 수준의 Prompt Engineer야.
    사용자가 입력한 원본 프롬프트(및 피드백)를 분석하여 AI가 가장 정확하고 효율적으로 답변할 수 있는 프롬프트로 재구성해줘.

    [작업 가이드라인]
    1. 사용자의 원본 프롬프트에서 '진짜 목적(Intent)'을 먼저 간결하게 파악할 것.
    2. 완성된 프롬프트는 아래 5가지 구조를 명확히 맞춰서 작성할 것:
       - 🎭 Role (역할): AI가 가져야 할 페르소나
       - 🎯 Context & Goal (배경 및 목적): 수행해야 할 핵심 목표
       - 📋 Instructions (구체적 지시사항): 단계별 가이드라인
       - 🚫 Constraints (제약조건): 금지사항 또는 규칙
       - 📤 Output Format (출력 양식): 원문/표/코드 등 답변의 형식
    
    [응답 형식]
    반드시 아래 형식으로 작성해줘:

    ### 🎯 파악된 핵심 목적
    (사용자가 이 프롬프트를 통해 달성하고자 하는 목적 한 줄 요약)

    ---

    ### ✨ 보완된 최종 프롬프트
    ```
    (보완된 프롬프트 내용 전체)
    ```

    ---

    ### 💡 주요 보완 및 개선점
    (어떤 점이 강화되었는지 2~3가지 요약)
    """

    user_content = f"[원본 프롬프트]\n{original_prompt}"
    if feedback:
        user_content += f"\n\n[사용자 피드백 / 추가 요청사항]\n{feedback}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_content}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------------------------------------------------------
# 메인 화면
# ---------------------------------------------------------
st.title("🪄 AI 프롬프트 보완기 (Prompt Enhancer)")
st.write("아이디어나 대략적인 프롬프트를 입력하면, AI가 가장 이해하기 쉬운 최적의 구조로 변환해 드립니다.")

st.markdown("---")

# 1. 원본 프롬프트 입력 영역
input_prompt = st.text_area(
    "보완하고 싶은 원본 프롬프트를 입력하세요:", 
    height=150,
    placeholder="예: 인스타그램에 올릴 제주도 여행 카드뉴스 문구 짜줘."
)

col1, col2 = st.columns([1, 4])
with col1:
    generate_button = st.button("🚀 프롬프트 보완하기", type="primary", use_container_width=True)

# 2. 실행 로직 (첫 생성)
if generate_button:
    if not api_key:
        st.error("⚠️ API Key가 설정되지 않았습니다. Secrets 설정을 확인해 주세요.")
    elif not input_prompt.strip():
        st.warning("⚠️ 보완할 프롬프트를 입력해 주세요.")
    else:
        client = OpenAI(api_key=api_key)
        with st.spinner("프롬프트의 목적을 분석하고 최적화하는 중..."):
            st.session_state.original_prompt = input_prompt
            st.session_state.enhanced_result = enhance_prompt(client, input_prompt)

# 3. 실행 로직 (사이드바 피드백 반영 재생성)
if refine_button:
    if not api_key:
        st.error("⚠️ API Key가 설정되지 않았습니다.")
    elif not st.session_state.original_prompt:
        st.warning("⚠️ 먼저 메인 화면에서 프롬프트를 한 번 이상 생성해 주세요.")
    elif not feedback_text.strip():
        st.warning("⚠️ 사이드바에 피드백 내용을 입력해 주세요.")
    else:
        client = OpenAI(api_key=api_key)
        with st.spinner("피드백을 반영하여 프롬프트를 다시 다듬는 중..."):
            st.session_state.enhanced_result = enhance_prompt(
                client, 
                st.session_state.original_prompt, 
                feedback_text
            )

# 4. 결과 출력 영역
if st.session_state.enhanced_result:
    st.markdown("---")
    st.markdown(st.session_state.enhanced_result)
