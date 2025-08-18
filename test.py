import streamlit as st
import time
import random

# -----------------------------
# Dino Runner (Chrome 공룡 점프 느낌)
# -----------------------------
# 키보드 직접 감지는 Streamlit 기본 기능에선 제한적이라
# "점프" 버튼으로 조작하는 버전입니다. (간단/안정)
# -----------------------------

st.set_page_config(page_title="Dino Runner - Streamlit", page_icon="🦖", layout="centered")
st.title("🦖 공룡 점프 미니게임 (Streamlit)")
st.caption("버튼으로 점프! 장애물을 피해서 가능한 오래 달리세요.")

# ====== 설정값 ======
WIDTH = 800
HEIGHT = 220
GROUND_Y = 180
DINO_W, DINO_H = 36, 36
OBST_W, OBST_H = 26, 48
GRAVITY = 1600.0        # px/s^2
JUMP_V = 600.0          # px/s (위로는 음수 대신 y축 아래 양수 기준이라 절댓값 처리)
BASE_SPEED = 240.0      # px/s
SPEED_UP = 6.0          # 초당 속도 증가량
FRAME_DT = 1/60         # 60 FPS 비슷하게

# ====== 세션 상태 ======
ss = st.session_state
if "running" not in ss:
    ss.running = False
if "game_over" not in ss:
    ss.game_over = False
if "dino_y" not in ss:
    ss.dino_y = GROUND_Y - DINO_H
if "dino_vy" not in ss:
    ss.dino_vy = 0.0
if "ob_x" not in ss:
    ss.ob_x = WIDTH + 200
if "speed" not in ss:
    ss.speed = BASE_SPEED
if "score" not in ss:
    ss.score = 0.0
if "high" not in ss:
    ss.high = 0.0
if "last_time" not in ss:
    ss.last_time = time.time()

# 난이도 가변 장애물 높이/간격
if "ob_h" not in ss:
    ss.ob_h = OBST_H
if "next_gap" not in ss:
    ss.next_gap = 260

# ====== 유틸 ======
def reset_game():
    ss.running = True
    ss.game_over = False
    ss.dino_y = GROUND_Y - DINO_H
    ss.dino_vy = 0.0
    ss.ob_x = WIDTH + 200
    ss.speed = BASE_SPEED
    ss.score = 0.0
    ss.last_time = time.time()
    ss.ob_h = random.choice([42, 48, 56])
    ss.next_gap = random.randint(240, 360)

# 점프 (지면 접촉 시에만)
def try_jump():
    on_ground = abs(ss.dino_y - (GROUND_Y - DINO_H)) < 0.5
    if on_ground and ss.running and not ss.game_over:
        ss.dino_vy = -JUMP_V

# 충돌 체크 (AABB)
def collide():
    dino_x, dino_y = 80, ss.dino_y
    ob_x, ob_y = ss.ob_x, GROUND_Y - ss.ob_h
    overlap_x = (dino_x < ob_x + OBST_W) and (ob_x < dino_x + DINO_W)
    overlap_y = (dino_y < ob_y + ss.ob_h) and (ob_y < dino_y + DINO_H)
    return overlap_x and overlap_y

# ====== 상단 UI ======
left, mid, right = st.columns([1,1,1])
with left:
    if st.button("▶️ 시작/다시시작", use_container_width=True):
        reset_game()
with mid:
    if st.button("🆙 점프", use_container_width=True):
        try_jump()
with right:
    st.metric(label="🏆 최고점", value=f"{int(ss.high)}")

st.write(":blue[조작법] 시작 누른 뒤, 🆙 점프 버튼을 반복해서 눌러 장애물을 피해보세요!")

# ====== 렌더( SVG ) ======
def draw_svg():
    dino_x = 80
    # 공룡 이모지 대신 단색 캐릭터(SVG)로 표현
    dino_svg = f'<rect x="{dino_x}" y="{ss.dino_y}" width="{DINO_W}" height="{DINO_H}" rx="6" />'
    ground_svg = f'<line x1="0" y1="{GROUND_Y}" x2="{WIDTH}" y2="{GROUND_Y}" stroke-width="3" />'
    cactus = f'<rect x="{ss.ob_x}" y="{GROUND_Y-ss.ob_h}" width="{OBST_W}" height="{ss.ob_h}" rx="4" />'
    # 구름/별 장식 (아기자기)
    deco = []
    random.seed(42)  # 프레임마다 변하면 깜빡임 -> 고정
    for i in range(6):
        cx = (i*130 + 60) % WIDTH
        cy = 40 + (i%3)*18
        deco.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="white" opacity="0.6" />')
    score_txt = f'<text x="{WIDTH-120}" y="30" font-size="18">Score: {int(ss.score)}</text>'
    high_txt = f'<text x="{WIDTH-120}" y="54" font-size="14" opacity="0.7">High: {int(ss.high)}</text>'

    svg = f'''
    <svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#f7f9ff" />
          <stop offset="100%" stop-color="#e9f2ff" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#sky)" />
      {''.join(deco)}
      <g fill="#222" stroke="#222">{ground_svg}{cactus}{dino_svg}</g>
      <g fill="#222" font-family="monospace">{score_txt}{high_txt}</g>
    </svg>
    '''
    return svg

placeholder = st.empty()
status = st.empty()

# ====== 메인 루프 ======
if ss.running and not ss.game_over:
    # 간단한 타임 스텝 루프 (최대 20초 * 60fps = 1200프레임 등 안전장치)
    # Streamlit은 긴 루프에 민감하니 짧게 끊어 그려줍니다.
    steps = 0
    while ss.running and not ss.game_over and steps < 600:
        now = time.time()
        dt = min(0.05, max(0.0, now - ss.last_time))
        ss.last_time = now
        steps += 1

        # 물리 업데이트
        ss.dino_vy += GRAVITY * dt
        ss.dino_y += ss.dino_vy * dt
        # 지면 충돌 처리
        ground_y = GROUND_Y - DINO_H
        if ss.dino_y > ground_y:
            ss.dino_y = ground_y
            ss.dino_vy = 0.0

        # 장애물 이동
        ss.ob_x -= ss.speed * dt
        if ss.ob_x < -OBST_W:
            ss.ob_x = WIDTH + ss.next_gap
            ss.ob_h = random.choice([42, 48, 56])
            ss.next_gap = random.randint(240, 380)
            ss.speed += SPEED_UP * dt * 60  # 프레임 보정 가속

        # 점수
        ss.score += dt * 60 * 0.5  # 초당 약 30점 -> 0.5 * 60 = 30

        # 충돌 체크
        if collide():
            ss.game_over = True
            ss.running = False
            ss.high = max(ss.high, ss.score)

        # 렌더
        svg = draw_svg()
        placeholder.markdown(svg, unsafe_allow_html=True)
        status.info(f"속도: {int(ss.speed)}  |  점수: {int(ss.score)}  |  최고점: {int(ss.high)}")

        time.sleep(FRAME_DT)

# 정지/게임오버 화면 렌더
svg = draw_svg()
placeholder.markdown(svg, unsafe_allow_html=True)

if ss.game_over:
    st.error("💥 부딪혔어요! ▶️ 시작/다시시작 을 눌러 재도전")
elif not ss.running:
    st.warning("▶️ 시작/다시시작 을 눌러 게임을 시작하세요. 🆙 점프로 장애물을 피하세요!")

# 푸터
st.caption("Made with Streamlit · 간단 SVG 렌더 + 버튼 입력 · 키보드 입력을 원하면 커스텀 컴포넌트 연동 방법도 안내해 드릴게요.")
