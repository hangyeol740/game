import random
import time
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 설정 및 초기 상태 세팅
# ---------------------------------------------------------
st.set_page_config(
    page_title="모험가의 여정 - 타이핑 확장판", page_icon="🗺️", layout="centered"
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
if "current_event" not in st.session_state:
    st.session_state.current_event = None
if "text_animated" not in st.session_state:
    st.session_state.text_animated = False

# 게임 초기화 함수
def reset_game():
    st.session_state.hp = 100
    st.session_state.gold = 50
    st.session_state.inventory = []
    st.session_state.weapon = "녹슨 단검"
    st.session_state.current_event = None
    st.session_state.text_animated = False

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

if st.sidebar.button("🔄 게임 초기화"):
    reset_game()
    st.rerun()

# ---------------------------------------------------------
# 3. 엔딩 및 사망 조건 체크
# ---------------------------------------------------------
if st.session_state.hp <= 0:
    st.error(
        "💀 **[BAD ENDING] 거듭된 상처와 피로를 이기지 못하고 길에서 쓰러졌습니다... 다시 도전하세요.**"
    )
    if st.button("처음부터 다시 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

if st.session_state.gold >= 150:
    st.success(
        "👑 **[HAPPY ENDING] 막대한 부를 쌓아 영지의 전설적인 영웅으로 추대되었습니다!**"
    )
    if st.button("새로운 모험 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

# ---------------------------------------------------------
# 4. 탐험 및 이벤트 모드 (타이핑 효과 적용)
# ---------------------------------------------------------
st.title("📜 모험가 이야기: 심화 탐험")

# 확장된 이벤트 목록 (상점 이벤트 포함)
EVENTS = [
    {
        "type": "combat",
        "title": "숲속의 고블린 매복병",
        "desc": "울창하고 어두운 숲길을 조심스럽게 헤쳐 나가던 중, 머리 위 나뭇가지 사이와 빽빽한 수풀 속에서 번뜩이는 눈빛들이 포착되었습니다. 잠시 후, 누더기 옷을 걸치고 몽둥이를 든 굶주린 고블린 무리가 괴성을 지르며 길을 가로막았습니다!",
        "choices": [
            {
                "text": "⚔️ 무기를 뽑아 들고 정면으로 맞서 싸운다",
                "succ": "치열한 난투 끝에 고블린들을 물리치고 도망간 녀석들의 주머니를 털어 금화를 챙겼습니다! (+35 Gold)",
                "fail": "고블린들의 기습에 허를 찔려 여러 차례 몽둥이 세례를 맞고 부상을 입었습니다. (-25 체력)",
                "succ_gold": 35,
                "fail_hp": 25,
            },
            {
                "text": "🎯 옆쪽의 가시 덩굴이 우거진 좁은 샛길로 날렵하게 도망친다",
                "succ": "녀석들이 헛방을 치는 사이 무사히 숲을 빠져나가며 바닥에 떨어진 반짝이는 보물 주머니를 발견했습니다! (+20 Gold)",
                "fail": "급하게 도망치다 가시 덩굴에 온몸이 긁히고 옷이 찢어졌습니다. (-15 체력)",
                "succ_gold": 20,
                "fail_hp": 15,
            },
        ],
    },
    {
        "type": "merchant",
        "title": "방랑 상인의 은밀한 오두막",
        "desc": "안개 자욱한 갈림길 한켠에서 희미한 등불 불빛이 새어나오는 낡은 오두막을 발견했습니다. 문을 조심스럽게 열고 들어가자, 굽은 등허리의 늙은 방랑 상인이 환한 미소를 지으며 당신을 맞이합니다. \"어서 오게나 젊은이, 위험한 여정에 쓸만한 물건들이 좀 있다네.\"",
    },
    {
        "type": "event",
        "title": "신비로운 달빛의 마법 샘",
        "desc": "고요한 숲속 깊은 곳, 은은한 푸른빛을 발산하는 신비로운 샘가에 도달했습니다. 샘물 주변에는 기묘한 고대 문자가 새겨진 돌무더기가 둘러싸고 있으며, 물가에서 은은한 온기와 함께 알 수 없는 치유의 기운이 피어오르고 있습니다.",
        "choices": [
            {
                "text": "💧 샘물을 손으로 떠서 시원하게 마신다",
                "succ": "청량한 물이 목을 타고 넘어가자 온몸의 피로가 씻겨 내려가듯 기운이 샘솟습니다! (+30 체력 회복)",
                "fail": "알 수 없는 정체의 마법 물이었던 것인지 마신 직후 심한 복통이 일어났습니다. (-15 체력)",
                "succ_hp": 30,
                "fail_hp": 15,
            },
            {
                "text": "🪙 주머니 속 동전을 꺼내 샘물에 던지며 소원을 빈다",
                "succ": "샘물 속에서 잔잔한 파문이 일더니 알 수 없는 행운이 깃들어 주머니가 묵직해졌습니다! (+40 Gold)",
                "fail": "동전이 가라앉은 뒤 아무런 반응도 일어나지 않았습니다. 왠지 아까운 돈을 날린 기분입니다.",
                "succ_gold": 40,
            },
        ],
    },
]

# 현재 이벤트가 없다면 무작위로 하나 선택
if st.session_state.current_event is None:
    st.session_state.current_event = random.choice(EVENTS)
    st.session_state.text_animated = False

event = st.session_state.current_event

st.subheader(f"📍 {event['title']}")
desc_placeholder = st.empty()

# ---------------------------------------------------------
# 타이핑 애니메이션 및 스킵 버튼 처리 로직
# ---------------------------------------------------------
if not st.session_state.text_animated:
    # 클릭하면 애니메이션을 즉시 건너뛰고 전체 텍스트를 출력하는 버튼
    if st.button("⚡ 텍스트 한 번에 보기 (스킵)"):
        st.session_state.text_animated = True
        st.rerun()

    # 타이핑 효과 시뮬레이션
    full_text = event["desc"]
    current_text = ""
    for char in full_text:
        current_text += char
        desc_placeholder.write(current_text)
        time.sleep(0.015)  # 타이핑 속도 조절

    st.session_state.text_animated = True
    st.rerun()
else:
    # 이미 타이핑이 끝났거나 스킵된 경우 전체 텍스트 고정 출력
    desc_placeholder.write(event["desc"])

st.markdown("---")

# ---------------------------------------------------------
# 이벤트 종류에 따른 분기 처리 (전투/일반 이벤트 vs 상점 이벤트)
# ---------------------------------------------------------
if event["type"] == "merchant":
    st.info("🛒 방랑 상인의 상점이 열렸습니다!")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧪 체력 포션")
        st.write("가격: **20 G**")
        st.write("마시면 체력을 30 회복합니다.")
        if st.button("포션 구매하기"):
            if st.session_state.gold >= 20:
                st.session_state.gold -= 20
                st.session_state.inventory.append("체력 포션")
                st.success("체력 포션을 구매했습니다!")
            else:
                st.error("골드가 부족합니다!")

    with col2:
        st.markdown("### ⚔️ 강철 검")
        st.write("가격: **80 G**")
        st.write("더 강력한 전투력을 발휘하는 무기입니다.")
        if st.button("강철 검 구매하기"):
            if st.session_state.gold >= 80:
                if st.session_state.weapon != "강철 검":
                    st.session_state.gold -= 80
                    st.session_state.weapon = "강철 검"
                    st.success("강철 검을 장착했습니다!")
                else:
                    st.warning("이미 장착하고 있는 무기입니다.")
            else:
                st.error("골드가 부족합니다!")

    st.markdown("---")
    if st.button("🚪 상점을 나와 다시 험난한 길을 떠난다"):
        st.session_state.current_event = None
        st.session_state.text_animated = False
        st.rerun()

else:
    # 일반 전투/선택지 이벤트 처리
    for i, choice in enumerate(event["choices"]):
        if st.button(choice["text"], key=f"choice_{i}"):
            # 강철 검 장착 시 성공 확률 보정 (기본 50% -> 70% 확률로 성공)
            bonus = 20 if st.session_state.weapon == "강철 검" else 0
            success_roll = random.randint(1, 100) - bonus

            if success_roll <= 50:
                st.success(choice["succ"])
                if "succ_gold" in choice:
                    st.session_state.gold += choice["succ_gold"]
                if "succ_hp" in choice:
                    st.session_state.hp = min(
                        st.session_state.max_hp,
                        st.session_state.hp + choice["succ_hp"],
                    )
            else:
                st.error(choice["fail"])
                if "fail_hp" in choice:
                    st.session_state.hp -= choice["fail_hp"]
                if "fail_gold" in choice:
                    st.session_state.gold = max(
                        0, st.session_state.gold - choice["fail_gold"]
                    )

            # 다음 무작위 이벤트로 넘어가기 위한 초기화
            st.session_state.current_event = None
            st.session_state.text_animated = False
            st.rerun()
