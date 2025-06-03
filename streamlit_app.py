import streamlit as st
from character_creator import character_creator_page
from websocket_client import setup_websocket
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
import streamlit_drawable_canvas as canvas

st.set_page_config(layout="wide")

# 페이지 선택: 상단 가로 메뉴
page = st.tabs(["TRPG 메인", "캐릭터 생성", "설정"])

with page[0]:
    st.title("16x16 격자 TRPG 보드")

    col1, col2 = st.columns([3,1])  # 좌우 비율 3:1

    with col1:
        st.write("여기에 16x16 격자 보드, 그림 그리기 기능 들어갑니다.")
        # 캔버스 예시 (추가 기능 넣어야 함)
        canvas_result = canvas.st_canvas(
            stroke_width=2,
            stroke_color="#000000",
            background_color="#fff",
            height=400,
            width=400,
            drawing_mode="freedraw",
            key="canvas",
        )
        # TODO: 그림 저장/불러오기, 지우기 기능 추가

    with col2:
        st.write("채팅창 (웹소켓 연결)")
        setup_websocket(WEBSOCKET_SERVER_URL)
        # TODO: 채팅 UI 구현, 명령어 파싱 등


with page[1]:
    character_creator_page()


with page[2]:
    st.header("설정")
    st.write("여기서 이미지 업로드 및 기타 설정을 합니다.")
    uploaded_file = st.file_uploader("캐릭터 이미지 업로드 (여기서만 가능)", type=["png","jpg","jpeg"])
    if uploaded_file:
        st.image(uploaded_file)
        # TODO: 업로드한 이미지 저장 처리
