import streamlit as st
import random

# 페이지 설정 (반응형 레이아웃)
st.set_page_config(
    page_title="모험가 이야기 (Life in Adventure)",
    page_icon="📜",
    layout="centered"
)

# ---------------------------------------------------------
# 💡 [성공 확률 계산 함수]
# D20 주사위(1~20) + 현재 스탯 >= 난이도 조건을 만족할 확률(%) 계산
# ---------------------------------------------------------
def calculate_success_rate(stat_value, difficulty):
    required_dice = difficulty - stat_value # 성공을 위해 필요한 최소 주사위 눈금
    
    if required_dice <= 1:
        return 100  # 1만 나와도 성공하는 경우 (100%)
    elif required_dice > 20:
        return 0    # 20이 나와도 실패하는 경우 (0%)
    else:
        # 성공할 수 있는 주사위 눈금의 개수 비율 계산
        winning_rolls = 20 - required_dice + 1
        return int((winning_rolls / 20) * 100)

# ---------------------------------------------------------
# 1. 게임 세션 상태 및 데이터 초기화
# ---------------------------------------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False  # 캐릭터 생성 전 상태

JOBS = {
    "전사": {
        "desc": "강한 체력과 힘으로 정면 돌파하는 파괴자",
        "weapon": "강철 대검",
        "armor": "사슬 갑옷",
        "base_hp": 120,
        "base_stats": {"str": 12, "dex": 8, "int": 8, "cha": 8}
    },
    "도적": {
        "desc": "재빠른 손놀림과 민첩함으로 위기를 탈출하는 자",
        "weapon": "독 바른 단검",
        "armor": "가죽 갑옷",
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
        "weapon": "신성 메이스",
        "armor": "사제 의복",
        "base_hp": 100,
        "base_stats": {"str": 9, "dex": 7, "int": 10, "cha": 12}
    }
}

EVENTS = [
    {
        "id": "goblin_ambush",
        "title": "📜 숲속의 고블린 습격",
        "desc": "수풀 속에서 굶주린 고블린 무리가 기습했습니다!",
        "choices": [
            {
                "text": "⚔️ 무기를 휘둘러 정면 대결",
                "stat": "str",
                "diff": 15,
                "succ": "고블린들을 쫓아내고 소지품을 털었습니다! (+25 Gold)",
                "fail": "고블린의 협공에 부상을 입었습니다. (-20 체력)",
                "succ_gold": 25, "fail_hp": 20
            },
            {
                "text": "🎯 수풀 사이로 신속하게 회피",
                "stat": "dex",
                "diff": 13,
                "succ": "날렵한 몸짓으로 기습을 피하고 무사히 탈출했습니다.",
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
                "text": "🧠 고대 고문자를 해석해본다",
                "stat": "int",
                "diff": 16,
                "succ": "비문을 해독하여 고대의 지혜와 숨겨진 금화를 발견했습니다! (+40 Gold)",
                "fail": "머리가 지끈거리며 아무것도 해석하지 못했습니다.",
                "succ_gold": 40
            },
            {
                "text": "✨ 석상 앞에서 정성스럽게 기도한다",
                "stat": "cha",
                "diff": 12,
                "succ": "석상에서 따뜻한 빛이 나와 상처를 치료합니다. (+30 체력 회복)",
                "fail": "아무런 일도 일어나지 않았습니다.",
                "succ_hp": 30
            }
        ]
    }
]

def next_event():
    st.session_state.current_event = random.choice(EVENTS)
    st.session_state.stage = "이벤트"

# ---------------------------------------------------------
# 2. [캐릭터 생성 화면]
# ---------------------------------------------------------
if not st.session_state.game_started:
    st.title("📜 모험가 생성 (Character Creation)")
    st.subheader("당신의 모험가를 만들어주세요")

    job_choice = st.selectbox("🎭 직업 선택", list(JOBS.keys()))
    job_info = JOBS[job_choice]
    
    st.info(f"**{job_choice}**: {job_info['desc']}\n\n"
            f"🗡️ **무기:** {job_info['weapon']} | 🛡️ **방어구:** {job_info['armor']} | ❤️ **체력:** {job_info['base_hp']}")

    st.divider()
    st.write("📊 **추가 능력치 포인트 분배 (총 10 pt)**")

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
        st.error(f"⚠️ 보너스 포인트를 초과했습니다! ({abs(remaining_points)}pt 초과)")
    else:
        st.success(f"남은 포인트: **{remaining_points} pt**")
        
        if st.button("🚀 모험 시작하기", use_container_width=True):
            st.session_state.job = job_choice
            st.session_state.weapon = job_info["weapon"]
            st.session_state.armor = job_info["armor"]
            st.session_state.hp = job_info["base_hp"]
            st.session_state.max_hp = job_info["base_hp"]
            st.session_state.gold = 30
            
            st.session_state.str = job_info["base_stats"]["str"] + add_str
            st.session_state.dex = job_info["base_stats"]["dex"] + add_dex
            st.session_state.int = job_info["base_stats"]["int"] + add_int
            st.session_state.cha = job_info["base_stats"]["cha"] + add_cha
            
            st.session_state.game_started = True
            next_event()
            st.rerun()

