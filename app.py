# ---------------------------------------------------------
# 에러 발생 시 다른 키로 자동으로 넘어가는 스마트 호출 함수
# ---------------------------------------------------------
def safe_chat_completion(prompt, temperature=0.7):
    """등록된 키들을 순회하며 성공할 때까지 시도합니다."""
    if not api_keys:
        st.error("⚠️ 등록된 API 키가 없습니다.")
        return None

    errors = []
    # 등록된 모든 키를 차례대로 시도
    for key in api_keys:
        try:
            client = OpenAI(api_key=key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            # 에러가 나면 기록하고 다음 키로 진행
            errors.append(str(e))
            continue
            
    # 모든 키가 실패했을 경우
    st.error("❌ 모든 API 키의 호출이 실패했습니다. 계정 잔액($)을 확인해 주세요.")
    return None

# ---------------------------------------------------------
# Agent 토론 로직 (자동 키 전환 적용)
# ---------------------------------------------------------
def run_agent_discussion(original_prompt):
    status_box = st.status("🤖 AI 에이전트들이 프롬프트를 두고 토론 중입니다...", expanded=True)
    
    # [1단계] Agent A: 1차 초안 작성
    status_box.write("1️⃣ **Agent A (초안 작성자)**: 원본 프롬프트를 구조화하고 있습니다...")
    prompt_a = f"""
    당신은 프롬프트 초안 작성 전문가입니다. 아래 원본 프롬프트를 분석하여 Role, Context, Instructions, Constraints, Output Format 구조로 1차 보완본을 작성하세요.
    
    [원본 프롬프트]: {original_prompt}
    """
    res_a = safe_chat_completion(prompt_a, temperature=0.7)
    if not res_a: return None
    
    # [2단계] Agent B: 초안 검토 및 비판적 피드백
    status_box.write("2️⃣ **Agent B (검수 및 비평가)**: Agent A의 초안을 검토하고 약점을 찾고 있습니다...")
    prompt_b = f"""
    당신은 깐깐한 프롬프트 검수 전문가입니다. Agent A가 작성한 초안을 보고, 부족한 점, 모호한 부분, 추가해야 할 제약조건이나 예시를 날카롭게 비판하세요.
    
    [Agent A의 초안]:
    {res_a}
    """
    res_b = safe_chat_completion(prompt_b, temperature=0.7)
    if not res_b: return None

    # [3단계] Agent C: 토론 내용 종합 및 최종 완벽 프롬프트 생성
    status_box.write("3️⃣ **Agent C (최종 중재자)**: 초안과 피드백을 종합하여 최종 완성본을 만드는 중입니다...")
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
    res_c = safe_chat_completion(prompt_c, temperature=0.5)
    if not res_c: return None

    status_box.update(label="✅ 에이전트 토론 완료!", state="complete", expanded=False)
    
    return {
        "agent_a": res_a,
        "agent_b": res_b,
        "final": res_c
    }
