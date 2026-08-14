import streamlit as st
import random

# 페이지 기본 설정 (반응형 모바일/PC 대응)
st.set_page_config(
    page_title="모험가 이야기 (Life in Adventure)",
    page_icon="📜",
    layout="centered"
)

# ---------------------------------------------------------
# 💡 [성공 확률 계산 함수]
# D20 주사위(1~20) + 플레이어 스탯 >= 난이도 만족 확률(%)
# ---------------------------------------------------------
def calculate_success_rate(stat_value, difficulty):
    required_dice = difficulty - stat_value
    if required_dice <= 1:
        return 100  # 1만 나와도 성공 (100%)
    elif required_dice > 20:
        return 0    # 20이 나와도 실패 (0%)
    else:
        winning_rolls = 20 - required_dice + 1
        return int((winning_rolls / 20) * 100)

# ---------------------------------------------------------
# 1. 직업 데이터 (전체적으로 초기 스탯 하향 조정)
# ---------------------------------------------------------
JOBS = {
    "전사": {
        "desc": "강인한 신체로 정면 승부를 즐기는 모험가",
        "weapon": "녹슨 숏소드",
        "armor": "가죽 누비 갑옷",
        "base_hp": 100,
        "base_stats": {"str": 7, "dex": 5, "int": 4, "cha": 4}  # 스탯 하향 (기존 12 -> 7)
    },
    "도적": {
        "desc": "민첩한 움직임과 재치로 위기를 벗어나는 기회주의자",
        "weapon": "녹슨 단검",
        "armor": "천 옷",
        "base_hp": 80,
        "base_stats": {"str": 4, "dex": 7, "int": 5, "cha": 4}
    },
    "마법사": {
        "desc": "고대 지식을 연구하며 초자연적 힘을 다루는 학자",
        "weapon": "낡은 목제 지팡이",
        "armor": "여행자 로브",
        "base_hp": 70,
        "base_stats": {"str": 3, "dex": 4, "int": 8, "cha": 5}
    },
    "사제": {
        "desc": "신성한 유대로 신도의 마음을 움직이는 성직자",
        "weapon": "나무 몽둥이",
        "armor": "수녀원 사제복",
        "base_hp": 85,
        "base_stats": {"str": 5, "dex": 4, "int": 4, "cha": 7}
    }
}

