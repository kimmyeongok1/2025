import streamlit as st
import time
import random

# ------------------------------
# Circle Runner (흑백, 점점 빨라지는 여러 장애물)
# ------------------------------

st.set_page_config(page_title="Circle Runner", layout="centered")
st.title("⚪ Circle Runner")
st.caption("점프 버튼으로 장애물을 피하세요!")

# ====== 게임 설정 ======
WIDTH = 600
HEIGHT = 300
GROUND_Y = 260
CIRCLE_RADIUS = 15
OBST_W = 20
OBST_H = 40
GRAVITY = 1
JUMP_V = -15
BASE_SPEED = 3  # 시작 속도를 조금 느리게
SPEEDUP = 0.02  # 점점 빨라짐
NUM_OBST = 3    # 장애물 개수

# ====== 세션 상태 초기화 ======
ss = st.session_state
for key, val in [
    ("running", False), ("game_over", False),
    ("circle_y", GROUND_Y), ("velocity", 0),
    ("obstacles", []), ("speed", BASE_SPEED),
    ("score", 0), ("high", 0), ("frame_count", 0)
]:
    if key not in ss:
        ss[key] = val

# 장애물 초기화
if not ss.obstacles:
    ss.obstacles = [{"x": WIDTH + i*250} for i in range(NUM_OBST)]

# ====== 유틸 함수 ======
def reset_game():
    ss.running = True
    ss.game_over = False
    ss.circle_y = GROUND_Y
    ss.velocity = 0
    ss.speed = BASE_SPEED
    ss.score = 0
    ss.frame_count = 0
    # 장애물 초기화
    ss.obstacles = [{"x": WIDTH + i*250} for i in range(NUM_OBST)]

def jump():
    if ss.circle_y >= GROUND_Y:
        ss.velocity = JUMP_V

def collide():
    circle_x = 50
    for ob in ss.obstacles:
        ob_x = ob["x"]
        ob_y = GROUND_Y - OBST_H
        overlap_x = (circle_x - CIRCLE_RADIUS < ob_x + OBST_W) and (ob_x < circle_x + CIRCLE_RADIUS)
        overlap_y = (ss.circle_y - CIRCLE_RADIUS < ob_y + OBST_H) and (ob_y < ss.circle_y + CIRCLE_RADIUS)
        if overlap_x and overlap_y:
            return True
    return False

# ====== UI ======
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("▶️ 시작/다시시작"):
        reset_game()
with col2:
    if st.button("⬆ 점프"):
        jump()
with col3:
    st.metric("🏆 최고점", f"{int(ss.high)}")

# ====== 게임 로직 ======
def game_step():
    if not ss.running or ss.game_over:
        return
    ss.frame_count += 1

    # 중력
    ss.velocity += GRAVITY
    ss.circle_y += ss.velocity
    if ss.circle_y > GROUND_Y:
        ss.circle_y = GROUND_Y
        ss.velocity = 0

    # 장애물 이동
    for ob in ss.obstacles:
        ob["x"] -= ss.speed
        if ob["x"] < -OBST_W:
            ob["x"] = WIDTH + random.randint(100, 300)
            ss.speed += SPEEDUP  # 점점 빨라짐

    # 점수 (10프레임마다 +1)
    if ss.frame_count % 10 == 0:
        ss.score += 1

    # 충돌 체크
    if collide():
        ss.game_over = True
        ss.running = False
        ss.high = max(ss.high, ss.score)

# ====== 화면 렌더 ======
def draw_game():
    circle_x = 50
    svg = f"""
    <svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">
        <!-- 배경 -->
        <rect width="{WIDTH}" height="{HEIGHT}" fill="white" />
        <!-- 땅 -->
        <rect y="{GROUND_Y + CIRCLE_RADIUS}" width="{WIDTH}" height="{HEIGHT - GROUND_Y}" fill="black" />
        <!-- 점수 -->
        <text x="10" y="20" font-family="monospace" font-size="16" fill="black">Score: {int(ss.score)}</text>
        <text x="10" y="40" font-family="monospace" font-size="14" fill="gray">High: {int(ss.high)}</text>
        <!-- 공룡 → 동그라미 -->
        <circle cx="{circle_x}" cy="{ss.circle_y}" r="{CIRCLE_RADIUS}" fill="black" />
        <!-- 장애물들 -->
        {''.join([f'<rect x="{ob["x"]}" y="{GROUND_Y - OBST_H}" width="{OBST_W}" height="{OBST_H}" fill="black" />' for ob in ss.obstacles])}
    </svg>
    """
    st.write(svg, unsafe_allow_html=True)

# ====== 메인 루프 ======
game_step()
draw_game()

if ss.game_over:
    st.error("💥 충돌! ▶️ 시작/다시시작 버튼으로 재도전")
elif not ss.running:
    st.info("▶️ 시작/다시시작 버튼으로 게임을 시작하세요!")

# 자동 새로고침
time.sleep(0.05)
st.rerun()
