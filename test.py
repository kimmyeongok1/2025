import streamlit as st
import time
import random

# -----------------------------
# Dino Runner (Chrome 공룡 점프 느낌) - 큐트 스킨 버전
# 검정 덩어리처럼 보이던 요소들을 파스텔 색상과 윤곽선으로 표현
# -----------------------------

st.set_page_config(page_title="Dino Runner - Streamlit", page_icon="🦖", layout="centered")
st.title("🦖 공룡 점프 미니게임 (귀여운 테마)")
st.caption("버튼으로 점프! 장애물을 피해서 가능한 오래 달리세요.")

# ====== 설정값 ======
WIDTH = 800
HEIGHT = 240
GROUND_Y = 200
DINO_W, DINO_H = 42, 36
OBST_W = 28
GRAVITY = 1600.0        # px/s^2
JUMP_V = 600.0          # px/s
BASE_SPEED = 240.0      # px/s
SPEED_UP = 6.0          # 초당 속도 증가량
FRAME_DT = 1/60         # 60 FPS 비슷하게

# ====== 색상 팔레트 ======
COLORS = {
    "sky_top": "#fdfbff",
    "sky_bottom": "#e7f3ff",
    "ground": "#7a5b46",
    "cloud": "#ffffff",
    "dino_fill": "#8bd7a3",
    "dino_stroke": "#2e7d5b",
    "eye_white": "#ffffff",
    "eye_black": "#222222",
    "cactus_fill": "#a2e67b",
    "cactus_stroke": "#5a9f3a",
    "score": "#2b2b2b",
}

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
    ss.ob_h = random.choice([42, 50, 60])
if "next_gap" not in ss:
    ss.next_gap = random.randint(240, 360)

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
    ss.ob_h = random.choice([42, 50, 60])
    ss.next_gap = random.randint(240, 360)

def try_jump():
    """지면 접촉 시에만 점프"""
    on_ground = abs(ss.dino_y - (GROUND_Y - DINO_H)) < 0.5
    if on_ground and ss.running and not ss.game_over:
        ss.dino_vy = -JUMP_V

def collide():
    """AABB 충돌"""
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

st.write(":blue[조작법] 시작 누른 뒤, 🆙 점프 버튼을 눌러 장애물을 피해보세요!")

# ====== 렌더( SVG ) ======
def draw_cute_dino(x: float, y: float) -> str:
    """검정 사각형 대신 귀여운 공룡 (몸통/머리/꼬리/눈/다리) 구성"""
    body = f'<rect x="{x}" y="{y}" width="{DINO_W}" height="{DINO_H}" rx="8" fill="{COLORS["dino_fill"]}" stroke="{COLORS["dino_stroke"]}" stroke-width="2" />'
    head = f'<rect x="{x + DINO_W - 18}" y="{y - 10}" width="20" height="18" rx="6" fill="{COLORS["dino_fill"]}" stroke="{COLORS["dino_stroke"]}" stroke-width="2" />'
    tail = f'<polygon points="{x-10},{y+10} {x},{y+16} {x},{y+4}" fill="{COLORS["dino_fill"]}" stroke="{COLORS["dino_stroke"]}" stroke-width="2" />'
    leg1 = f'<rect x="{x+6}" y="{y + DINO_H}" width="8" height="10" rx="3" fill="{COLORS["dino_fill"]}" stroke="{COLORS["dino_stroke"]}" stroke-width="2" />'
    leg2 = f'<rect x="{x+20}" y="{y + DINO_H}" width="8" height="10" rx="3" fill="{COLORS["dino_fill"]}" stroke="{COLORS["dino_stroke"]}" stroke-width="2" />'
    eye_w = f'<circle cx="{x + DINO_W - 6}" cy="{y - 2}" r="3.6" fill="{COLORS["eye_white"]}" stroke="{COLORS["dino_stroke"]}" stroke-width="1" />'
    eye_b = f'<circle cx="{x + DINO_W - 6}" cy="{y - 2}" r="1.6" fill="{COLORS["eye_black"]}" />'
    blush = f'<circle cx="{x + DINO_W - 15}" cy="{y + 2}" r="2.2" fill="#ffb3c1" opacity="0.8" />'
    return f"<g>{body}{head}{tail}{leg1}{leg2}{eye_w}{eye_b}{blush}</g>"

