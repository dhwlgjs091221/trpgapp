import streamlit as st
from character_creator import character_creator_page
from websocket_client import start_websocket as setup_websocket, send_message, get_received_messages as receive_messages
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas
import asyncio
import threading

# 페이지 레이아웃 고정 + 스크롤 제거 CSS
st.markdown(
    """
    <style>
    /* 스크롤 안보이게 */
    html, body, #root, .main {
        overflow: hidden;
        height: 100vh;
    }
    /* 캔버스 격자 스타일 */
    .grid-background {
        background-image:
          linear-gradient(to right, #ccc 1px, transparent 1px),
          linear-gradient(to bottom, #ccc 1px, transparent 1px);
        background-size: 40px 40px;  /* 셀 크기 40px */
        width: 640px;
        height: 640px;
    }
    /* 툴바 스타일 */
    .toolbar {
        display: flex;
        gap: 15px;
        padding: 10px;
        background-color: #eee;
        border-bottom: 1px solid #ccc;
        align-items: center;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    .toolbar button {
        background: #f5f5f5;
        border: 1px solid #ccc;
        padding: 6px 12px;
        border-radius: 3px;
        cursor: pointer;
    }
    .toolbar button.selected {
        background: #0078d7;
        color: white;
        border-color: #0078d7;
    }
    </style>
    """, unsafe_allow_html=True
)

st.set_page_config(layout="wide")

# --- 웹소켓 메시지 수신 백그라운드 처리 ---
if "ws_messages" not in st.session_state:
    st.session_state.ws_messages = []
if "ws_running" not in st.session_state:
    st.session_state.ws_running = False

def websocket_receiver_loop():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    async def runner():
        async for msg in receive_messages():
            st.session_state.ws_messages.append(msg)
            st.experimental_rerun()
    loop.run_until_complete(runner())

if not st.session_state.ws_running:
    setup_websocket(WEBSOCKET_SERVER_URL)
    threading.Thread(target=websocket_receiver_loop, daemon=True).start()
    st.session_state.ws_running = True

# --- 페이지 탭 ---
page = st.tabs(["TRPG 메인", "캐릭터 생성", "설정"])

# --- TRPG 메인 페이지 ---
with page[0]:
    st.title("16x16 격자 TRPG 보드")

    col1, col2 = st.columns([3,1])  # 좌우 3:1 비율

    with col1:
        st.write("16x16 격자 보드 및 그림 그리기")

        canvas_size = 640
        grid_cells = 16
        cell_size = canvas_size // grid_cells

        # 도구 상태: pen, eraser, line, rect 등 - 기본 pen
        if "tool" not in st.session_state:
            st.session_state.tool = "freedraw"

        # 윈도우 10 스타일 툴바를 상단에 html 버튼 대신 Streamlit 버튼으로 구현
        tools = [
            ("펜", "freedraw"),
            ("지우개", "eraser"),
            ("선", "line"),
            ("사각형", "rect"),
            ("원", "circle"),
        ]

        # 툴 버튼 가로 바 구현
        cols = st.columns(len(tools))
        for i, (label, tool_val) in enumerate(tools):
            is_selected = (st.session_state.tool == tool_val)
            btn_label = f"**{label}**" if is_selected else label
            if cols[i].button(btn_label):
                st.session_state.tool = tool_val

        canvas_result = canvas.st_canvas(
            stroke_width=3,
            stroke_color="#000" if st.session_state.tool != "eraser" else "#fff",
            background_color="#fff",
            height=canvas_size,
            width=canvas_size,
            drawing_mode=st.session_state.tool,
            key="canvas",
        )

    with col2:
        st.write("채팅")

        chat_area = st.empty()
        chat_area.text_area("채팅 기록", value="\n".join(st.session_state.ws_messages), height=600, disabled=True)

        new_msg = st.text_input("메시지 입력", key="chat_input")
        send_clicked = st.button("전송")

        if send_clicked and new_msg.strip():
            st.session_state.ws_messages.append(f"나: {new_msg}")
            asyncio.run(send_message(new_msg))
            st.session_state.chat_input = ""
            st.experimental_rerun()

# --- 캐릭터 생성 페이지 ---
with page[1]:
    character_creator_page()

# --- 설정 페이지 ---
with page[2]:
    st.header("설정")
    st.write("여기서 이미지 업로드 및 기타 설정을 합니다.")
    uploaded_file = st.file_uploader("캐릭터 이미지 업로드 (여기서만 가능)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file)
        # TODO: 업로드한 이미지 저장 처리
