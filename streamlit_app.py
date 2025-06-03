import streamlit as st

# ✅ 페이지 설정은 최상단에서 먼저 설정해야 함
st.set_page_config(layout="wide")

from character_creator import character_creator_page
from websocket_client import start_websocket as setup_websocket, send_message, get_received_messages as receive_messages
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas
import asyncio
import threading

# 전체 화면 고정 스타일 삽입 (스크롤 방지)
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# --- 페이지 탭 ---
tabs = st.tabs(["TRPG 메인", "캐릭터 생성", "설정"])

# --- TRPG 메인 ---
with tabs[0]:
    st.title("16x16 격자 TRPG 보드")

    # 도구 바: 그리기/지우개 선택 (가로 배치)
    tool_col1, tool_col2, tool_col3 = st.columns([1, 1, 8])
    with tool_col1:
        drawing_tool = st.radio("도구", ["펜", "지우개"], horizontal=True, label_visibility="collapsed")

    # 레이아웃: 보드 + 채팅창 (채팅창은 아래쪽 고정)
    board_col, _ = st.columns([4, 1])
    with board_col:
        st.subheader("격자 보드 및 그림")

        canvas_size = 800
        grid_cells = 16
        cell_size = canvas_size // grid_cells

        drawing_mode = "freedraw" if drawing_tool == "펜" else "eraser"

        canvas_result = canvas.st_canvas(
            stroke_width=4,
            stroke_color="#000000",
            background_color="#ffffff",
            height=canvas_size,
            width=canvas_size,
            drawing_mode=drawing_mode,
            key="main_canvas"
        )

    st.divider()

    # 채팅 기능 - 하단 고정
    st.subheader("💬 채팅")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 채팅 메시지 입력
    chat_col1, chat_col2 = st.columns([5, 1])
    with chat_col1:
        new_msg = st.text_input("", label_visibility="collapsed", placeholder="메시지 입력")
    with chat_col2:
        if st.button("전송") and new_msg.strip():
            st.session_state.chat_history.append(f"나: {new_msg}")
            send_message(new_msg)

    # 수신 메시지 출력
    received_msgs = receive_messages()
    if received_msgs:
        st.session_state.chat_history.extend(received_msgs)

    chat_display = st.empty()
    chat_display.text_area("채팅 기록", value="\n".join(st.session_state.chat_history), height=200, disabled=True)

# --- 캐릭터 생성 ---
with tabs[1]:
    character_creator_page()

# --- 설정 페이지 ---
with tabs[2]:
    st.header("설정")
    st.write("여기서 캐릭터 이미지 등을 업로드하세요.")
    uploaded_file = st.file_uploader("캐릭터 이미지 업로드 (여기서만 가능)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="업로드된 캐릭터 이미지")
