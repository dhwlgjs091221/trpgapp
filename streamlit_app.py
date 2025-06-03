import streamlit as st
from character_creator import character_creator_page
from websocket_client import start_websocket as setup_websocket, send_message, get_received_messages as receive_messages
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas
import asyncio
import threading

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
            # UI 갱신용
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

        drawing_mode = st.radio("그리기 모드", ("freedraw", "select", "transform", "line"), horizontal=True)

        # streamlit_drawable_canvas에 배경 격자 그리기: 투명 배경에 CSS로 격자 표시
        grid_style = f"""
            <style>
            .grid-background {{
                background-image:
                  linear-gradient(to right, #ccc 1px, transparent 1px),
                  linear-gradient(to bottom, #ccc 1px, transparent 1px);
                background-size: {cell_size}px {cell_size}px;
                width: {canvas_size}px;
                height: {canvas_size}px;
                }}
            </style>
        """
        st.markdown(grid_style, unsafe_allow_html=True)

        canvas_result = canvas.st_canvas(
            stroke_width=3,
            stroke_color="#000",
            background_color="#fff",
            height=canvas_size,
            width=canvas_size,
            drawing_mode=drawing_mode,
            key="canvas",
        )

        # 선택된 도형 삭제 기능
        if drawing_mode == "select":
            if st.button("선택된 도형 삭제"):
                if canvas_result.json_data and "objects" in canvas_result.json_data:
                    new_objects = [obj for obj in canvas_result.json_data["objects"] if not obj.get("active", False)]
                    # 이거는 그냥 상태에 반영 못함, 다시 그리기 위해선 저장 후 재로딩 필요
                    st.warning("삭제 후 다시 그리기 위해 페이지를 새로고침해주세요.")
                else:
                    st.info("선택된 도형이 없습니다.")

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
