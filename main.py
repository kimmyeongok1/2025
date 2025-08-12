import streamlit as st

# MBTI별 추천 직업 데이터
mbti_jobs = {
    "INTJ": ["데이터 과학자", "전략 컨설턴트", "연구원"],
    "INTP": ["프로그래머", "이론 물리학자", "UX 디자이너"],
    "ENTJ": ["경영 컨설턴트", "프로젝트 매니저", "기업가"],
    "ENTP": ["광고 기획자", "마케터", "벤처 창업가"],
    "INFJ": ["심리상담가", "작가", "인권 변호사"],
    "INFP": ["일러스트레이터", "시인", "사회복지사"],
    "ENFJ": ["강사", "HR 매니저", "외교관"],
    "ENFP": ["여행 작가", "방송 작가", "콘텐츠 크리에이터"],
    "ISTJ": ["회계사", "변호사", "군 장교"],
    "ISFJ": ["간호사", "교사", "사서"],
    "ESTJ": ["경찰관", "사업가", "공무원"],
    "ESFJ": ["이벤트 플래너", "영업 관리자", "홍보 담당자"],
    "ISTP": ["기계공", "파일럿", "스포츠 트레이너"],
    "ISFP": ["사진작가", "패션 디자이너", "음악가"],
    "ESTP": ["세일즈 전문가", "응급 구조사", "프로 운동선수"],
    "ESFP": ["배우", "가수", "관광 가이드"],
}

st.set_page_config(page_title="MBTI 진로 추천", page_icon="💼")

# 제목
st.title("💼 MBTI 기반 진로 추천 앱")

# MBTI 선택
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_jobs.keys()))

# 추천 버튼
if st.button("추천 직업 보기"):
    jobs = mbti_jobs.get(selected_mbti, [])
    if jobs:
        st.subheader(f"🔍 {selected_mbti} 추천 직업")
        for job in jobs:
            st.write(f"- {job}")
    else:
        st.warning("추천 직업이 없습니다. 😢")

# 부가 설명
st.markdown("---")
st.caption("이 앱은 단순 참고용입니다. 직업 선택은 다양한 요소를 고려하세요!")