# ---------------------------------------------------------
# 2. 다양하고 구체적인 이벤트 카드 데이터베이스
# ---------------------------------------------------------
EVENTS = [
    {
        "id": "goblin_ambush",
        "title": "📜 숲속의 고블린 매복",
        "desc": "울창한 숲길을 지나던 중, 나무 위와 수풀 속에서 고블린 3마리가 몽둥이를 들고 튀어나왔습니다! 놈들의 눈빛이 굶주림으로 번뜩입니다.",
        "choices": [
            {
                "text": "⚔️ 무기를 뽑아 들고 정면으로 맞서 싸운다",
                "stat": "str",
                "diff": 14,
                "succ": "무게를 실은 공격으로 고블린 두 마리를 단숨에 제압했습니다. 남은 한 마리는 기겁하며 도망쳤습니다! (+20 Gold)",
                "fail": "고블린들의 수에 눌려 여러 차례 몽둥이에 맞아 깊은 상처를 입었습니다. 겨우 내쫓았지만 피해가 큽니다. (-25 체력)",
                "succ_gold": 20, "fail_hp": 25
            },
            {
                "text": "🎯 수풀 사이 좁은 길로 날렵하게 몸을 날려 탈출한다",
                "stat": "dex",
                "diff": 13,
                "succ": "고블린들이 헛방을 치는 사이, 가시 덩굴 사이를 빠져나와 안전한 곳까지 도망쳤습니다.",
                "fail": "발이 가시 덩굴에 걸려 넘어졌습니다. 고블린들에게 얻어맞고 주머니 속 골드까지 털렸습니다. (-15 체력, -10 Gold)",
                "fail_hp": 15, "fail_gold": 10
            }
        ]
    },
    {
        "id": "injured_merchant",
        "title": "📜 습격당한 상단 마차",
        "desc": "길가에 뒤집혀 있는 마차를 발견했습니다. 마차 아래에 다리가 낀 상인이 피를 흘리며 신음하고 있습니다. 머지않아 피 냄새를 맡고 몬스터가 몰려올 것입니다.",
        "choices": [
            {
                "text": "⚔️ 잔해를 힘으로 들어 올려 상인을 구출한다",
                "stat": "str",
                "diff": 15,
                "succ": "무거운 마차 잔해를 들어 올려 상인을 구했습니다! 상인은 눈물을 흘리며 감사의 표시로 두툼한 주머니를 건넸습니다. (+35 Gold)",
                "fail": "잔해를 들려다가 삐끗하여 근육이 찢어졌습니다. 힘을 쓰지 못해 상인도 구하지 못했습니다. (-15 체력)",
                "fail_hp": 15
            },
            {
                "text": "✨ 따뜻한 말과 지혜로 상인의 불안을 달래며 레버 원리로 구출한다",
                "stat": "cha",
                "diff": 12,
                "succ": "차분한 태도로 상인을 안심시키고 긴 나뭇가지를 활용해 무사히 구출했습니다. 상인이 보답으로 포션을 주었습니다. (+20 체력 회복)",
                "fail": "당신의 당황한 모습에 상인은 더욱 패닉에 빠졌고, 서두르다가 마차가 더 기울어 부상이 악화되었습니다.",
                "succ_hp": 20
            }
        ]
    },
    {
        "id": "ancient_ruins",
        "title": "📜 이끼 낀 고대 유적 문",
        "desc": "산자락 깊은 곳에서 고대 문명이 남긴 유적 입구를 발견했습니다. 문에는 세월의 흔적이 느껴지는 기괴한 룬 문자들이 새겨져 있습니다.",
        "choices": [
            {
                "text": "🧠 룬 문자의 법칙을 분석하여 비밀 문을 연다",
                "stat": "int",
                "diff": 16,
                "succ": "문자의 고대 마법 공식을 풀어내어 비밀 장치를 해제했습니다! 상자 안에서 고대 금화를 찾았습니다. (+50 Gold)",
                "fail": "잘못된 문자를 건드리는 바람에 환영 마법이 발동하여 마력이 엉키고 머리가 깨질 듯 아픕니다. (-20 체력)",
                "succ_gold": 50, "fail_hp": 20
            },
            {
                "text": "🎯 틈새 사이로 섬세하게 도구를 넣어 잠금장치를 해제한다",
                "stat": "dex",
                "diff": 15,
                "succ": "철사를 정밀하게 조작하여 내부 걸쇠를 빼냈습니다! 비밀 방 내부에서 보물을 챙겼습니다. (+30 Gold)",
                "fail": "도구가 부러지며 함정이 발동해 독침이 팔에 꽂혔습니다! (-25 체력)",
                "succ_gold": 30, "fail_hp": 25
            }
        ]
    },
    {
        "id": "cursed_chest",
        "title": "📜 어둠 속의 저주받은 보물상자",
        "desc": "동굴 구석에서 자줏빛 기운을 내뿜는 단단한 쇠상자를 발견했습니다. 상자 주변에는 이전 모험가들의 유골이 흩어져 있습니다.",
        "choices": [
            {
                "text": "🧠 상자에 걸린 저주 공식을 해독해 중화한다",
                "stat": "int",
                "diff": 15,
                "succ": "마법적인 결계를 차분히 해제하여 저주를 안전하게 무력화했습니다! (보상: +45 Gold)",
                "fail": "저주 해제에 실패하여 불길한 저주의 마력이 온몸에 휘감겼습니다! (-30 체력)",
                "succ_gold": 45, "fail_hp": 30
            },
            {
                "text": "✨ 강인한 신념의 힘으로 상자의 악마적 분위기를 압도한다",
                "stat": "cha",
                "diff": 14,
                "succ": "당신의 강한 정신력에 불길한 기운이 물러갔습니다. 상자가 열리며 희귀한 신성 재료가 흘러나옵니다. (+25 체력 회복)",
                "fail": "악마의 환청이 귓가에 맴돌며 정신적 충격을 받았습니다. (-15 체력)",
                "succ_hp": 25, "fail_hp": 15
            }
        ]
    },
    {
        "id": "ogre_bridge",
        "title": "📜 외나무다리를 막아선 오우거",
        "desc": "깊은 계곡을 건너는 유일한 외나무다리에 거대한 오우거가 앉아 통행료를 요구하고 있습니다. 통행료는 무려 50골드입니다!",
        "choices": [
            {
                "text": "⚔️ 거대한 오우거와 목숨을 건 사투를 벌인다",
                "stat": "str",
                "diff": 17,
                "succ": "오우거의 육중한 공격을 피하며 약점을 정확히 타격했습니다! 거구가 무너지며 통행료 주머니를 떨어뜨립니다. (+40 Gold)",
                "fail": "오우거의 거대한 주먹에 맞고 계곡 아래로 굴러떨어졌습니다. 다행히 목숨은 건졌으나 중상을 입었습니다. (-40 체력)",
                "succ_gold": 40, "fail_hp": 40
            },
            {
                "text": "✨ 화술로 오우거를 속여 무료로 지나간다",
                "stat": "cha",
                "diff": 14,
                "succ": "'뒤에서 왕국 기사단이 몰려오고 있다'고 거짓말을 하여 당황한 오우거가 다리를 비켜주게 만들었습니다.",
                "fail": "오우거는 속지 않았고, 오히려 화를 내며 당신을 다리 밖으로 걷어찼습니다! (-20 체력)",
                "fail_hp": 20
            }
        ]
    }
]

