import streamlit as st
import random
import time

# -----------------------------
# 게임 데이터: 쓰레기 종류와 정답 분류
# -----------------------------
items = [
    {"name": "페트병", "type": "recycle", "img": "https://upload.wikimedia.org/wikipedia/commons/5/57/Plastic_bottle_icon.png"},
    {"name": "신문지", "type": "recycle", "img": "https://upload.wikimedia.org/wikipedia/commons/8/88/Newspaper_icon.png"},
    {"name": "종이컵", "type": "trash", "img": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Paper_cup_icon.png"},
    {"name": "바나나껍질", "type": "trash", "img": "https://upload.wikimedia.org/wikipedia/commons/4/46/Banana_icon.png"},
    {"name": "유리병", "type": "recycle", "img": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Wine_bottle_icon.png"},
    {"name": "스낵봉지", "type": "trash", "img": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Plastic_bag_icon.png"}
]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_start" not in st.session_state:
    st.session_state.time_start = None
if "current_item" not in st.session_state:
    st.session_state.current_item = random.choice(items)
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# -----------------------------
# 게임 시작
# -----------------------------
st.title("♻️ 분리수거 두더지 잡기 게임")
st.write("쓰레기를 보고 재활용인지 일반쓰레기인지 맞춰보세요! (제한 시간: 30초)")

if st.session_state.time_start is None:
    if st.button("게임 시작"):
        st.session_state.time_start = time.time()
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.current_item = random.choice(items)
else:
    # 시간 확인
    elapsed = time.time() - st.session_state.time_start
    remaining = 30 - int(elapsed)

    if remaining <= 0:
        st.session_state.game_over = True

    if not st.session_state.game_over:
        st.write(f"⏱ 남은 시간: {remaining}초")
        st.write(f"현재 점수: {st.session_state.score}")

        item = st.session_state.current_item
        st.image(item["img"], width=150)
        st.write(f"👉 이것은 **{item['name']}** 입니다. 분리수거는?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("♻️ 재활용"):
                if item["type"] == "recycle":
                    st.session_state.score += 1
                    st.success("정답! 재활용 가능 ✅")
                else:
                    st.session_state.score -= 1
                    st.error("틀렸어요 ❌ 일반쓰레기입니다")
                st.session_state.current_item = random.choice(items)

        with col2:
            if st.button("🗑 일반쓰레기"):
                if item["type"] == "trash":
                    st.session_state.score += 1
                    st.success("정답! 일반쓰레기 ✅")
                else:
                    st.session_state.score -= 1
                    st.error("틀렸어요 ❌ 재활용 가능합니다")
                st.session_state.current_item = random.choice(items)

    else:
        st.header("⏰ 게임 종료!")
        st.write(f"최종 점수: {st.session_state.score}점")
        if st.button("다시 시작"):
            st.session_state.time_start = None
            st.session_state.score = 0
            st.session_state.game_over = False
