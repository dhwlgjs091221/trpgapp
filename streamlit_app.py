import streamlit as st
from character_creator import character_creator_page
from websocket_client import setup_websocket, send_message, receive_messages
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas
import asyncio

st.set_page_config(layout="wide")

# --- 페이지 탭 ---
page = st.tabs(["TRPG 메인", "캐릭터 생성", "설정"])

# --- TRPG 메인 페이지 ---
with page[0]:
    st.title("16x16 격자 TRPG 보드")

    col1, col2 = st.columns([3,1])  # 좌우 3:1 비율

    with col1:
        st.write("여기에 16x16 격자 보드 및 그림 그리기")

        # 캔버스 크기, 셀 크기 설정 (16x16)
        canvas_size = 640  # 가로세로 픽셀 수
        grid_cells = 16
        cell_size = canvas_size // grid_cells

        # 격자 무늬 배경 그리기: 흰 배경 위에 격자선 수동 그리기
        # streamlit_drawable_canvas는 배경 이미지 지정 가능하므로 미리 그린 격자 이미지 넣어도 됨
        # 여기선 단순히 배경색으로 처리 (복잡한 격자 그리기는 따로 이미지 만들거나 JS 라이브러리 사용 필요)
        
        drawing_mode = st.radio("그리기 모드", ("freedraw", "select", "transform", "line"), horizontal=True)

        canvas_result = canvas.st_canvas(
            stroke_width=3,
            stroke_color="#000",
            background_color="#fff",
            height=canvas_size,
            width=canvas_size,
            drawing_mode=drawing_mode,
            key="canvas",
            # grid 설정 없음, 직접 격자 이미지 만들어 background_image로 넣어야함 (옵션)
            # 여기에 grid는 직접 그려야 하는데 streamlit_drawable_canvas에 grid 옵션 없음
        )

        # 선택해서 삭제하는 기능은 drawing_mode 'select' 상태에서
        # 유저가 선택 후 'Delete' 키 누르면 삭제 (JS 이벤트 필요)
        # Streamlit만으로는 키 이벤트 처리 어려움 -> 삭제 버튼 만들어서 선택된 요소 지우는 게 현실적

        if drawing_mode == "select":
            if st.button("선택된 도형 삭제"):
                if canvas_result.json_data is not None:
                    objects = canvas_result.json_data["objects"]
                    # 선택된 객체만 삭제
                    objects = [obj for obj in objects if not obj.get("active", False)]
                    # 이 상태로 다시 저장하는 기능 구현 필요 (복잡)
                    st.warning("삭제 후 다시 그리기 필요 - 현재는 수동 처리 필요")
                else:
                    st.info("선택된 객체가 없습니다.")

    with col2:
        st.write("채팅창")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # 채팅 메시지 입력
        new_msg = st.text_input("메시지 입력", key="chat_input")

        if st.button("전송") and new_msg.strip():
            st.session_state.chat_history.append(f"나: {new_msg}")
            # 실제 웹소켓 서버에 메시지 보내기 함수 호출 (비동기 문제로 따로 처리 필요)
            # send_message(new_msg)  # 별도 웹소켓 클라이언트 함수 호출

        # 채팅 내용 출력
        chat_area = st.empty()
        chat_area.text_area("채팅 기록", value="\n".join(st.session_state.chat_history), height=400, max_chars=None, key="chat_area", disabled=True)

        # TODO: 웹소켓에서 메시지 실시간 받아오도록 업데이트 필요

# --- 캐릭터 생성 페이지 ---
with page[1]:
    character_creator_page()

# --- 설정 페이지 ---
with page[2]:
    st.header("설정")
    st.write("여기서 이미지 업로드 및 기타 설정을 합니다.")
    uploaded_file = st.file_uploader("캐릭터 이미지 업로드 (여기서만 가능)", type=["png","jpg","jpeg"])
    if uploaded_file:
        st.image(uploaded_file)
        # TODO: 업로드한 이미지 저장 처리
