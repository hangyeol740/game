import random
import time
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 설정 및 초기 세팅
# ---------------------------------------------------------
st.set_page_config(
    page_title="모험가의 여정", page_icon="🗺️", layout="centered"
)

if "game_state" not in st.session_state:
    st.session_state.game_state = "create"

if "hp" not in st.session_state:
    st.session_state.hp = 100
if "max_hp" not in st.session_state:
    st.session_state.max_hp = 100
if "gold" not in st.session_state:
    st.session_state.gold = 50
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "job" not in st.session_state:
    st.session_state.job = ""
if "weapon" not in st.session_state:
    st.session_state.weapon = "녹슨 단검"
if "current_event" not in st.session_state:
    st.session_state.current_event = None
if "text_animated" not in st.session_state:
    st.session_state.text_animated = False

def reset_game():
    st.session_state.game_state = "create"
    st.session_state.hp = 100
    st.session_state.max_hp = 100
    st.session_state.gold = 50
    st.session_state.inventory = []
    st.session_state.job = ""
    st.session_state.weapon = "녹슨 단검"
    st.session_state.current_event = None
    st.session_state.text_animated = False

# ---------------------------------------------------------
# 2. 캐릭터 생성 화면
# ---------------------------------------------------------
if st.session_state.game_state == "create":
    st.title("🛡️ 모험가 생성소")
    st.write("위험천만한 모험을 떠나기 전, 당신의 직업과 초기 스탯을 선택하세요!")

    job_choice = st.selectbox(
        "직업을 선택하세요", 
        ["전사 (체력 중심)", "도적 (골드/보상 중심)", "마법사 (균형형)"]
    )

    st.markdown("---")
    st.subheader("📊 초기 스탯 분배 (총 포인트: 10)")
    
    stat_str = st.slider("💪 근력 (전투 성공률 및 무기 위력 영향)", 1, 8, 4)
    stat_agi = st.slider("🏃 민첩 (도주 및 회피 확률 영향)", 1, 8, 3)
    stat_luk = st.slider("✨ 행운 (골드 획득량 및 아이템 발견 영향)", 1, 8, 3)

    if stat_str + stat_agi + stat_luk != 10:
        st.warning("⚠️ 스탯 포인터의 총합이 10이 되도록 맞춰주세요!")
    else:
        st.success("✨ 스탯 배분 완료! 모험을 시작할 준비가 되었습니다.")

    if st.button("🚀 모험 시작하기"):
        st.session_state.job = job_choice.split(" ")[0]
        
        if st.session_state.job == "전사":
            st.session_state.max_hp = 130
            st.session_state.hp = 130
            st.session_state.weapon = "강철 대검"
        elif st.session_state.job == "도적":
            st.session_state.max_hp = 90
            st.session_state.hp = 90
            st.session_state.gold = 70
            st.session_state.weapon = "날렵한 단검"
        else:
            st.session_state.max_hp = 100
            st.session_state.hp = 100
            st.session_state.weapon = "마력의 지팡이"

        st.session_state.stat_str = stat_str
        st.session_state.stat_agi = stat_agi
        st.session_state.stat_luk = stat_luk

        st.session_state.game_state = "explore"
        st.rerun()

    st.stop()

# ---------------------------------------------------------
# 3. 사이드바
# ---------------------------------------------------------
st.sidebar.title("🎒 모험가 상태창")
st.sidebar.markdown(f"🧙‍♂️ **직업:** {st.session_state.job}")
st.sidebar.markdown(f"❤️ **체력:** {st.session_state.hp} / {st.session_state.max_hp}")
st.sidebar.markdown(f"💰 **골드:** {st.session_state.gold} G")
st.sidebar.markdown(f"⚔️ **무기:** {st.session_state.weapon}")
st.sidebar.markdown(f"📊 **스탯:** 근력 {st.session_state.get('stat_str', 4)} / 민첩 {st.session_state.get('stat_agi', 3)} / 행운 {st.session_state.get('stat_luk', 3)}")
st.sidebar.markdown(f"🎒 **인벤토리:** {st.session_state.inventory}")

st.sidebar.markdown("---")

if "체력 포션" in st.session_state.inventory:
    if st.sidebar.button("🧪 포션 사용 (+30 HP)"):
        st.session_state.inventory.remove("체력 포션")
        st.session_state.hp = min(
            st.session_state.max_hp, st.session_state.hp + 30
        )
        st.sidebar.success("포션을 마셔 체력을 회복했습니다!")
        st.rerun()

if st.sidebar.button("🔄 캐릭터 다시 만들기"):
    reset_game()
    st.rerun()

