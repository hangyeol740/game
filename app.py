import streamlit as st
import random

# 페이지 설정 (반응형 레이아웃)
st.set_page_config(
    page_title="모험가 이야기 (Life in Adventure)",
    page_icon="📜",
    layout="centered"
)

# ---------------------------------------------------------
# 1. 게임 세션 상태 초기화
# ---------------------------------------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False  # 캐릭터 생성 전

# 직업 정보 정의 (시작 장비, 기본 스탯, 직업 설명)
JOBS = {
    "전사": {
        "desc": "강한 체력과 힘으로 정면 돌파하는 영웅",
        "weapon": "강철 대검",
        "armor": "사슬 갑옷",
        "base_hp": 120,
        "base_stats": {"str": 12, "dex": 8, "int": 8, "cha": 8}
    },
    "도적": {
        "desc": "재빠른 손놀림과 민첩함으로 위기를 탈출하는 자",
        "weapon": "독 바른 단검",
        "armor": "가죽 가포",
        "base_hp": 90,
        "base_stats": {"str": 8, "dex": 13, "int": 9, "cha": 8}
    },
    "마법사": {
        "desc": "높은 지능과 마법으로 사건을 해결하는 연구자",
        "weapon": "수습 지팡이",
        "armor": "마법사 로브",
        "base_hp": 80,
        "base_stats": {"str": 7, "dex": 8, "int": 14, "cha": 9}
    },
    "사제": {
        "desc": "뛰어난 매력과 신성한 힘으로 사람들을 인도하는 자",
        "weapon": "메이스",
        "armor": "사제 의복",
        "base_hp": 100,
        "base_stats": {"str": 9, "dex": 7, "int": 10, "cha": 12}
    }
}

# ---------------------------------------------------------
# 2. [단계 1] 캐릭터 생성 및 스탯 분배 화면
# ---------------------------------------------------------
if not st.session_state.game_started:
    st.title("📜 모험가 생성 (Character Creation)")
    st.subheader("당신의 모험가를 설정하세요")

    # [1] 직업 선택
    job_choice = st.selectbox("🎭 직업을 선택하세요", list(JOBS.keys()))
    job_info = JOBS[job_choice]
    
    st.info(f"**{job_choice}**: {job_info['desc']}\n\n"
            f"🗡️ **시작 무기:** {job_info['weapon']} | 🛡️ **시작 방어구:** {job_info['armor']} | ❤️ **기본 체력:** {job_info['base_hp']}")

    st.divider()
    st.write("📊 **추가 능력치 포인트 분배 (남은 포인트: 총 10 pt)**")
    st.caption("※ 모험가 이야기에서는 스탯 올리기가 매우 어렵습니다. 초기 분배가 중요합니다!")

    # [2] 스탯 포인트 투자 (슬라이더 사용)
    # 총 보너스 포인트 10을 초과하지 않도록 제한
    c1, c2 = st.columns(2)
    with c1:
        add_str = st.number_input("⚔️ 근력 (STR)", min_value=0, max_value=10, value=2)
        add_dex = st.number_input("🎯 민첩 (DEX)", min_value=0, max_value=10, value=2)
    with c2:
        add_int = st.number_input("🧠 지능 (INT)", min_value=0, max_value=10, value=2)
        add_cha = st.number_input("✨ 매력 (CHA)", min_value=0, max_value=10, value=4)

    used_points = add_str + add_dex + add_int + add_cha
    remaining_points = 10 - used_points

    if remaining_points < 0:
        st.error(f"⚠️ 사용 가능한 보너스 포인트를 초과했습니다! ({abs(remaining_points)}pt 초과)")
    else:
        st.success(f"남은 보너스 포인트: **{remaining_points} pt**")
        
        if st.button("🚀 이 설정으로 모험 시작하기", use_container_width=True):
            # 게임 데이터 세션에 저장
            st.session_state.job = job_choice
            st.session_state.weapon = job_info["weapon"]
            st.session_state.armor = job_info["armor"]
            st.session_state.hp = job_info["base_hp"]
            st.session_state.max_hp = job_info["base_hp"]
            st.session_state.gold = 30
            
            # 최종 스탯 = 기본 스탯 + 투자 스탯
            st.session_state.str = job_info["base_stats"]["str"] + add_str
            st.session_state.dex = job_info["base_stats"]["dex"] + add_dex
            st.session_state.int = job_info["base_stats"]["int"] + add_int
            st.session_state.cha = job_info["base_stats"]["cha"] + add_cha
            
            st.session_state.log = f"{job_choice}(으)로 모험을 시작합니다. [{job_info['weapon']}]을(를) 장착했습니다."
            st.session_state.stage = "이벤트"
            st.session_state.game_started = True
            st.rerun()

