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
    .fixed-chat-wrapper {
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 280px;
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 8px;
        z-index: 9999;
        font-size: 14px;
    }
    .fixed-chat-wrapper textarea {
        width: 100%;
        height: 200px;
        resize: none;
        font-size: 12px;
    }
    .fixed-chat-wrapper input[type="text"] {
        width: 70%;
        font-size: 12px;
    }
    .fixed-chat-wrapper button {
        width: 28%;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 페이지 탭 ---
tabs = st.tabs(["TRPG 메인", "캐릭터 생성", "설정"])

# --- TRPG 메인 ---
with tabs[0]:
    # 도구 바: 그리기/지우개 선택 (가로 배치)
    tool_col1, tool_col2, tool_col3 = st.columns([1, 1, 8])
    with tool_col1:
        drawing_tool = st.radio("도구", ["펜", "지우개"], horizontal=True, label_visibility="collapsed")

    # 레이아웃: 보드
    board_col, _ = st.columns([4, 1])
    with board_col:
        canvas_size = 800
        grid_cells = 16
        cell_size = canvas_size // grid_cells

        drawing_mode = "freedraw"
        stroke_color = "#000000" if drawing_tool == "펜" else "#ffffff"

        canvas_result = canvas.st_canvas(
            stroke_width=4,
            stroke_color=stroke_color,
            background_color="#ffffff",
            height=canvas_size,
            width=canvas_size,
            drawing_mode=drawing_mode,
            key="main_canvas"
        )

    # ✅ 고정 채팅창 영역 (HTML로 직접 삽입)
    chat_log = "\n".join(st.session_state.get("chat_history", []))
    chat_html = f"""
    <div class='fixed-chat-wrapper'>
        <b>💬 채팅</b>
        <textarea readonly id='chat_log'>{chat_log}</textarea><br>
        <input type='text' id='chat_input' name='msg' placeholder='메시지 입력'>
        <button onclick="sendMessage()">전송</button>
    </div>
    <script>
    function sendMessage() {{
        const input = window.parent.document.getElementById('chat_input');
        const value = input.value;
        if (value.trim() !== '') {{
            const streamlitInput = window.parent.document.querySelectorAll('input[data-testid="stTextInput"]')[0];
            if (streamlitInput) {{
                streamlitInput.value = value;
                const inputEvent = new Event('input', {{ bubbles: true }});
                streamlitInput.dispatchEvent(inputEvent);
                input.value = '';
            }}
        }}
    }}
    window.parent.document.getElementById('chat_input')?.addEventListener("keypress", function(e) {{
        if (e.key === "Enter") {{
            e.preventDefault();
            sendMessage();
        }}
    }});
    </script>
    """
    st.markdown(chat_html, unsafe_allow_html=True)

    # 실질적 채팅 처리 (숨겨진 영역)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    new_msg = st.text_input("숨김 채팅 입력", label_visibility="collapsed", key="hidden_chat_input")
    if new_msg.strip():
        st.session_state.chat_history.append(f"나: {new_msg}")
        send_message(new_msg)

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
