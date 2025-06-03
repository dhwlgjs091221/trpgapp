import streamlit as st
from character_creator import character_creator_page
from websocket_client import start_websocket as setup_websocket, send_message, get_received_messages as receive_messages
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas
import asyncio
import threading
import time

st.set_page_config(layout="wide")

# --- 페이지 탭 ---
page = st.tabs(["TRPG 메인", "캐릭터 생성", "설정"])

# --- 웹소켓 백그라운드 수신 처리 ---
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
    loop.run_until_complete(runner())

if not st.session_state.ws_running:
    setup_websocket(WEBSOCKET_SERVER_URL)
    threading.Thread(target=websocket_receiver_loop, daemon=True).start()
    st.session_state.ws_running = True

# --- TRPG 메인 페이지 ---
with page[0]:
    st.title("16x16 격자 TRPG 보드")

    col1, col2 = st.columns([3,1])  # 좌우 3:1 비율

    with col1:
        st.write("16x16 격자 보드 및 그림 그리기")

        canvas_size = 640
        grid_cells = 16
        cell_size = canvas_size // grid_cells

        # 배경에 격자 무늬 만들기 (canvas 자체에 grid 옵션 없으니 배경 이미지 대신 CSS 격자 스타일로 격자 느낌)
        grid_style = f"""
            <style>
            .grid-background {{
                background-image:
                  linear-gradient(to right, #bbb 1px, transparent 1px),
                  linear-gradient(to bottom, #bbb 1px, transparent 1px);
                background-size: {cell_size}px {cell_size}px;
                width: {canvas_size}px;
                height: {canvas_size}px;
                position: relative;
                }}
            </style>
        """
        st.markdown(grid_style, unsafe_allow_html=True)
        st.markdown('<div class="grid-background">', unsafe_allow_html=True)

        drawing_mode = st.radio("그리기 모드", ("freedraw", "select", "transform", "line"), horizontal=True)

        canvas_result = canvas.st_canvas(
            stroke_width=3,
            stroke_color="#000",
            background_color="#fff",
            height=canvas_size,
            width=canvas_size,
            drawing_mode=drawing_mode,
            key="canvas",
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # 선택된 도형 삭제 기능
        if drawing_mode == "select":
            if st.button("선택된 도형 삭제"):
                if canvas_result.json_data and "objects" in canvas_result.json_data:
                    new_objects = [obj for obj in canvas_result.json_data["objects"] if not obj.get("active", False)]
                    canvas_result.json_data["objects"] = new_objects
                    st.experimental_rerun()
                else:
                    st.info("선택된 도형이 없습니다.")

    with col2:
        st.write("채팅창 (입력창은 아래)")

        # 채팅 내역 출력
        chat_display = st.empty()
        chat_display.text_area("채팅 기록", value="\n".join(st.session_state.ws_messages + st.session_state.get("chat_history", [])),
                               height=550, max_chars=None, key="chat_area", disabled=True)

    # 채팅 입력창은 페이지 맨 아래 고정
    new_msg = st.text_input("메시지 입력", key="chat_input")
    send_clicked = st.button("전송")

    if send_clicked and new_msg.strip():
        st.session_state.ws_messages.append(f"나: {new_msg}")
        asyncio.run(send_message(new_msg))  # 웹소켓으로 메시지 전송
        st.session_state.chat_input = ""  # 입력 초기화
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
