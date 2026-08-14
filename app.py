import random
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 설정 및 초기 게임 상태 세팅
# ---------------------------------------------------------
st.set_page_config(
    page_title="모험가의 여정 - 확장판", page_icon="🗺️", layout="centered"
)

if "hp" not in st.session_state:
    st.session_state.hp = 100
if "max_hp" not in st.session_state:
    st.session_state.max_hp = 100
if "gold" not in st.session_state:
    st.session_state.gold = 50
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "weapon" not in st.session_state:
    st.session_state.weapon = "녹슨 단검"
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "explore"  # 'explore' 또는 'shop'
if "current_event" not in st.session_state:
    st.session_state.current_event = None

# 게임 초기화 함수
def reset_game():
    st.session_state.hp = 100
    st.session_state.gold = 50
    st.session_state.inventory = []
    st.session_state.weapon = "녹슨 단검"
    st.session_state.game_mode = "explore"
    st.session_state.current_event = None

# ---------------------------------------------------------
# 2. 사이드바: 상태창 및 포션 사용
# ---------------------------------------------------------
st.sidebar.title("🎒 모험가 상태창")
st.sidebar.markdown(f"❤️ **체력:** {st.session_state.hp} / {st.session_state.max_hp}")
st.sidebar.markdown(f"💰 **골드:** {st.session_state.gold} G")
st.sidebar.markdown(f"⚔️ **무기:** {st.session_state.weapon}")
st.sidebar.markdown(f"🎒 **인벤토리:** {st.session_state.inventory}")

st.sidebar.markdown("---")

# 포션 사용 기능
if "체력 포션" in st.session_state.inventory:
    if st.sidebar.button("🧪 포션 사용 (+30 HP)"):
        st.session_state.inventory.remove("체력 포션")
        st.session_state.hp = min(
            st.session_state.max_hp, st.session_state.hp + 30
        )
        st.sidebar.success("포션을 마셔 체력을 회복했습니다!")
        st.rerun()

# 화면 모드 전환 버튼
if st.sidebar.button("🛒 방랑 상점 방문 / 나가기"):
    if st.session_state.game_mode == "explore":
        st.session_state.game_mode = "shop"
    else:
        st.session_state.game_mode = "explore"
    st.rerun()

if st.sidebar.button("🔄 게임 초기화"):
    reset_game()
    st.rerun()

