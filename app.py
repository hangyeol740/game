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
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=800",  # 어두운 숲
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
        "image": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?q=80&w=800",  # 뒤집힌 수레길
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
        "image": "https://images.unsplash.com/photo-1544967082-d9d25d867d66?q=80&w=800",  # 고대 성벽 유적
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
        "image": "https://images.unsplash.com/photo-1511447333015-45b65e60f6d5?q=80&w=800",  # 신비한 연기와 집
        "desc": "수상한 연기가 피어오르는 오두막에서 기묘한 차림의 마녀가 솥에 묘약을 끓이고 있습니다.",
        "choices": [
            {
                "text": "🧠 묘약의 성분을 파악하여 위험한 재료인지 확인한다",
                "stat": "int", "diff": 14,
                "succ": "마녀의 실수를 지적해 주고 보상으로 신비한 묘약을 나누어 마셨습니다! (+30 체력 회복)",
                "fail": "마녀의 비기 재료를 건드렸다가 분노한 마녀의 저주에 당했습니다. (-20 체력)",
                "succ_hp": 30, "fail_hp": 20