# ---------------------------------------------------------
# 3. [메인 게임 화면] (사이드바 + 확률 표시 적용)
# ---------------------------------------------------------
else:
    # 👈 [왼쪽 사이드바] 스탯, 인벤토리, 상태창 구현
    with st.sidebar:
        st.header("👤 모험가 프로필")
        st.write(f"**직업:** {st.session_state.job}")
        st.write(f"❤️ **체력:** {st.session_state.hp} / {st.session_state.max_hp}")
        st.write(f"💰 **골드:** {st.session_state.gold} G")
        
        st.divider()
        st.header("🎒 인벤토리 (장비)")
        st.write(f"🗡️ **무기:** {st.session_state.weapon}")
        st.write(f"🛡️ **방어구:** {st.session_state.armor}")
        
        st.divider()
        st.header("📊 능력치 (Stats)")
        st.write(f"⚔️ **근력 (STR):** {st.session_state.str}")
        st.write(f"🎯 **민첩 (DEX):** {st.session_state.dex}")
        st.write(f"🧠 **지능 (INT):** {st.session_state.int}")
        st.write(f"✨ **매력 (CHA):** {st.session_state.cha}")

    # 메인 중앙 화면
    st.title("📜 모험가 이야기")

    # [A] 게임 오버
    if st.session_state.hp <= 0:
        st.error("💀 체력이 다해 쓰러졌습니다... 모험이 끝났습니다.")
        if st.button("🔄 새로운 모험가로 다시 시작", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()

    # [B] 이벤트 진행 화면
    elif st.session_state.stage == "이벤트":
        ev = st.session_state.current_event
        st.subheader(ev["title"])
        st.info(ev["desc"])
        
        st.write("---")
        st.write("👉 **당신의 행동을 선택하세요:**")
        
        for idx, choice in enumerate(ev["choices"]):
            stat_key = choice["stat"]
            p_stat = getattr(st.session_state, stat_key)
            stat_name = {"str": "근력", "dex": "민첩", "int": "지능", "cha": "매력"}[stat_key]
            
            # 🎲 [실시간 성공 확률 계산]
            chance = calculate_success_rate(p_stat, choice["diff"])
            
            # 선택지 버튼 레이블에 [스탯 / 난이도 / 성공확률%] 명시
            btn_text = f"{choice['text']}  [{stat_name} | 난이도 {choice['diff']} | 성공 확률: {chance}%]"
            
            if st.button(btn_text, key=f"c_{idx}", use_container_width=True):
                dice = random.randint(1, 20)
                total = p_stat + dice
                
                # 판정 성공 조건
                if total >= choice["diff"]:
                    msg = f"🎲 주사위({dice}) + 능력치({p_stat}) = **{total}** (난이도 {choice['diff']}) ➡️ **[성공!]**\n\n"
                    msg += choice["succ"]
                    
                    st.session_state.gold += choice.get("succ_gold", 0)
                    st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + choice.get("succ_hp", 0))
                    
                    # 성공 시 15% 확률로 해당 스탯 성장
                    if random.random() < 0.15:
                        setattr(st.session_state, stat_key, p_stat + 1)
                        msg += f"\n\n✨ **[스탯 상승!]** 모험을 통해 **{stat_name}** 이(가) 1 올랐습니다!"
                else:
                    msg = f"🎲 주사위({dice}) + 능력치({p_stat}) = **{total}** (난이도 {choice['diff']}) ➡️ **[실패...]**\n\n"
                    msg += choice["fail"]
                    
                    st.session_state.hp -= choice.get("fail_hp", 0)
                    
                st.session_state.log = msg
                st.session_state.stage = "결과"
                st.rerun()

    # [C] 결과 출력 화면
    elif st.session_state.stage == "결과":
        st.subheader("📜 행동 결과")
        if "[성공!]" in st.session_state.log:
            st.success(st.session_state.log)
        else:
            st.warning(st.session_state.log)
            
        if st.button("▶️ 다음 모험 계속하기", use_container_width=True):
            next_event()
            st.rerun()