# ---------------------------------------------------------
# 3. 게임 상태 초기화 및 리셋 함수
# ---------------------------------------------------------
def reset_game():
    st.session_state.game_started = False
    st.session_state.stage = "생성"
    st.session_state.current_event = None
    st.session_state.log = ""

if "game_started" not in st.session_state:
    reset_game()

def next_event():
    st.session_state.current_event = random.choice(EVENTS)
    st.session_state.stage = "이벤트"

# ---------------------------------------------------------
# 4. [왼쪽 사이드바] 스탯, 인벤토리, 리셋 버튼
# ---------------------------------------------------------
with st.sidebar:
    st.header("📜 모험가 프로필")
    
    if st.session_state.game_started:
        st.write(f"**직업:** {st.session_state.job}")
        st.write(f"❤️ **체력:** {st.session_state.hp} / {st.session_state.max_hp}")
        st.write(f"💰 **골드:** {st.session_state.gold} G")
        
        st.divider()
        st.subheader("🎒 인벤토리")
        st.write(f"🗡️ **무기:** {st.session_state.weapon}")
        st.write(f"🛡️ **방어구:** {st.session_state.armor}")
        
        st.divider()
        st.subheader("📊 능력치 (Stats)")
        st.caption("※ 초반 능력치가 낮아 난이도가 높습니다!")
        st.write(f"⚔️ **근력 (STR):** {st.session_state.str}")
        st.write(f"🎯 **민첩 (DEX):** {st.session_state.dex}")
        st.write(f"🧠 **지능 (INT):** {st.session_state.int}")
        st.write(f"✨ **매력 (CHA):** {st.session_state.cha}")
        
        st.divider()
        # 🔄 언제든 처음부터 다시 시작 가능한 버튼
        if st.button("🔄 처음부터 다시 시작", use_container_width=True):
            reset_game()
            st.rerun()
    else:
        st.info("💡 캐릭터를 생성하면 이곳에 스탯과 인벤토리가 활성화됩니다.")

# ---------------------------------------------------------
# 5. [메인 화면 A] 캐릭터 생성 (초기 스탯 보너스 감소)
# ---------------------------------------------------------
if not st.session_state.game_started:
    st.title("📜 캐릭터 생성 (Character Creation)")
    st.write("초기 능력치가 낮아 초반 난이도가 꽤 높습니다. 신중하게 능력치를 분배하세요!")

    job_choice = st.selectbox("🎭 직업 선택", list(JOBS.keys()))
    job_info = JOBS[job_choice]
    
    st.info(f"**{job_choice}**: {job_info['desc']}\n\n"
            f"🗡️ **시작 무기:** {job_info['weapon']} | 🛡️ **시작 방어구:** {job_info['armor']} | ❤️ **기본 체력:** {job_info['base_hp']}\n\n"
            f"📊 **기본 스탯:** 근력 {job_info['base_stats']['str']} | 민첩 {job_info['base_stats']['dex']} | 지능 {job_info['base_stats']['int']} | 매력 {job_info['base_stats']['cha']}")

    st.divider()
    st.write("📊 **보너스 능력치 포인트 분배 (총 5 pt)**")

    c1, c2 = st.columns(2)
    with c1:
        add_str = st.number_input("⚔️ 근력 (STR)", min_value=0, max_value=5, value=1)
        add_dex = st.number_input("🎯 민첩 (DEX)", min_value=0, max_value=5, value=1)
    with c2:
        add_int = st.number_input("🧠 지능 (INT)", min_value=0, max_value=5, value=1)
        add_cha = st.number_input("✨ 매력 (CHA)", min_value=0, max_value=5, value=2)

    used_points = add_str + add_dex + add_int + add_cha
    remaining_points = 5 - used_points

    if remaining_points < 0:
        st.error(f"⚠️ 사용 가능한 보너스 포인트를 초과했습니다! ({abs(remaining_points)}pt 초과)")
    else:
        st.success(f"남은 포인트: **{remaining_points} pt**")
        
        if st.button("🚀 이 설정으로 모험 시작하기", use_container_width=True):
            st.session_state.job = job_choice
            st.session_state.weapon = job_info["weapon"]
            st.session_state.armor = job_info["armor"]
            st.session_state.hp = job_info["base_hp"]
            st.session_state.max_hp = job_info["base_hp"]
            st.session_state.gold = 20  # 시작 골드 조율
            
            # 하향된 스탯 + 보너스 포인트 저장
            st.session_state.str = job_info["base_stats"]["str"] + add_str
            st.session_state.dex = job_info["base_stats"]["dex"] + add_dex
            st.session_state.int = job_info["base_stats"]["int"] + add_int
            st.session_state.cha = job_info["base_stats"]["cha"] + add_cha
            
            st.session_state.game_started = True
            next_event()
            st.rerun()