# ---------------------------------------------------------
# 3. 엔딩 및 사망 조건 체크
# ---------------------------------------------------------
if st.session_state.hp <= 0:
    st.error(
        "💀 **[BAD ENDING] 체력이 바닥나 길에서 쓰러졌습니다... 다시 도전하세요.**"
    )
    if st.button("처음부터 다시 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

if st.session_state.gold >= 150:
    st.success(
        "👑 **[HAPPY ENDING] 막대한 부를 쌓아 영지의 전설적인 영웅이 되었습니다!**"
    )
    if st.button("새로운 모험 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

# ---------------------------------------------------------
# 4. 상점 화면 모드
# ---------------------------------------------------------
if st.session_state.game_mode == "shop":
    st.title("🛒 방랑 상인의 오두막")
    st.write(
        "\"어서 오게나! 모험에 필요한 물건들을 저렴하게 팔고 있다네.\""
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧪 체력 포션")
        st.write("가격: **20 G**")
        st.write("설명: 마시면 체력을 30 회복합니다.")
        if st.button("포션 구매"):
            if st.session_state.gold >= 20:
                st.session_state.gold -= 20
                st.session_state.inventory.append("체력 포션")
                st.success("체력 포션을 구매했습니다!")
            else:
                st.error("골드가 부족합니다!")

    with col2:
        st.subheader("⚔️ 강철 검")
        st.write("가격: **80 G**")
        st.write("설명: 더 강력한 공격을 가능하게 해주는 검입니다.")
        if st.button("강철 검 구매"):
            if st.session_state.gold >= 80:
                if st.session_state.weapon != "강철 검":
                    st.session_state.gold -= 80
                    st.session_state.weapon = "강철 검"
                    st.success("강철 검을 장착했습니다!")
                else:
                    st.warning("이미 장착하고 있습니다.")
            else:
                st.error("골드가 부족합니다!")

    st.markdown("---")
    if st.button("🌲 탐험 지역으로 돌아가기"):
        st.session_state.game_mode = "explore"
        st.rerun()

# ---------------------------------------------------------
# 5. 탐험 및 이벤트 모드
# ---------------------------------------------------------
else:
    st.title("📜 모험가 이야기: 확장판")

    # 이벤트 목록 정의
    EVENTS = [
        {
            "title": "숲속의 고블린 매복",
            "desc": "울창한 숲길을 지나던 중, 수풀 속에서 고블린 무리가 튀어나왔습니다!",
            "choices": [
                {
                    "text": "⚔️ 정면으로 맞서 싸운다",
                    "succ": "고블린들을 무찌르고 주머니를 뒤져 금화를 얻었습니다! (+30 Gold)",
                    "fail": "공격을 허용해 부상을 입었습니다. (-20 체력)",
                    "succ_gold": 30,
                    "fail_hp": 20,
                },
                {
                    "text": "🎯 좁은 샛길로 날렵하게 도망친다",
                    "succ": "무사히 추격을 따돌리고 숨겨진 보물상자를 발견했습니다! (+20 Gold)",
                    "fail": "달리다 가시에 걸려 다쳤습니다. (-10 체력)",
                    "succ_gold": 20,
                    "fail_hp": 10,
                },
            ],
        },
        {
            "title": "버려진 상단의 마차",
            "desc": "길가에 뒤집힌 마차 밑에서 다리가 낀 상인이 살려달라고 신음하고 있습니다.",
            "choices": [
                {
                    "text": "⚔️ 힘으로 마차 잔해를 들어 올려 구출한다",
                    "succ": "상인을 구해주자 고마움에 보답을 건네줍니다. (+40 Gold)",
                    "fail": "잔해에 허리를 다쳤습니다. (-15 체력)",
                    "succ_gold": 40,
                    "fail_hp": 15,
                },
                {
                    "text": "✨ 지렛대를 만들어 안전하게 구출한다",
                    "succ": "지혜롭게 구조해 내어 상인이 포션을 선물했습니다!",
                    "fail": "시간을 너무 지체해 아무것도 얻지 못했습니다.",
                    "succ_item": "체력 포션",
                },
            ],
        },
        {
            "title": "신비로운 호수의 샘",
            "desc": "달빛이 비치는 신비로운 샘가에 도착했습니다. 물을 마시거나 조용히 명상할 수 있습니다.",
            "choices": [
                {
                    "text": "💧 샘물을 시원하게 마신다",
                    "succ": "기운이 샘솟으며 상쾌해집니다! (+25 체력 회복)",
                    "fail": "알 수 없는 물이라 배탈이 났습니다. (-10 체력)",
                    "succ_hp": 25,
                    "fail_hp": 10,
                },
                {
                    "text": "🪙 샘물에 동전을 던지고 소원을 빈다",
                    "succ": "행운이 깃들어 주머니가 두둑해졌습니다! (+35 Gold)",
                    "fail": "아무 일도 일어나지 않았습니다.",
                    "succ_gold": 35,
                },
            ],
        },
    ]

    # 현재 이벤트가 없다면 무작위로 하나 선택
    if st.session_state.current_event is None:
        st.session_state.current_event = random.choice(EVENTS)

    event = st.session_state.current_event

    st.subheader(f"📍 {event['title']}")
    st.write(event["desc"])
    st.markdown("---")

    # 선택지 버튼 출력
    for i, choice in enumerate(event["choices"]):
        if st.button(choice["text"], key=f"choice_{i}"):
            # 무기 보정치 계산 (강철 검 장착 시 성공 확률 높임 또는 데미지 감소 등)
            bonus = 10 if st.session_state.weapon == "강철 검" else 0
            success_roll = random.randint(1, 100) - bonus

            # 50% 확률로 성공/실패 판정
            if success_roll <= 50:
                st.success(choice["succ"])
                if "succ_gold" in choice:
                    st.session_state.gold += choice["succ_gold"]
                if "succ_hp" in choice:
                    st.session_state.hp = min(
                        st.session_state.max_hp,
                        st.session_state.hp + choice["succ_hp"],
                    )
                if "succ_item" in choice:
                    st.session_state.inventory.append(choice["succ_item"])
            else:
                st.error(choice["fail"])
                if "fail_hp" in choice:
                    st.session_state.hp -= choice["fail_hp"]
                if "fail_gold" in choice:
                    st.session_state.gold = max(
                        0, st.session_state.gold - choice["fail_gold"]
                    )

            # 다음 이벤트로 갱신하기 위해 현재 이벤트 초기화
            st.session_state.current_event = None
            st.rerun()
