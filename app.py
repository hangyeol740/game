import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="모험가 이야기 (Life in Adventure)",
    page_icon="📜",
    layout="centered"
)

# ---------------------------------------------------------
# 💡 [성공 확률 계산 함수]
# ---------------------------------------------------------
def calculate_success_rate(stat_value, difficulty):
    required_dice = difficulty - stat_value
    if required_dice <= 1:
        return 100
    elif required_dice > 20:
        return 0
    else:
        winning_rolls = 20 - required_dice + 1
        return int((winning_rolls / 20) * 100)

# ---------------------------------------------------------
# 1. 직업 데이터베이스
# ---------------------------------------------------------
JOBS = {
    "전사": {
        "desc": "강인한 신체로 정면 승부를 즐기는 모험가",
        "weapon": "녹슨 숏소드",
        "armor": "가죽 누비 갑옷",
        "base_hp": 100,
        "base_stats": {"str": 7, "dex": 5, "int": 4, "cha": 4}
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
# 2. 이미지 URL이 포함된 이벤트 카드 목록
# ---------------------------------------------------------
EVENTS = [
    {
        "id": "goblin_ambush",
        "title": "📜 숲속의 고블린 매복",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=800",
        "desc": "울창한 숲길을 지나던 중, 나무 위와 수풀 속에서 굶주린 고블린 3마리가 몽둥이를 들고 튀어나왔습니다!",
        "choices": [
            {
                "text": "⚔️ 무기를 뽑아 들고 정면으로 맞서 싸운다",
                "stat": "str", "diff": 14,
                "succ": "무게를 실은 공격으로 고블린들을 제압했습니다! (+20 Gold)",
                "fail": "고블린들의 수에 눌려 여러 차례 몽둥이에 맞았습니다. (-25 체력)",
                "succ_gold": 20, "fail_hp": 25
            },
            {
                "text": "🎯 수풀 사이 좁은 길로 날렵하게 몸을 날려 탈출한다",
                "stat": "dex", "diff": 13,
                "succ": "고블린들이 헛방을 치는 사이 가시 덩굴을 빠져나와 도망쳤습니다.",
                "fail": "가시 덩굴에 걸려 넘어져 다쳤습니다. (-15 체력, -10 Gold)",
                "fail_hp": 15, "fail_gold": 10
            }
        ]
    },
    {
        "id": "injured_merchant",
        "title": "📜 습격당한 상단 마차",
        "image": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?q=80&w=800",
        "desc": "길가에 뒤집힌 마차 아래에 다리가 낀 상인이 피를 흘리며 신음하고 있습니다. 곧 몬스터가 몰려올 것입니다.",
        "choices": [
            {
                "text": "⚔️ 잔해를 힘으로 들어 올려 상인을 구출한다",
                "stat": "str", "diff": 15,
                "succ": "무거운 잔해를 들어 올려 상인을 구했습니다! 상인이 두툼한 주머니를 건넵니다. (+35 Gold)",
                "fail": "잔해를 들려다가 허리를 삐끗하여 부상을 입었습니다. (-15 체력)",
                "fail_hp": 15
            },
            {
                "text": "✨ 따뜻한 말과 지혜로 상인을 안심시키며 레버 원리로 구출한다",
                "stat": "cha", "diff": 12,
                "succ": "차분하게 지렛대를 만들어 무사히 구출했습니다. 상인이 회복 포션을 줍니다. (+25 체력 회복)",
                "fail": "당신의 당황한 모습에 상인은 더욱 패닉에 빠져 구조에 실패했습니다.",
                "succ_hp": 25
            }
        ]
    },
    {
        "id": "ancient_ruins",
        "title": "📜 이끼 낀 고대 유적 문",
        "image": "https://images.unsplash.com/photo-1544967082-d9d25d867d66?q=80&w=800",
        "desc": "산자락 깊은 곳에서 기괴한 룬 문자가 새겨진 고대 유적 입구를 발견했습니다.",
        "choices": [
            {
                "text": "🧠 룬 문자의 법칙을 분석하여 비밀 문을 연다",
                "stat": "int", "diff": 16,
                "succ": "고대 마법 공식을 풀어내어 문을 열었습니다! 상자에서 금화를 획득합니다. (+50 Gold)",
                "fail": "잘못된 문자를 건드려 환영 마법 폭발이 일어났습니다! (-20 체력)",
                "succ_gold": 50, "fail_hp": 20
            },
            {
                "text": "🎯 틈새 사이로 도구를 넣어 잠금장치를 해제한다",
                "stat": "dex", "diff": 15,
                "succ": "철사를 정밀하게 조작하여 내부 걸쇠를 빼냈습니다! (+30 Gold)",
                "fail": "도구가 부러지며 함정이 발동해 독침이 꽂혔습니다! (-25 체력)",
                "succ_gold": 30, "fail_hp": 25
            }
        ]
    },
    {
        "id": "witch_hut",
        "title": "📜 늪지대의 숲속 마녀",
        "image": "https://images.unsplash.com/photo-1511447333015-45b65e60f6d5?q=80&w=800",
        "desc": "수상한 연기가 피어오르는 오두막에서 기묘한 차림의 마녀가 솥에 묘약을 끓이고 있습니다.",
        "choices": [
            {
                "text": "🧠 묘약의 성분을 파악하여 위험한 재료인지 확인한다",
                "stat": "int", "diff": 14,
                "succ": "마녀의 실수를 지적해 주고 보상으로 신비한 묘약을 나누어 마셨습니다! (+30 체력 회복)",
                "fail": "마녀의 비기 재료를 건드렸다가 분노한 마녀의 저주에 당했습니다. (-20 체력)",
                "succ_hp": 30, "fail_hp": 20
            },
            {
                "text": "✨ 친근하게 접근해 마녀와 대화를 시도한다",
                "stat": "cha", "diff": 13,
                "succ": "마녀는 마음을 열고 당신의 무기에 유용한 주문을 걸어주었습니다. (+15 Gold)",
                "fail": "마녀는 타인을 믿지 않는다며 당신을 오두막 밖으로 내쫓았습니다.",
                "succ_gold": 15
            }
        ]
    },
    {
        "id": "sword_in_stone",
        "title": "📜 바위에 꽂힌 의식용 검",
        "image": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?q=80&w=800",
        "desc": "오래된 제단 중앙, 커다란 바위에 정교한 장식의 검이 깊숙이 박혀 있습니다.",
        "choices": [
            {
                "text": "⚔️ 온 힘을 다해 바위에서 검을 뽑아낸다",
                "stat": "str", "diff": 16,
                "succ": "바위에 금이 가며 검이 뽑혀 나왔습니다! 검을 팔아 큰 돈을 받았습니다. (+45 Gold)",
                "fail": "손이 미끄러지며 바위에 강하게 부딪혔습니다. (-15 체력)",
                "fail_hp": 15
            },
            {
                "text": "🧠 제단 주변의 마법 진을 분석해 검을 해제한다",
                "stat": "int", "diff": 15,
                "succ": "마법적 고리를 풀자 검이 스르륵 빠져나왔습니다. (+35 Gold)",
                "fail": "마법 결계가 역류하며 손에 심한 화상을 입었습니다. (-20 체력)",
                "succ_gold": 35, "fail_hp": 20
            }
        ]
    },
    {
        "id": "ogre_bridge",
        "title": "📜 외나무다리를 막아선 오우거",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=800",
        "desc": "계곡의 외나무다리를 거대한 오우거가 막아서며 턱없는 통행료를 요구합니다.",
        "choices": [
            {
                "text": "⚔️ 거대한 오우거와 목숨을 건 사투를 벌인다",
                "stat": "str", "diff": 17,
                "succ": "오우거의 육중한 공격을 피하고 약점을 타격해 제압했습니다! (+40 Gold)",
                "fail": "오우거의 주먹에 맞고 계곡 아래로 굴러떨어졌습니다. (-35 체력)",
                "succ_gold": 40, "fail_hp": 35
            },
            {
                "text": "✨ 화술로 오우거를 속여 무료로 지나간다",
                "stat": "cha", "diff": 14,
                "succ": "'뒤에서 왕국 기사단이 몰려오고 있다'고 속여 오우거를 도망치게 했습니다.",
                "fail": "오우거는 속지 않고 화를 내며 당신을 발로 차버렸습니다! (-20 체력)",
                "fail_hp": 20
            }
        ]
    },
    {
        "id": "shady_gambler",
        "title": "📜 어두운 골목의 도박사",
        "image": "https://images.unsplash.com/photo-1511193311914-0346f16efe90?q=80&w=800",
        "desc": "한 남자가 주사위 세 개를 보여주며 '솔솔한 내깃돈'을 걸고 한판 하자고 제안합니다.",
        "choices": [
            {
                "text": "🎯 눈을 번뜩이며 도박사의 손장난을 파악한다",
                "stat": "dex", "diff": 14,
                "succ": "도박사의 속임수를 간파하고 역으로 허점을찔러 돈을 따냈습니다! (+30 Gold)",
                "fail": "손놀림에 속아 돈을 전부 잃고 말았습니다. (-20 Gold)",
                "succ_gold": 30, "fail_gold": 20
            },
            {
                "text": "✨ 현란한 언변으로 승부수를 던진다",
                "stat": "cha", "diff": 13,
                "succ": "상대의 심리를 교란하여 승리를 거머쥐었습니다! (+25 Gold)",
                "fail": "상대의 심리전에 말려들어 주머니를 털렸습니다. (-15 Gold)",
                "succ_gold": 25, "fail_gold": 15
            }
        ]
    },
    {
        "id": "abandoned_camp",
        "title": "📜 버려진 모험가의 캠프",
        "image": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?q=80&w=800",
        "desc": "불씨가 꺼진 지 얼마 되지 않은 모험가의 텐트를 발견했습니다. 무언가 쓸만한 물건이 남아있을지 모릅니다.",
        "choices": [
            {
                "text": "🎯 텐트 주변 함정을 경계하며 신중하게 수색한다",
                "stat": "dex", "diff": 13,
                "succ": "설치되어 있던 부비트랩을 비켜가며 비상 식량과 동전을 발견했습니다! (+20 체력 회복, +15 Gold)",
                "fail": "줄에 발이 걸려 경보용 종이 울리고 함정이 발동했습니다! (-15 체력)",
                "succ_hp": 20, "succ_gold": 15, "fail_hp": 15
            },
            {
                "text": "🧠 남겨진 일기장을 읽고 모험가의 행방을 추적한다",
                "stat": "int", "diff": 14,
                "succ": "일기장에서 지도를 확보하여 숨겨진 비상금을 찾아냈습니다! (+35 Gold)",
                "fail": "일기장을 읽는 데 몰두하다 야생 동물의 습격을 받았습니다! (-20 체력)",
                "succ_gold": 35, "fail_hp": 20
            }
        ]
    }
]

# ---------------------------------------------------------
# 3. 게임 상태 초기화 및 중복 방지 시스템
# ---------------------------------------------------------
def reset_game():
    st.session_state.game_started = False
    st.session_state.stage = "생성"
    st.session_state.current_event = None
    st.session_state.event_deck = []
    st.session_state.log = ""

if "game_started" not in st.session_state or "event_deck" not in st.session_state:
    reset_game()

def draw_next_event():
    if not st.session_state.get("event_deck"):
        indices = list(range(len(EVENTS)))
        random.shuffle(indices)
        st.session_state.event_deck = indices
        
    next_idx = st.session_state.event_deck.pop()
    st.session_state.current_event = EVENTS[next_idx]
    st.session_state.stage = "이벤트"

# ---------------------------------------------------------
# 4. [사이드바] 모험가 프로필
# ---------------------------------------------------------
with st.sidebar:
    st.header("📜 모험가 프로필")
    
    if st.session_state.get("game_started", False):
        st.write(f"**직업:** {st.session_state.job}")
        st.write(f"❤️ **체력:** {st.session_state.hp} / {st.session_state.max_hp}")
        st.write(f"💰 **골드:** {st.session_state.gold} G")
        
        st.divider()
        st.subheader("🎒 인벤토리")
        st.write(f"🗡️ **무기:** {st.session_state.weapon}")
        st.write(f"🛡️ **방어구:** {st.session_state.armor}")
        
        st.divider()
        st.subheader("📊 능력치 (Stats)")
        st.write(f"⚔️ **근력 (STR):** {st.session_state.str}")
        st.write(f"🎯 **민첩 (DEX):** {st.session_state.dex}")
        st.write(f"🧠 **지능 (INT):** {st.session_state.int}")
        st.write(f"✨ **매력 (CHA):** {st.session_state.cha}")
        
        st.divider()
        deck_list = st.session_state.get("event_deck", [])
        st.caption(f"🃏 덱에 남은 미확인 이벤트: **{len(deck_list)}개**")
        
        if st.button("🔄 처음부터 다시 시작", use_container_width=True):
            reset_game()
            st.rerun()
    else:
        st.info("💡 캐릭터를 생성하면 상태창이 활성화됩니다.")

# ---------------------------------------------------------
# 5. [메인 화면] 캐릭터 생성
# ---------------------------------------------------------
if not st.session_state.game_started:
    st.title("📜 캐릭터 생성 (Character Creation)")

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
        st.error(f"⚠️ 보너스 포인트를 초과했습니다! ({abs(remaining_points)}pt 초과)")
    else:
        st.success(f"남은 포인트: **{remaining_points} pt**")
        
        if st.button("🚀 이 설정으로 모험 시작하기", use_container_width=True):
            st.session_state.job = job_choice
            st.session_state.weapon = job_info["weapon"]
            st.session_state.armor = job_info["armor"]
            st.session_state.hp = job_info["base_hp"]
            st.session_state.max_hp = job_info["base_hp"]
            st.session_state.gold = 20
            
            st.session_state.str = job_info["base_stats"]["str"] + add_str
            st.session_state.dex = job_info["base_stats"]["dex"] + add_dex
            st.session_state.int = job_info["base_stats"]["int"] + add_int
            st.session_state.cha = job_info["base_stats"]["cha"] + add_cha
            
            st.session_state.game_started = True
            draw_next_event()
            st.rerun()

# ---------------------------------------------------------
# 6. [메인 화면] 메인 이벤트 진행
# ---------------------------------------------------------
else:
    st.title("📜 모험가 이야기 (Life in Adventure)")

    # [1] 게임 오버
    if st.session_state.hp <= 0:
        st.error("💀 체력이 다해 쓰러졌습니다... 당신의 모험은 여기서 끝났습니다.")
        if st.button("🔄 새로운 캐릭터로 다시 시작하기", use_container_width=True):
            reset_game()
            st.rerun()

    # [2] 이벤트 진행 화면
    elif st.session_state.stage == "이벤트":
        ev = st.session_state.current_event
        st.subheader(ev["title"])
        
        if "image" in ev:
            st.image(ev["image"], use_container_width=True)
            
        st.info(ev["desc"])
        
        st.write("---")
        st.write("👉 **행동을 선택하세요:**")
        
        for idx, choice in enumerate(ev["choices"]):
            stat_key = choice["stat"]
            p_stat = getattr(st.session_state, stat_key)
            stat_name = {"str": "근력", "dex": "민첩", "int": "지능", "cha": "매력"}[stat_key]
            
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
            draw_next_event()
            st.rerun()