# ---------------------------------------------------------
# 3. [단계 2] 메인 게임 화면 (이벤트 및 어려운 스탯 성장)
# ---------------------------------------------------------
else:
    # 이벤트 카드가 정의되어 있지 않다면 설정
    EVENTS = [
        {
            "id": "goblin_ambush",
            "title": "📜 숲속의 고블린 기습",
            "desc": "수풀 속에서 고블린 무리가 기습했습니다!",
            "choices": [
                {
                    "text": "⚔️ 무기를 휘둘러 정면 대결",
                    "stat": "str",
                    "diff": 14,
                    "succ": "시작 무기를 활용해 고블린들을 물리쳤습니다! (+20 Gold)",
                    "fail": "고블린의 협공에 부상을 입었습니다. (-20 체력)",
                    "succ_gold": 20, "fail_hp": 20
                },
                {
                    "text": "🎯 신속하게 숲속으로 재빠르게 회피",
                    "stat": "dex",
                    "diff": 13,
                    "succ": "날렵한 몸짓으로 기습을 피하고 탈출했습니다.",
                    "fail": "발이 엉켜 넘어져 다쳤습니다. (-15 체력)",
                    "fail_hp": 15
                }
            ]
        },
        {
            "id": "ancient_statue",
            "title": "📜 고대의 모험가 석상",
            "desc": "이끼 낀 오래된 모험가의 석상이 비밀스러운 비문을 품고 있습니다.",
            "choices": [
                {
                    "text": "🧠 고대 고문자를 해석한다",
                    "stat": "int",
                    "diff": 15,
                    "succ": "비문을 해독하여 고대의 지혜를 깨달았습니다!",
                    "fail": "머리가 지끈거리며 아무것도 얻지 못했습니다.",
                },
                {
                    "text": "✨ 석상 앞에서 정성스럽게 기도한다",
                    "stat": "cha",
                    "diff": 12,
                    "succ": "석상에서 따뜻한 빛이 나와 상처를 치료해 줍니다. (+25 체력 회복)",
                    "fail": "아무런 일도 일어나지 않았습니다.",
                    "succ_hp": 25
                }
            ]
        }
    ]

    def next_event():
        st.session_state.current_event = random.choice(EVENTS)
        st.session_state.stage = "이벤트"

    if "current_event" not in st.session_state:
        next_event()

    # 상단 플레이어 프로필 UI
    st.title(f"📜 모험가 이야기 ({st.session_state.job})")
    
    # 1줄: 체력, 골드, 장비 정보
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("❤️ 체력", f"{st.session_state.hp}/{st.session_state.max_hp}")
    m2.metric("💰 골드", f"{st.session_state.gold} G")
    m3.metric("🗡️ 무기", st.session_state.weapon)
    m4.metric("🛡️ 방어구", st.session_state.armor)

    # 2줄: 능력치 (스탯)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("⚔️ 근력(STR)", st.session_state.str)
    s2.metric("🎯 민첩(DEX)", st.session_state.dex)
    s3.metric("🧠 지능(INT)", st.session_state.int)
    s4.metric("✨ 매력(CHA)", st.session_state.cha)

    st.divider()

    # [A] 게임 오버
    if st.session_state.hp <= 0:
        st.error("💀 쓰러졌습니다... 당신의 모험은 여기서 끝납니다.")
        if st.button("🔄 새로운 캐릭터 만들기", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()

    # [B] 이벤트 진행 화면
    elif st.session_state.stage == "이벤트":
        ev = st.session_state.current_event
        st.subheader(ev["title"])
        st.info(ev["desc"])
        
        st.write("👉 **행동 선택:**")
        
        for idx, choice in enumerate(ev["choices"]):
            stat_key = choice["stat"]
            stat_name = {"str": "근력", "dex": "민첩", "int": "지능", "cha": "매력"}[stat_key]
            btn_text = f"{choice['text']}  [{stat_name} 판정 / 난이도 {choice['diff']}]"
            
            if st.button(btn_text, key=f"c_{idx}", use_container_width=True):
                # 주사위 D20 시스템
                dice = random.randint(1, 20)
                p_stat = getattr(st.session_state, stat_key)
                total = p_stat + dice
                
                # 결과 판단
                if total >= choice["diff"]:
                    msg = f"🎲 주사위({dice}) + 능력치({p_stat}) = **{total}** (난이도 {choice['diff']}) ➡️ **판정 성공!**\n\n"
                    msg += choice["succ"] + "\n\n"
                    
                    # 보상 적용
                    st.session_state.gold += choice.get("succ_gold", 0)
                    st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + choice.get("succ_hp", 0))
                    
                    # 💡 스탯 성장 시스템 (하드코어: 성공 시 15% 확률로만 해당 스탯 +1 상승)
                    if random.random() < 0.15:
                        setattr(st.session_state, stat_key, p_stat + 1)
                        msg += f"\n\n✨ **[스탯 성장!]** 모험을 통해 **{stat_name}** 이(가) 1 상승했습니다! ({p_stat} ➡️ {p_stat + 1})"
                        
                else:
                    msg = f"🎲 주사위({dice}) + 능력치({p_stat}) = **{total}** (난이도 {choice['diff']}) ➡️ **판정 실패...**\n\n"
                    msg += choice["fail"]
                    
                    st.session_state.hp -= choice.get("fail_hp", 0)
                    
                st.session_state.log = msg
                st.session_state.stage = "결과"
                st.rerun()

    # [C] 판정 결과 화면
    elif st.session_state.stage == "결과":
        st.subheader("📜 판정 결과")
        if "성공" in st.session_state.log:
            st.success(st.session_state.log)
        else:
            st.warning(st.session_state.log)
            
        if st.button("▶️ 다음 모험으로 이동", use_container_width=True):
            next_event()
            st.rerun()
