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
    :root {
        --accent-1: #ff4d88;
        --accent-2: #ff80aa;
        --panel-bg: rgba(255, 240, 245, 0.9);
        --shadow: rgba(255, 182, 193, 0.35);
    }
    .stApp {
        background: linear-gradient(120deg, #fff0f7, #e6f7ff);
        font-family: 'Comic Sans MS', 'Trebuchet MS', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: var(--accent-1);
        text-shadow: 2px 2px #ffd6e7;
        margin-top: 10px;
        margin-bottom: 6px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: var(--accent-2);
        margin-bottom: 30px;
    }
    .card {
        background: var(--panel-bg);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 8px 24px var(--shadow);
    }
    .result-box {
        background: linear-gradient(180deg, #fff7fb, #fff0f7);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        text-align: center;
        margin-top: 14px;
    }
    .score {
        font-size: 34px;
        font-weight: 800;
        color: #ff2e6d;
        margin-bottom: 6px;
    }
    .desc {
        font-size: 16px;
        color: #ff6f9a;
        margin-bottom: 12px;
    }
    .mbti-select {
        font-weight: 700;
    }
    /* 버튼 스타일 (경미한 커스터마이즈) */
    .stButton>button {
        background: linear-gradient(90deg, #ff8ab8, #ff5a94);
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 12px;
        font-weight: 700;
    }
    .stButton>button:hover {
        filter: brightness(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 4. UI
# ---------------------------
st.markdown("<div class='title'>💌 MBTI 궁합 테스트 💌</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>귀여운 디자인으로 나와 상대의 성향 궁합을 확인해보세요 — 재미로만 이용해주세요!</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        user_mbti = st.selectbox("💗 나의 MBTI", mbti_types, key="user_mbti")
    with col2:
        partner_mbti = st.selectbox("💗 상대방 MBTI", mbti_types, key="partner_mbti")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# 5. 결과 버튼
# ---------------------------
if st.button("궁합 확인하기 💕"):
    # 간단한 '랜덤+조금 의미있는' 연출:
    # 같은 유형이면 조금 더 높은 점수, 비슷한 1~2글자 일치하면 보정 등
    base_score = random.randint(65, 95)
    if user_mbti == partner_mbti:
        base_score = min(100, base_score + 5)
    # 같은 외향/내향 (첫글자) 보정
    if user_mbti[0] == partner_mbti[0]:
        base_score = min(100, base_score + 3)
    # 같은 판단/인식 (세번째 글자: T/F or J/P) 보정
    if user_mbti[2] == partner_mbti[2]:
        base_score = min(100, base_score + 2)

    score_text, desc_text = random.choice(compatibility_texts)
    img_url = random.choice(cute_images)

    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score'>{score_text} — {base_score}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='desc'>{desc_text}</div>", unsafe_allow_html=True)
    # 변경된 부분: use_container_width 사용 (deprecated된 use_column_width 대신)
    st.image(img_url, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 추가: 간단 팁 카드
    st.markdown(
        """
        <div style="margin-top:10px;border-radius:12px;padding:12px;background:linear-gradient(90deg,#fff7fc,#fff1f6);box-shadow:0 6px 18px rgba(255,182,193,0.18)">
        <strong>✨ 궁합 팁</strong>
        <ul style="margin-top:8px;">
            <li>서로의 차이를 존중하면 관계가 더 단단해져요.</li>
            <li>대화 습관(직접/간접), 계획성, 감정 표현 방식을 이해해보세요.</li>
            <li>이 앱은 참고용이에요 — 실제 관계는 더 복잡합니다!</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.caption("※ 이 테스트는 재미용이며, 실제 성향과 다를 수 있습니다.")
