import streamlit as st
import random
import time

# =========================
# 게임 데이터 (이미지 없음)
# type: "separate" = 분리배출(재활용/특수수거), "trash" = 일반쓰레기
# =========================
ITEMS = [
    {"name": "휴지곽(골판지)", "type": "separate"},   # 종이/골판지 분리배출
    {"name": "핸드폰(폐휴대폰)", "type": "separate"}, # 전자폐기물 수거함
    {"name": "배터리(건전지)", "type": "separate"},   # 폐건전지 수거함
    {"name": "형광등", "type": "separate"},           # 전용수거함
    {"name": "우유팩(깨끗한)", "type": "separate"},   # 종이팩 전용수거
    {"name": "음료 캔", "type": "separate"},          # 캔류
    {"name": "비닐봉지(깨끗한)", "type": "separate"}, # 필름류(지자체별 상이할 수 있음)
    {"name": "샴푸통(플라스틱)", "type": "separate"}, # 플라스틱
    {"name": "스티로폼 트레이(깨끗한)", "type": "separate"}, # 발포수지
    {"name": "CD/DVD", "type": "trash"},              # 보통 일반쓰레기(지역별 상이)
    {"name": "깨진 도자기 접시", "type": "trash"},    # 재활용 불가
    {"name": "거울", "type": "trash"},                # 재활용 불가
    {"name": "종이 영수증(감열지)", "type": "trash"}, # 재활용 불가
    {"name": "일회용 나무젓가락", "type": "trash"},   # 일반쓰레기
    {"name": "껌", "type": "trash"},                  # 일반쓰레기
]

TIME_LIMIT = 30  # 초

# =========================
# 유틸: 새 문제 큐 생성
# =========================
def make_queue():
    # 모든 항목을 섞어서 한 바퀴 생성
    q = ITEMS.copy()
    random.shuffle(q)
    return q

def refill_queue_if_needed():
    # 큐가 너무 짧아지면 새 묶음을 뒤에 붙임
    if len(st.session_state.queue) < 3:
        st.session_state.queue += make_queue()

def start_game():
    st.session_state.score = 0
    st.session_state.time_start = time.time()
    st.session_state.game_over = False
    st.session_state.queue = make_queue()
    st.session_state.current = st.session_state.queue.pop(0)  # 현재 문제
    st.session_state.q_index = 0      # 질문 번호(라디오 키 리셋용)
    st.session_state.feedback = ""    # 직전 정오표시

def submit_answer(choice):
    item = st.session_state.current
    correct = (item["type"] == "separate" and choice == "분리배출") or \
              (item["type"] == "trash" and choice == "일반쓰레기")
    if correct:
        st.session_state.score += 1
        st.session_state.feedback = "✅ 정답!"
    else:
        st.session_state.score -= 1
        st.session_state.feedback = f"❌ 오답! ({item['name']} → " + \
            ("분리배출" if item["type"] == "separate" else "일반쓰레기") + ")"

    # 다음 문제로 진행: '미리보기'였던 항목이 곧바로 현재 문제가 됨
    if st.session_state.queue:
        st.session_state.current = st.session_state.queue.pop(0)
    refill_queue_if_needed()
    st.session_state.q_index += 1  # 라디오 키 변경(선택 리셋)

# =========================
# 세션 상태 초기화
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_start" not in st.session_state:
    st.session_state.time_start = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current" not in st.session_state:
    st.session_state.current = None
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# =========================
# UI
# =========================
st.title("♻️ 분리수거 퀵 퀴즈 (이미지 없이 텍스트 버전)")
st.caption("지방자치단체별 분리 배출 기준이 다를 수 있어요. 이 게임은 일반적인 기준에 맞춘 연습용입니다.")

if st.session_state.time_start is None or st.session_state.game_over:
    if st.button("게임 시작 / 다시 시작"):
        start_game()
else:
    # 시간 계산
    elapsed = int(time.time() - st.session_state.time_start)
    remaining = TIME_LIMIT - elapsed
    if remaining <= 0:
        st.session_state.game_over = True

    if not st.session_state.game_over:
        # 점수/타이머
        st.metric("남은 시간", f"{remaining}초")
        st.metric("점수", f"{st.session_state.score}")

        # 현재 문제
        st.subheader("현재 문제")
        st.markdown(f"### 👉 **{st.session_state.current['name']}** 는(은) 어디로?")
        choice = st.radio(
            "정답을 선택하세요",
            ["분리배출", "일반쓰레기"],
            index=None,
            key=f"answer_{st.session_state.q_index}",
            horizontal=True
        )

        # 제출 버튼 (한 번의 이벤트로 상태 업데이트)
        if st.button("제출"):
            if choice is None:
                st.warning("먼저 정답을 선택해주세요!")
            else:
                submit_answer(choice)

        # 피드백
        if st.session_state.feedback:
            st.info(st.session_state.feedback)

        # 다음 문제 미리보기 (큐의 맨 앞이 다음 문제)
        if st.session_state.queue:
            st.divider()
            st.subheader("다음 문제(미리보기) 👀")
            st.markdown(f"**{st.session_state.queue[0]['name']}**")

    else:
        st.header("⏰ 게임 종료!")
        st.write(f"최종 점수: **{st.session_state.score}**점")
        if st.button("다시 시작"):
            start_game()
