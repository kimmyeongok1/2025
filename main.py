import streamlit as st
import random

# ---------------------------
# 1. 데이터 준비
# ---------------------------
mbti_types = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

# MBTI 간단 성향 설명
mbti_descriptions = {
    "INTJ": "전략적인 사고와 계획을 중시하는 완벽주의자.",
    "INTP": "호기심 많고 창의적인 사색가.",
    "ENTJ": "리더십이 강하고 결단력 있는 지휘관.",
    "ENTP": "새로운 아이디어를 사랑하는 발명가.",
    "INFJ": "깊은 통찰력과 배려심을 지닌 이상주의자.",
    "INFP": "감성적이고 가치 중심적인 중재자.",
    "ENFJ": "타인을 이끄는 카리스마 있는 사회 지도자.",
    "ENFP": "열정적이고 자유로운 영혼.",
    "ISTJ": "책임감 있고 신뢰할 수 있는 관리자.",
    "ISFJ": "헌신적이고 세심한 수호자.",
    "ESTJ": "실용적이고 조직적인 리더.",
    "ESFJ": "사교적이고 친절한 협력가.",
    "ISTP": "문제 해결에 능한 현실주의자.",
    "ISFP": "감각적이고 자유로운 예술가.",
    "ESTP": "모험을 즐기는 실용주의자.",
    "ESFP": "사람들을 즐겁게 하는 분위기 메이커."
}

# 궁합 결과 예시 데이터
compatibility_levels = [
    ("💖 최고의 궁합!", "서로의 장단점을 보완하며 함께 성장하는 환상의 조합이에요!"),
    ("💞 좋은 궁합!", "함께 있으면 웃음이 끊이지 않는 사이가 될 수 있어요."),
    ("🌸 무난한 궁합", "큰 갈등 없이 조화롭게 지낼 수 있는 관계입니다."),
    ("🔥 도전적인 궁합", "서로 다른 점이 많지만, 노력한다면 큰 시너지를 낼 수 있어요."),
    ("❄️ 냉랭한 궁합?", "성향 차이가 크지만, 이해심을 가지면 새로운 세계를 배울 수 있습니다.")
]

# 귀여운 이미지/GIF 리스트
cute_images = [
    "https://i.ibb.co/x8B7hDk/cute-heart.gif",
    "https://i.ibb.co/b1rnpYk/cute-couple.gif",
    "https://i.ibb.co/mbZ8Jbm/cute-bear.gif",
    "https://i.ibb.co/7Qv3V6V/cute-cat.gif",
    "https://i.ibb.co/F6gr3gH/cute-bunny.gif"
]

# 관계 발전 팁
relationship_tips = [
    "서로의 차이를 존중하면 관계가 더 단단해져요.",
    "대화 습관(직접/간접), 계획성, 감정 표현 방식을 이해해보세요.",
    "갈등이 생기면 감정을 가라앉히고 차분히 이야기해보세요.",
    "공통 관심사를 찾아 함께 시간을 보내세요.",
    "서로의 장점을 칭찬하고 자주 표현하세요."
]

# ---------------------------
# 2. 페이지 설정
# ---------------------------
st.set_page_config(page_title="MBTI 궁합 테스트", page_icon="💖", layout="centered")

# ---------------------------
# 3. CSS 스타일
# ---------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff0f7 0%, #e6f7ff 100%);
        font-family: 'Comic Sans MS', 'Trebuchet MS', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 50px;
        font-weight: 800;
        color: #ff4d88;
        text-shadow: 2px 2px #ffd6e7;
        margin-top: 5px;
        margin-bottom: 8px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #ff80aa;
        margin-bottom: 40px;
    }
    .result-box {
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        margin-top: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }
    .score {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .desc {
        font-size: 17px;
        margin-bottom: 12px;
    }
    .tip-box {
        background: #fff7fc;
        border-left: 6px solid #ff99bb;
        padding: 12px;
        border-radius: 10px;
        margin-top: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 4. UI
# ---------------------------
st.markdown("<div class='title'>💌 MBTI 궁합 테스트 💌</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>화려하게 알려주는 나와 상대의 성향 궁합 — 재미로 즐겨보세요!</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    user_mbti = st.selectbox("💗 나의 MBTI", mbti_types)
with col2:
    partner_mbti = st.selectbox("💗 상대방 MBTI", mbti_types)

# ---------------------------
# 5. 결과 버튼
# ---------------------------
if st.button("궁합 확인하기 💕"):
    # 점수 계산
    base_score = random.randint(60, 95)
    if user_mbti == partner_mbti:
        base_score = min(100, base_score + 5)
    if user_mbti[0] == partner_mbti[0]:
        base_score = min(100, base_score + 3)
    if user_mbti[2] == partner_mbti[2]:
        base_score = min(100, base_score + 2)

    # 결과 선택
    score_text, desc_text = random.choice(compatibility_levels)
    img_url = random.choice(cute_images)
    tip = random.choice(relationship_tips)

    # 점수에 따라 카드 색상 변경
    if base_score >= 85:
        card_color = "#ffe6f0"
    elif base_score >= 70:
        card_color = "#fff0f7"
    else:
        card_color = "#f0f7ff"

    # 궁합 결과 박스
    st.markdown(
        f"""
        <div class='result-box' style='background:{card_color}'>
            <div class='score'>{score_text} — {base_score}%</div>
            <div class='desc'>{desc_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.image(img_url, use_container_width=True)

    # MBTI 성향 설명
    st.subheader("📌 MBTI 성향")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"**나 ({user_mbti})**: {mbti_descriptions[user_mbti]}")
    with col4:
        st.markdown(f"**상대 ({partner_mbti})**: {mbti_descriptions[partner_mbti]}")

    # 관계 팁
    st.subheader("💡 관계 발전 팁")
    st.markdown(f"<div class='tip-box'>✨ {tip}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("※ 이 테스트는 과학적 근거가 없는 재미용입니다.")
