import streamlit as st
import random
import time

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "mole" not in st.session_state:
    st.session_state.mole = random.randint(1, 9)
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🐹 두더지 잡기 미니게임 🐹")
st.markdown("귀엽고 아기자기한 두더지를 잡아 점수를 얻어보세요!")

# 게임 제한 시간 (초)
TIME_LIMIT = 30
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, TIME_LIMIT - elapsed)

st.write(f"⏰ 남은 시간: {remaining}초")
st.write(f"🌟 현재 점수: {st.session_state.score}")

if remaining <= 0:
    st.session_state.game_over = True
    st.success(f"게임 종료! 최종 점수는 {st.session_state.score}점이에요 🎉")
else:
    # 3x3 버튼 그리드 (두더지 위치 랜덤)
    cols = st.columns(3)
    for i in range(1, 10):
        with cols[(i-1) % 3]:
            if st.session_state.mole == i:
                if st.button("🐹", key=f"mole_{i}"):
                    st.session_state.score += 1
                    st.session_state.mole = random.randint(1, 9)
            else:
                st.button("🌱", key=f"grass_{i}")

# 다시 시작 버튼
if st.session_state.game_over:
    if st.button("🔄 다시 시작"):
        st.session_state.score = 0
        st.session_state.mole = random.randint(1, 9)
        st.session_state.start_time = time.time()
        st.session_state.game_over = False

