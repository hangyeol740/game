import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="AI 프롬프트 보완기", page_icon="⚡", layout="centered")

# 2. Streamlit Secrets에서 Groq API Key 가져오기
api_key = st.secrets.get("GROQ_API_KEY", "")

# 3. 타이틀
st.title("⚡ AI 프롬프트 보완기 (Groq 무료버전)")
st.write("아이디어를 입력하면, 초고속 Groq AI가 가장 최적화된 구조의 프롬프트로 변환해 드립니다.")
st.markdown("---")

# 4. 입력 영역
original_prompt = st.text_area(
    "보완할 원본 프롬프트를 입력하세요:",
    height=150,
    placeholder="예: 인스타그램에 올릴 제주도 여행 카드뉴스 문구 짜줘."
)

# 5. 실행 버튼
if st.button("🚀 프롬프트 보완하기", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ Streamlit Secrets에 GROQ_API_KEY가 설정되어 있지 않습니다.")
    elif not original_prompt.strip():
        st.warning("⚠️ 프롬프트를 입력해 주세요.")
    else:
        try:
            # Groq API는 OpenAI SDK와 호환되며 base_url을 변경하여 사용합니다.
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            
            with st.spinner("AI가 프롬프트를 분석하고 최적화하는 중입니다..."):
                system_prompt = """
                너는 최고 수준의 Prompt Engineer야. 사용자의 원본 프롬프트를 분석하여 아래 5가지 구조로 재구성해줘.
                1. 🎭 Role (역할)
                2. 🎯 Context & Goal (배경 및 목적)
                3. 📋 Instructions (구체적 지시사항)
                4. 🚫 Constraints (제약조건)
                5. 📤 Output Format (출력 양식)
                
                결과는 깔끔한 마크다운 형식으로 출력해줘.
                """
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"원본 프롬프트: {original_prompt}"}
                    ],
                    temperature=0.7
                )
                
                result = response.choices[0].message.content
                
                st.markdown("### ✨ 최적화된 프롬프트 결과")
                st.markdown(result)
                
        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {e}")