# ---------------------------------------------------------
# 4. 엔딩 체크
# ---------------------------------------------------------
if st.session_state.hp <= 0:
    st.error("💀 **[BAD ENDING] 거듭된 상처와 피로를 이기지 못하고 쓰러졌습니다...**")
    if st.button("처음부터 다시 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

if st.session_state.gold >= 150:
    st.success("👑 **[HAPPY ENDING] 막대한 부를 쌓아 영지의 전설적인 영웅이 되었습니다!**")
    if st.button("새로운 모험 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

# ---------------------------------------------------------
# 5. 이벤트 데이터베이스
# ---------------------------------------------------------
EVENTS = [
    {
        "type": "merchant",
        "title": "방랑 상인의 은밀한 오두막",
        "desc": "안개 자욱한 갈림길 한켠에서 희미한 등불 불빛이 새어나오는 낡은 오두막을 발견했습니다. 문을 조심스럽게 열고 들어가자, 굽은 등허리의 늙은 방랑 상인이 환한 미소를 지으며 당신을 맞이합니다. \"어서 오게나 젊은이, 위험한 여정에 쓸만한 물건들이 좀 있다네.\""
    },
    {
        "type": "merchant",
        "title": "지하 암시장의 밀수꾼",
        "desc": "어두운 골목길 뒤편, 두꺼운 후드를 뒤집어쓴 인물이 은밀하게 손짓합니다. \"원하는 건 뭐든 있지... 돈만 충분하다면 말이야.\""
    },
    {
        "type": "merchant",
        "title": "떠돌이 대장장이의 대장간",
        "desc": "망치 소리가 울려 퍼지는 오솔길 옆에서 근육질의 대장장이가 화로에 불을 지피고 있습니다. \"강철 무기가 필요한가? 제값만 치른다면 최고의 단조품을 주지.\""
    },
    {
        "type": "combat",
        "title": "숲속의 고블린 매복병",
        "desc": "울창하고 어두운 숲길을 조심스럽게 헤쳐 나가던 중, 수풀 속에서 굶주린 고블린 무리가 괴성을 지르며 길을 가로막았습니다!",
        "choices": [
            {"text": "⚔️ 무기를 뽑아 들고 정면으로 맞서 싸운다", "succ": "고블린들을 무찌르고 금화를 챙겼습니다! (+40 Gold)", "fail": "상대의 수에 밀려 부상을 입었습니다. (-25 체력)", "succ_gold": 40, "fail_hp": 25},
            {"text": "🎯 옆쪽 좁은 샛길로 날렵하게 도망친다", "succ": "추격을 따돌리고 떨어진 보물 주머니를 발견했습니다! (+25 Gold)", "fail": "도망치다 가시 덩굴에 긁혔습니다. (-20 체력)", "succ_gold": 25, "fail_hp": 20}
        ]
    },
    {
        "type": "combat",
        "title": "외나무다리의 오우거",
        "desc": "거대한 협곡의 유일한 외나무다리 한가운데에 오우거가 몽둥이를 쥔 채 앉아있습니다. \"통행료를 내거나 몸으로 때워라!\"",
        "choices": [
            {"text": "⚔️ 약점을 노려 강력한 일격을 날린다", "succ": "오우거를 협곡 아래로 떨어뜨리고 보물을 얻었습니다! (+50 Gold)", "fail": "오우거의 몽둥이에 크게 맞았습니다. (-30 체력)", "succ_gold": 50, "fail_hp": 30},
            {"text": "🏃 다리 사이로 재주넘어 통과한다", "succ": "빠른 움직임으로 통과했습니다!", "fail": "오우거에게 잡혀 내팽개쳐졌습니다. (-25 체력)", "fail_hp": 25}
        ]
    },
    {
        "type": "combat",
        "title": "길목을 막아선 산적 패거리",
        "desc": "산길 곡예지점에서 칼을 든 산적 세 명이 나타났습니다. \"돈 될 만한 건 다 내놓고 가시지!\"",
        "choices": [
            {"text": "⚔️ 정면 돌파로 산적 두목을 제압한다", "succ": "두목을 기절시키자 산적들이 돈을 버리고 도망쳤습니다! (+45 Gold)", "fail": "산적들에게 구타당하고 돈을 빼앗겼습니다. (-20 체력, -15 Gold)", "succ_gold": 45, "fail_hp": 20, "fail_gold": 15},
            {"text": "✨ 화려한 말솜씨로 속인다", "succ": "산적들이 속아 다른 곳으로 달아났습니다! (+20 Gold)", "fail": "거짓말이 들통나 맞았습니다. (-25 체력)", "succ_gold": 20, "fail_hp": 25}
        ]
    },
    {
        "type": "event",
        "title": "신비로운 달빛의 마법 샘",
        "desc": "고요한 숲속 깊은 곳, 은은한 푸른빛을 발산하는 신비로운 샘가에 도달했습니다.",
        "choices": [
            {"text": "💧 샘물을 시원하게 마신다", "succ": "청량한 물이 피로를 씻어내 줍니다! (+30 체력 회복)", "fail": "배탈이 났습니다. (-15 체력)", "succ_hp": 30, "fail_hp": 15},
            {"text": "🪙 동전을 던지며 소원을 빈다", "succ": "행운이 찾아와 주머니가 두둑해졌습니다! (+45 Gold)", "fail": "아무 일도 일어나지 않았습니다.", "succ_gold": 45}
        ]
    },
    {
        "type": "event",
        "title": "버려진 모험가의 배낭",
        "desc": "나무 아래 오래전에 버려진 것으로 보이는 때 묻은 모험가의 배낭이 놓여 있습니다.",
        "choices": [
            {"text": "🔍 배낭 안을 신중하게 수색한다", "succ": "배낭 안에서 약간의 금화를 발견했습니다! (+25 Gold)", "fail": "배낭 안의 독충에게 물렸습니다. (-10 체력)", "succ_gold": 25, "fail_hp": 10},
            {"text": "🚫 그냥 지나친다", "succ": "안전하게 길을 계속 갑니다.", "fail": "아무 일도 없었습니다."}
        ]
    },
    {
        "type": "event",
        "title": "길가의 도박사",
        "desc": "한 남자가 주사위를 만지작거리며 부릅니다. \"한 판당 20골드! 인생 역전의 기회라구!\"",
        "choices": [
            {"text": "🎲 20골드를 내고 참여한다", "succ": "더블 6이 나왔습니다! 세 배로 받았습니다! (+50 Gold)", "fail": "돈을 잃었습니다. (-20 Gold)", "succ_gold": 50, "fail_gold": 20},
            {"text": "🚫 무시하고 지나간다", "succ": "지갑을 지켰습니다.", "fail": "아무 일도 없었습니다."}
        ]
    }
]

# 무작위 이벤트 선택
if st.session_state.current_event is None:
    st.session_state.current_event = random.choice(EVENTS)
    st.session_state.text_animated = False

event = st.session_state.current_event

st.title("📜 모험가 이야기: 탐험")
st.subheader(f"📍 {event['title']}")
desc_placeholder = st.empty()

# ---------------------------------------------------------
# 6. 타이핑 애니메이션
# ---------------------------------------------------------
if not st.session_state.text_animated:
    if st.button("⚡ 스킵 (텍스트 한 번에 보기)"):
        st.session_state.text_animated = True
        st.rerun()

    full_text = event["desc"]
    current_text = ""
    for char in full_text:
        current_text += char
        desc_placeholder.write(current_text)
        time.sleep(0.012)

    st.session_state.text_animated = True
    st.rerun()
else:
    desc_placeholder.write(event["desc"])

st.markdown("---")

# ---------------------------------------------------------
# 7. 상점 vs 일반 이벤트 분기
# ---------------------------------------------------------
if event.get("type") == "merchant":
    st.info("🛒 방랑 상인의 상점이 열렸습니다!")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧪 체력 포션")
        st.write("가격: **20 G** / 회복량: 30 HP")
        if st.button("포션 구매"):
            if st.session_state.gold >= 20:
                st.session_state.gold -= 20
                st.session_state.inventory.append("체력 포션")
                st.success("체력 포션을 구매했습니다!")
            else:
                st.error("골드가 부족합니다!")

    with col2:
        st.markdown("### ⚔️ 전설의 명검")
        st.write("가격: **80 G** / 전용 무기")
        if st.button("명검 구매"):
            if st.session_state.gold >= 80:
                if st.session_state.weapon != "전설의 명검":
                    st.session_state.gold -= 80
                    st.session_state.weapon = "전설의 명검"
                    st.success("전설의 명검을 장착했습니다!")
                else:
                    st.warning("이미 장착 중입니다.")
            else:
                st.error("골드가 부족합니다!")

    st.markdown("---")
    if st.button("🚪 상점을 나와 다시 길을 떠난다"):
        st.session_state.current_event = None
        st.session_state.text_animated = False
        st.rerun()

else:
    for i, choice in enumerate(event.get("choices", [])):
        if st.button(choice["text"], key=f"choice_{i}"):
            str_val = st.session_state.get('stat_str', 4)
            agi_val = st.session_state.get('stat_agi', 3)
            luk_val = st.session_state.get('stat_luk', 3)
            
            bonus = (str_val + agi_val + luk_val) * 2
            if "명검" in st.session_state.weapon:
                bonus += 15

            success_roll = random.randint(1, 100) - bonus

            if success_roll <= 50:
                st.success(choice["succ"])
                if "succ_gold" in choice:
                    st.session_state.gold += choice["succ_gold"] + (luk_val * 2)
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

            st.session_state.current_event = None
            st.session_state.text_animated = False
            st.rerun()
