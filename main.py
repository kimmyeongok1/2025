import streamlit as st

# MBTI 궁합 데이터 (귀여운 이미지 포함)
mbti_compatibility = {
    ("INTJ", "ENFP"): {
        "score": "💖 90%",
        "desc": "서로의 부족함을 채워주는 최고의 궁합!",
        "img": "https://i.ibb.co/x8B7hDk/cute-heart.gif"
    },
    ("ENFP", "INTJ"): {
        "score": "💖 90%",
        "desc": "서로의 부족함을 채워주는 최고의 궁합!",
        "img": "https://i.ibb.co/x8B7hDk/cute-heart.gif"
    },
    ("INFJ", "ENTP"): {
        "score": "💞 85%",
        "desc": "새로운 시각과 깊은 이해가 만나는 조합!",
        "img": "https://i.ibb.co/b1rnpYk/cute-couple.gif"
    },
    ("ENTP", "INFJ"): {
        "score": "💞 85%",
        "desc": "새로운 시각과 깊은 이해가 만나는 조합!",
        "img": "https://i.ibb.co/b1rnpYk/cute-couple.gif"
    },
    ("ISTJ", "ESFP"): {
        "score": "🌸 80%",
        "desc": "서로를 보완하는 안정-자유 조합!",
        "img": "https://i.ibb.co/mbZ8Jbm/cute-bear.gif"
    },
    ("ESFP", "ISTJ"): {
        "score": "🌸 80%",
        "desc": "서로를 보완하는 안정-자유 조합!",
        "img": "https://i.ibb.co/mbZ8Jbm/cute-bear.gif"
    },
}

mbti_types = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

# 페이지 설정
st.set_page_config(page_title="MBTI 궁합 테스트", page_icon="💖", layout="centered")

# CSS로 배경색, 폰트 스타일 조정
st.markdown(
    """
    <style>
    body {
        background-color: #FFF8F8;
        font-family: 'Comic Sans MS', cursive;
    }
    .title {
        text-align: center;
        font-size: 36px;
        color: #FF69B4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 제목
st.markdown("<div class='title'>💌 귀여운 MBTI 궁합 테스트 💌</div>", unsafe_allow_html=True)
st.write("당신과 상대방의 MBTI 궁합을 확인해보세요! (재미용)")

# 선택
col1, col2 = st.columns(2)
with col1:
    user_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_types)
with col2:
    partner_mbti = st.selectbox("상대방 MBTI를 선택하세요:", mbti_types)

# 버튼
if st.button("궁합 확인하기 💕"):
    result = mbti_compatibility.get((user_mbti, partner_mbti))
    if result:
        st.subheader(f"✨ 궁합 점수: {result['score']}")
        st.write(f"**설명:** {result['desc']}")
        st.image(result['img'], use_column_width=True)
    else:
        st.subheader("🤔 무난한 궁합")
        st.write("평범한 조합이에요. 서로를 이해하려는 마음이 중요해요!")
        st.image("https://i.ibb.co/7Qv3V6V/cute-cat.gif", use_column_width=True)

# 하단 안내
st.markdown("---")
st.caption("※ 이 결과는 과학적 근거가 없는 재미용입니다.")

