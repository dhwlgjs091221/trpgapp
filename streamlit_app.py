import streamlit as st
from character_creator import character_creator_page
from websocket_client import start_websocket as setup_websocket, send_message, get_received_messages as receive_messages
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas

# 1) 페이지 설정은 무조건 가장 상단에 위치해야 함
st.set_page_config(layout="wide")

# 2) 스크롤 제거 및 채팅창 고정 CSS 추가
st.markdown("""
    <style>
    html, body, [class*="css"] {
        overflow: hidden !important;  /* 스크롤 숨기기 */
        height: 100vh; /* 화면 높이 고정 */
    }
    /* 채팅창 고정 박스 */
    .fixed-chat-wrapper {
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 300px;
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 8px;
        z-index: 9999;
        font-size: 13px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .fixed-chat-wrapper textarea {
        width: 100%;
        height: 180px;
        resize: none;
        font-size: 12px;
        padding: 4px;
        border-radius: 4px;
    }
    .fixed-chat-wrapper input[type="text"] {
        width: 70%;
        font-size: 12px;
        padding: 4px;
        margin-top: 6px;
        border-radius: 4px;
        border: 1px solid #ccc;
    }
    .fixed-chat-wrapper button {
        width: 28%;
        font-size: 12px;
        padding: 5px 0;
        margin-left: 4%;
        border-radius: 4px;
        background-color: #0b79d0;
        color: white;
        border: none;
        cursor: pointer;
    }
    .fixed-chat-wrapper button:hover {
        background-color: #095a9d;
    }
    /* 도구 바 스타일 */
    .tool-bar {
        display: flex;
        gap: 20px;
        padding: 10px 0;
        border-bottom: 1px solid #ddd;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 페이지 탭 ---
tabs = st.tabs(["TRPG 메인", "캐릭터 생성", "설정"])

# --- TRPG 메인 페이지 ---
with tabs[0]:
    # 도구 바 (가로로 배치)
    drawing_tool = st.radio("도구 선택", ["펜", "지우개"], horizontal=True, label_visibility="collapsed")

    # 캔버스 설정
    canvas_size = 800
    grid_cells = 16
    cell_size = canvas_size // grid_cells

    stroke_color = "#000000" if drawing_tool == "펜" else "#ffffff"
    stroke_width = 4 if drawing_tool == "펜" else 20  # 지우개는 굵게

    # 캔버스 그리기
    canvas_result = canvas.st_canvas(
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#ffffff",
        height=canvas_size,
        width=canvas_size,
        drawing_mode="freedraw",
        key="main_canvas"
    )

    # 채팅창 고정 HTML + JS (우측 하단)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_log = "\n".join(st.session_state.chat_history)
    chat_html = f"""
    <div class='fixed-chat-wrapper'>
        <b>💬 채팅</b>
        <textarea readonly id='chat_log'>{chat_log}</textarea><br>
        <input type='text' id='chat_input' placeholder='메시지 입력'>
        <button onclick="sendMessage()">전송</button>
    </div>

    <script>
    function sendMessage() {{
        const input = document.getElementById('chat_input');
        const value = input.value.trim();
        if (value === '') return;
        const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput"]');
        if (streamlitInput) {{
            streamlitInput.value = value;
            streamlitInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.value = '';
        }}
    }}
    document.getElementById('chat_input').addEventListener("keypress", function(e) {{
        if (e.key === "Enter") {{
            e.preventDefault();
            sendMessage();
        }}
    }});
    </script>
    """
    st.markdown(chat_html, unsafe_allow_html=True)

    # 숨겨진 입력 텍스트로 메시지 처리
    new_msg = st.text_input("숨김 채팅 입력", label_visibility="collapsed", key="hidden_chat_input")
    if new_msg.strip():
        st.session_state.chat_history.append(f"나: {new_msg}")
        send_message(new_msg)

    received_msgs = receive_messages()
    if received_msgs:
        st.session_state.chat_history.extend(received_msgs)

# --- 캐릭터 생성 페이지 ---
with tabs[1]:
    character_creator_page()

# --- 설정 페이지 ---
with tabs[2]:
    st.header("설정")
    st.write("여기서 캐릭터 이미지 등을 업로드하세요.")
    uploaded_file = st.file_uploader("캐릭터 이미지 업로드 (여기서만 가능)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="업로드된 캐릭터 이미지")
