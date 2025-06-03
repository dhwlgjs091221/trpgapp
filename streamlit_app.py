import streamlit as st

# ✅ 페이지 설정은 최상단에서 먼저 설정해야 함
st.set_page_config(layout="wide")

from character_creator import character_creator_page
from websocket_client import start_websocket as setup_websocket, send_message, get_received_messages as receive_messages
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas
import asyncio
import threading

# 전체 화면 고정 스타일 삽입 (스크롤 방지 + 채팅창 고정 위치 설정)
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        overflow: hidden;
    }
    #fixed-chat-box {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 300px;
        background-color: #f1f1f1;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        z-index: 9999;
    }
    #fixed-chat-box textarea {
        width: 100%;
        height: 150px;
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

    # 레이아웃: 보드
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

    # ✅ 고정 채팅창 영역 (HTML로 직접 삽입)
    chat_html = """
    <div id="fixed-chat-box">
        <h4>💬 채팅</h4>
        <form action="#" method="post">
            <textarea readonly id="chat_log">{chat_log}</textarea><br>
            <input type="text" id="chat_input" name="msg" placeholder="메시지 입력" style="width: 75%;">
            <button type="button" onclick="sendChat()">전송</button>
        </form>
    </div>
    <script>
    const input = window.parent.document.getElementById("chat_input")
    if (input) input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            window.parent.document.querySelector("button").click();
        }
    });
    </script>
    """.format(chat_log="\n".join(st.session_state.get("chat_history", [])))
    st.markdown(chat_html, unsafe_allow_html=True)

    # 실질적 채팅 처리 (숨겨진 영역)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    new_msg = st.text_input("숨김 채팅 입력", label_visibility="collapsed", key="hidden_chat_input")
    if new_msg.strip():
        st.session_state.chat_history.append(f"나: {new_msg}")
        send_message(new_msg)
        new_msg = ""

    received_msgs = receive_messages()
    if received_msgs:
        st.session_state.chat_history.extend(received_msgs)

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