# ---------------------------------------------------------
# 6. [메인 화면 B] 이벤트 / 결과 / 게임 오버
# ---------------------------------------------------------
else:
    st.title("📜 모험가 이야기 (Life in Adventure)")

    # [1] 게임 오버
    if st.session_state.hp <= 0:
        st.error("💀 체력이 다해 쓰러졌습니다... 당신의 모험은 여기서 끝났습니다.")
        if st.button("🔄 새로운 캐릭터로 다시 시작하기", use_container_width=True):
            reset_game()
            st.rerun()

    # [2] 이벤트 진행 중
    elif st.session_state.stage == "이벤트":
        ev = st.session_state.current_event
        st.subheader(ev["title"])
        st.info(ev["desc"])
        
        st.write("---")
        st.write("👉 **행동을 선택하세요:**")
        
        for idx, choice in enumerate(ev["choices"]):
            stat_key = choice["stat"]
            p_stat = getattr(st.session_state, stat_key)
            stat_name = {"str": "근력", "dex": "민첩", "int": "지능", "cha": "매력"}[stat_key]
            
            # 스탯 하향으로 인해 초반 성공률이 약 25% ~ 60% 수준으로 조율됨
            chance = calculate_success_rate(p_stat, choice["diff"])
            
            btn_text = f"{choice['text']}\n[{stat_name} {p_stat} | 난이도 {choice['diff']} | 성공률: {chance}%]"
            
            if st.button(btn_text, key=f"choice_btn_{idx}", use_container_width=True):
                dice = random.randint(1, 20)
                total = p_stat + dice
                
                if total >= choice["diff"]:
                    msg = f"🎲 주사위({dice}) + {stat_name}({p_stat}) = **{total}** (난이도 {choice['diff']}) ➡️ **[성공!]**\n\n"
                    msg += choice["succ"]
                    
                    st.session_state.gold += choice.get("succ_gold", 0)
                    st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + choice.get("succ_hp", 0))
                    
                    # 성공 시 20% 확률로 스탯 성장
                    if random.random() < 0.20:
                        setattr(st.session_state, stat_key, p_stat + 1)
                        msg += f"\n\n✨ **[능력치 상승!]** 시련을 이겨내고 **{stat_name}** 이(가) 1 상승했습니다!"
                else:
                    msg = f"🎲 주사위({dice}) + {stat_name}({p_stat}) = **{total}** (난이도 {choice['diff']}) ➡️ **[실패...]**\n\n"
                    msg += choice["fail"]
                    
                    st.session_state.hp -= choice.get("fail_hp", 0)
                    st.session_state.gold = max(0, st.session_state.gold - choice.get("fail_gold", 0))
                    
                st.session_state.log = msg
                st.session_state.stage = "결과"
                st.rerun()

    # [3] 선택 결과 화면
    elif st.session_state.stage == "결과":
        st.subheader("📜 판정 결과")
        if "[성공!]" in st.session_state.log:
            st.success(st.session_state.log)
        else:
            st.warning(st.session_state.log)
            
        if st.button("▶️ 다음 모험 카드로 이동", use_container_width=True):
            next_event()
            st.rerun()
