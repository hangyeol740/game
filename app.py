import streamlit as st

# 페이지 설정 (반응형 레이아웃 및 브라우저 탭 이름 설정)
st.set_page_config(
    page_title="모험가 이야기 RPG",
    page_icon="🗡️",
    layout="centered"
)

# ---------------------------------------------------------
# 1. 게임 상태(Session State) 초기화
# 세션 상태는 사용자가 버튼을 누르거나 페이지가 새로고침되어도 
# 데이터(체력, 골드 등)가 사라지지 않게 유지해 줍니다.
# ---------------------------------------------------------
if "hp" not in st.session_state:
    st.session_state.hp = 100         # 현재 체력
    st.session_state.max_hp = 100     # 최대 체력
    st.session_state.gold = 50        # 소지 골드
    st.session_state.weapon = "녹슨 단검" # 장착한 무기
    st.session_state.attack = 10      # 공격력
    st.session_state.stage = "마을"   # 현재 위치 (마을, 사냥터, 상점, 이벤트 등)
    st.session_state.log = "모험의 땅에 오신 것을 환영합니다!" # 게임 진행 상황 메시지

# ---------------------------------------------------------
# 2. 화면 상단: 상태창 (플레이어 정보)
# ---------------------------------------------------------
st.title("🗡️ 모험가 이야기 RPG")
st.markdown("외부 도구 없이 Python과 Streamlit으로 만든 텍스트 RPG입니다.")

# 3개의 열로 나누어 상태를 깔끔하게 표시 (반응형 지원)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="❤️ 체력", value=f"{st.session_state.hp} / {st.session_state.max_hp}")
with col2:
    st.metric(label="💰 골드", value=f"{st.session_state.gold} G")
with col3:
    st.metric(label="⚔️ 공격력", value=str(st.session_state.attack))
with col4:
    st.metric(label="🗡️ 장비", value=st.session_state.weapon)

st.divider()

# ---------------------------------------------------------
# 3. 게임 로그 (최근 행동 결과 출력)
# ---------------------------------------------------------
st.info(f"📢 **상황 로그:** {st.session_state.log}")

# ---------------------------------------------------------
# 4. 게임 스테이지별 로직 및 선택지
# ---------------------------------------------------------

# [1] 마을 상태
if st.session_state.stage == "마을":
    st.subheader("🏡 평화로운 마을")
    st.write("다양한 모험을 준비하는 안전한 마을입니다. 다음 행동을 선택하세요.")
    
    # 버튼을 누르면 현재 스테이지가 변경되거나 이벤트가 발생합니다.
    if st.button("🌲 숲으로 사냥하러 가기", use_container_width=True):
        st.session_state.stage = "사냥터"
        st.session_state.log = "몬스터가 도사리는 숲에 입장했습니다."
        st.rerun() # 화면을 즉시 새로고침하여 변경된 상태를 반영
        
    if st.button("🛒 아이템 상점 가기", use_container_width=True):
        st.session_state.stage = "상점"
        st.session_state.log = "상점에 입장했습니다. 필요한 물품을 구매하세요."
        st.rerun()

    if st.button("🛌 여관에서 휴식하기 (비용: 10 골드)", use_container_width=True):
        if st.session_state.gold >= 10:
            st.session_state.gold -= 10
            st.session_state.hp = st.session_state.max_hp
            st.session_state.log = "여관에서 편안하게 휴식을 취해 체력이 모두 회복되었습니다! (-10 골드)"
        else:
            st.session_state.log = "골드가 부족하여 여관을 이용할 수 없습니다!"
        st.rerun()

# [2] 사냥터 상태
elif st.session_state.stage == "사냥터":
    st.subheader("🌲 위험한 숲")
    st.write("몬스터를 사냥해 골드를 모으고 모험을 즐기세요.")
    
    if st.button("⚔️ 슬라임 사냥하기", use_container_width=True):
        st.session_state.gold += 15
        st.session_state.log = "슬라임을 물리치고 15 골드를 획득했습니다!"
        st.rerun()
        
    if st.button("🔥 숲의 보스(고블린) 도전하기", use_container_width=True):
        if st.session_state.attack >= 15:
            st.session_state.gold += 50
            st.session_state.log = "고블린을 멋지게 물리치고 보상으로 50 골드를 얻었습니다!"
        else:
            st.session_state.hp -= 30
            st.session_state.log = "공격력이 부족해 고블린에게 당했습니다! 체력 30 감소."
            if st.session_state.hp <= 0:
                st.session_state.stage = "게임오버"
        st.rerun()

    if st.button("🏃 마을로 돌아가기", use_container_width=True):
        st.session_state.stage = "마을"
        st.session_state.log = "안전하게 마을로 돌아왔습니다."
        st.rerun()

# [3] 상점 상태
elif st.session_state.stage == "상점":
    st.subheader("🛒 잡화점")
    st.write("더 강한 장비를 구매하여 모험을 유리하게 만드세요.")
    
    # 이미 구매했는지 여부에 따른 조건문 처리
    if st.session_state.weapon == "녹슨 단검":
        if st.button("🗡️ 철검 구매하기 (가격: 30 골드)", use_container_width=True):
            if st.session_state.gold >= 30:
                st.session_state.gold -= 30
                st.session_state.weapon = "철검"
                st.session_state.attack = 20
                st.session_state.log = "철검을 구매했습니다! 공격력이 20으로 증가합니다."
            else:
                st.session_state.log = "골드가 부족합니다!"
            st.rerun()
    else:
        st.write("✨ 이미 상점에서 판매하는 최고의 장비를 소유하고 있습니다!")

    if st.button("🏡 마을 광장으로 돌아가기", use_container_width=True):
        st.session_state.stage = "마을"
        st.session_state.log = "상점에서 나왔습니다."
        st.rerun()

# [4] 게임 오버 상태
elif st.session_state.stage == "게임오버":
    st.error("💀 체력이 0이 되어 쓰러졌습니다... 게임 오버!")
    
    if st.button("🔄 게임 다시 시작하기", use_container_width=True):
        # 모든 상태를 처음으로 초기화
        st.session_state.hp = 100
        st.session_state.max_hp = 100
        st.session_state.gold = 50
        st.session_state.weapon = "녹슨 단검"
        st.session_state.attack = 10
        st.session_state.stage = "마을"
        st.session_state.log = "새로운 모험이 다시 시작됩니다."
        st.rerun()
