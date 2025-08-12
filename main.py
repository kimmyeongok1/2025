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

# 예시 궁합 데이터 (랜덤 선택용)
compatibility_texts = [
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
    body {
        background: linear-gradient(120deg, #ffe6f0, #e6f7ff);
        font-family: 'Comic Sans MS', cursive;
    }
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #ff4d88;
        text-shadow: 2px 2px #ffd6e7;
        margin-bottom: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #ff80aa;
        margin-bottom: 40px;
    }
    .result-box {
        background-color: #fff0f5;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(255, 182, 193, 0.4);
        text-align: center;
    }
    .score {
        font-size: 36px;
        font-weight: bold;
        color: #ff3385;
    }
    .desc {
        font-size: 18px;
        color: #ff6699;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 4. UI
# ---------------------------
st.markdown("<div class='title'>💌 MBTI 궁합 테스트 💌</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>당신과 상대방의 MBTI 궁합을 귀여운 스타일로 확인하세요!</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    user_mbti = st.selectbox("💗 나의 MBTI", mbti_types)
with col2:
    partner_mbti = st.selectbox("💗 상대방 MBTI", mbti_types)

# ---------------------------
# 5. 결과 버튼
# ---------------------------
if st.button("궁합 확인하기 💕"):
    score_text, desc_text = random.choice(compatibility_texts)
    score_percent = random.randint(60, 100)  # 랜덤 점수
    img_url = random.choice(cute_images)

    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score'>{score_text} ({score_percent}%)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='desc'>{desc_text}</div>", unsafe_allow_html=True)
    st.image(img_url, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("※ 이 테스트는 재미용이며, 실제 성향과 다를 수 있습니다.")
