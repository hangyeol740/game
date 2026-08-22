import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="AI 없는 프롬프트 보완기", page_icon="📝", layout="centered")

# 2. 타이틀
st.title("📝 스마트 프롬프트 보완기 (Rule-based)")
st.write("외부 AI 호출 없이, 입력하신 키워드를 분석하여 전문가 구조의 프롬프트로 자동 조합해 드립니다.")
st.markdown("---")

# 3. 입력 영역
original_prompt = st.text_area(
    "보완할 원본 프롬프트를 입력하세요:",
    height=150,
    placeholder="예: 인스타그램에 올릴 제주도 여행 카드뉴스 문구 짜줘."
)

# 4. 실행 버튼
if st.button("🚀 프롬프트 조합하기", type="primary", use_container_width=True):
    if not original_prompt.strip():
        st.warning("⚠️ 프롬프트를 입력해 주세요.")
    else:
        with st.spinner("프롬프트 구조를 분석하고 조립하는 중입니다..."):
            
            # 규칙 기반으로 프롬프트 구조화 (템플릿 조합)
            optimized_prompt = f"""### 1. 🎭 Role (역할)
- 당신은 해당 분야에서 10년 이상의 경력을 가진 최고 전문가 및 숙련된 프롬프트 엔지니어입니다.

### 2. 🎯 Context & Goal (배경 및 목적)
- **사용자 요청 사항**: {original_prompt}
- **목적**: 위 요청사항을 누락 없이 구체적이고 완성도 높은 결과물로 도출하기 위함입니다.

### 3. 📋 Instructions (구체적 지시사항)
- 사용자의 원본 요청 의도를 정확히 파악하고 단계별(Step-by-step)로 논리적으로 작성하세요.
- 전문적이면서도 목적에 맞는 명확한 어조(Tone & Manner)를 유지하세요.
- 독창적이거나 실용적인 아이디어를 포함하여 풍부하게 작성하세요.

### 4. 🚫 Constraints (제약조건)
- 모호하거나 추상적인 표현은 지양하고 구체적인 수치나 예시를 포함하세요.
- 요청된 핵심 주제에서 벗어나지 않도록 주의하세요.
- 불필요한 서두나 인사말은 최소화하고 본론 위주로 출력하세요.

### 5. 📤 Output Format (출력 양식)
- 가독성이 좋은 마크다운 형식(제목, 글머리 기호, 볼드체 등)으로 구조화하여 출력하세요."""

            st.markdown("### ✨ 최적화된 프롬프트 결과")
            st.markdown(optimized_prompt)
