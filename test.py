import streamlit as st
import random
import time

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "cat" not in st.session_state:
    st.session_state.cat = random.randint(1, 100)
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🐾 대형 맵 고양이 찾기 미니게임 🐾")
st.markdown("넓은 맵 속에서 고양이를 찾아 점수를 얻어보세요! 🐱")

# 게임 제한 시간 (초)
TIME_LIMIT = 45
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, TIME_LIMIT - elapsed)

st.write(f"⏰ 남은 시간: {remaining}초")
st.write(f"🌟 현재 점수: {st.session_state.score}")

MAP_SIZE = 100  # 전체 맵 크기 (버튼 개수)
COLUMNS = 10    # 한 줄에 표시될 버튼 수

if remaining <= 0:
    st.session_state.game_over = True
    st.success(f"게임 종료! 최종 점수는 {st.session_state.score}점이에요 🎉")
else:
    # 대형 맵 버튼 배치
    for row in range(MAP_SIZE // COLUMNS):
        cols = st.columns(COLUMNS)
        for col in range(COLUMNS):
            idx = row * COLUMNS + col + 1
            with cols[col]:
                if st.session_state.cat == idx:
                    if st.button("🐱", key=f"cat_{idx}"):
                        st.session_state.score += 1
                        st.session_state.cat = random.randint(1, MAP_SIZE)
                else:
                    st.button("🌲", key=f"tree_{idx}")

# 다시 시작 버튼
if st.session_state.game_over:
    if st.button("🔄 다시 시작"):
        st.session_state.score = 0
        st.session_state.cat = random.randint(1, MAP_SIZE)
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