def draw_cute_cactus(x: float, bottom_y: float, h: float) -> str:
    """사각형 한 덩어리 대신 여러 팔이 달린 선인장"""
    trunk_y = bottom_y - h
    trunk = f'<rect x="{x}" y="{trunk_y}" width="{OBST_W}" height="{h}" rx="6" fill="{COLORS["cactus_fill"]}" stroke="{COLORS["cactus_stroke"]}" stroke-width="2" />'
    # 왼팔/오른팔 (높이 무작위 살짝)
    arm_h1 = min(22, h - 18)
    arm_h2 = min(26, h - 14)
    left_arm = f'<rect x="{x-12}" y="{trunk_y + 18}" width="12" height="{arm_h1}" rx="6" fill="{COLORS["cactus_fill"]}" stroke="{COLORS["cactus_stroke"]}" stroke-width="2" />'
    right_arm = f'<rect x="{x+OBST_W}" y="{trunk_y + 10}" width="12" height="{arm_h2}" rx="6" fill="{COLORS["cactus_fill"]}" stroke="{COLORS["cactus_stroke"]}" stroke-width="2" />'
    return f"<g>{trunk}{left_arm}{right_arm}</g>"

def draw_svg() -> str:
    dino_x = 80
    ground_svg = f'<line x1="0" y1="{GROUND_Y}" x2="{WIDTH}" y2="{GROUND_Y}" stroke="{COLORS["ground"]}" stroke-width="4" />'

    # 구름 장식
    deco = []
    random.seed(42)
    for i in range(6):
        cx = (i * 130 + 60) % WIDTH
        cy = 44 + (i % 3) * 18
        deco.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{COLORS["cloud"]}" opacity="0.9" />')

    score_txt = f'<text x="{WIDTH-140}" y="28" font-size="18" fill="{COLORS["score"]}" font-family="monospace">Score: {int(ss.score)}</text>'
    high_txt = f'<text x="{WIDTH-140}" y="50" font-size="14" fill="{COLORS["score"]}" opacity="0.7" font-family="monospace">High: {int(ss.high)}</text>'

    dino = draw_cute_dino(dino_x, ss.dino_y)
    cactus = draw_cute_cactus(ss.ob_x, GROUND_Y, ss.ob_h)

    svg = f'''
    <svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{COLORS['sky_top']}" />
          <stop offset="100%" stop-color="{COLORS['sky_bottom']}" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#sky)" />
      {''.join(deco)}
      {ground_svg}
      {cactus}
      {dino}
      {score_txt}
      {high_txt}
    </svg>
    '''
    return svg

placeholder = st.empty()
status = st.empty()

# ====== 메인 루프 ======
if ss.running and not ss.game_over:
    steps = 0
    while ss.running and not ss.game_over and steps < 600:
        now = time.time()
        dt = min(0.05, max(0.0, now - ss.last_time))
        ss.last_time = now
        steps += 1

        # 물리 업데이트
        ss.dino_vy += GRAVITY * dt
        ss.dino_y += ss.dino_vy * dt
        ground_y = GROUND_Y - DINO_H
        if ss.dino_y > ground_y:
            ss.dino_y = ground_y
            ss.dino_vy = 0.0

        # 장애물 이동
        ss.ob_x -= ss.speed * dt
        if ss.ob_x < -OBST_W - 20:
            ss.ob_x = WIDTH + ss.next_gap
            ss.ob_h = random.choice([42, 50, 60])
            ss.next_gap = random.randint(240, 380)
            ss.speed += SPEED_UP * dt * 60

        # 점수
        ss.score += dt * 60 * 0.5  # 초당 약 30점

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

# 정지/게임오버 화면 렌더 (마지막 프레임 그리기)
svg = draw_svg()
placeholder.markdown(svg, unsafe_allow_html=True)

if ss.game_over:
    st.error("💥 부딪혔어요! ▶️ 시작/다시시작 을 눌러 재도전")
elif not ss.running:
    st.warning("▶️ 시작/다시시작 을 눌러 게임을 시작하세요. 🆙 점프로 장애물을 피하세요!")

# 푸터
st.caption("Made with Streamlit · SVG 기반 귀여운 스킨 · 색상/스킨을 더 바꾸고 싶으면 알려줘!")
