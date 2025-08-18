import streamlit as st
import time
import random

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "dino_y" not in st.session_state:
    st.session_state.dino_y = 260   # 공룡 위치 위로 조정
if "velocity" not in st.session_state:
    st.session_state.velocity = 0
if "obstacle_x" not in st.session_state:
    st.session_state.obstacle_x = 600
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "speed" not in st.session_state:
    st.session_state.speed = 5
if "frame_count" not in st.session_state:
    st.session_state.frame_count = 0

gravity = 1
jump_power = -15
ground_level = 260

# 게임 초기화
def reset_game():
    st.session_state.score = 0
    st.session_state.dino_y = ground_level
    st.session_state.velocity = 0
    st.session_state.obstacle_x = 600
    st.session_state.game_over = False
    st.session_state.speed = 5
    st.session_state.frame_count = 0

# 점프 동작
def jump():
    if st.session_state.dino_y >= ground_level:
        st.session_state.velocity = jump_power

# 프레임 진행
def game_step():
    if st.session_state.game_over:
        return

    # 프레임 카운트 증가
    st.session_state.frame_count += 1

    # 중력 적용
    st.session_state.velocity += gravity
    st.session_state.dino_y += st.session_state.velocity

    if st.session_state.dino_y >= ground_level:
        st.session_state.dino_y = ground_level
        st.session_state.velocity = 0

    # 장애물 이동
    st.session_state.obstacle_x -= st.session_state.speed
    if st.session_state.obstacle_x < -40:
        st.session_state.obstacle_x = 600
        st.session_state.speed += 0.5  # 점점 빨라짐

    # 점수는 10프레임마다 +1
    if st.session_state.frame_count % 10 == 0:
        st.session_state.score += 1

    # 충돌 판정
    if abs(50 - st.session_state.obstacle_x) < 40 and st.session_state.dino_y > 220:
        st.session_state.game_over = True
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

# 화면 그리기
def draw_game():
    dino_y = st.session_state.dino_y
    obstacle_x = st.session_state.obstacle_x

    svg = f"""
    <svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
        <!-- 하늘 -->
        <rect width="600" height="300" fill="lightblue" />
        <!-- 땅 -->
        <rect y="280" width="600" height="20" fill="tan" />

        <!-- 공룡 -->
        <rect x="50" y="{dino_y}" width="30" height="30" fill="green" stroke="black" stroke-width="2"/>
        <circle cx="70" cy="{dino_y+5}" r="5" fill="white" stroke="black"/>
        <circle cx="72" cy="{dino_y+5}" r="2" fill="black"/>

        <!-- 장애물 (선인장) -->
        <rect x="{obstacle_x}" y="240" width="20" height="40" fill="darkgreen" stroke="black" stroke-width="2"/>
        <rect x="{obstacle_x-10}" y="250" width="10" height="20" fill="darkgreen" stroke="black" stroke-width="2"/>
        <rect x="{obstacle_x+20}" y="250" width="10" height="20" fill="darkgreen" stroke="black" stroke-width="2"/>
    </svg>
    """
    st.write(svg, unsafe_allow_html=True)

# UI 영역
st.title("🐱 귀여운 러너 게임")
st.write(f"점수: {st.session_state.score} | 최고점: {st.session_state.high_score}")

col1, col2 = st.columns(2)
if col1.button("점프!"):
    jump()
if col2.button("다시 시작"):
    reset_game()

# 게임 루프 (한 번만 실행되며 rerun으로 갱신)
game_step()
draw_game()

if st.session_state.game_over:
    st.write("💀 게임 오버!")

# 자동 새로고침 (0.05초 간격)
time.sleep(0.05)
st.experimental_rerun()
