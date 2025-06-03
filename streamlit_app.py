import streamlit as st
import streamlit_drawable_canvas as canvas
from character_creator import character_creator_page
from websocket_client import setup_websocket
from config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET, WEBSOCKET_SERVER_URL
from supabase import create_client
import random, re, json

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
st.set_page_config(layout="wide")

# 세션 상태 초기화
def init_session():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "characters" not in st.session_state:
        st.session_state["characters"] = []
    if "background" not in st.session_state:
        st.session_state["background"] = None

init_session()

# 주사위 명령어 처리
def parse_dice_command(cmd):
    match = re.match(r"/r (\d+)d(\d+)([+-]\d+)?", cmd)
    if match:
        n, d, mod = int(match[1]), int(match[2]), match[3]
        rolls = [random.randint(1, d) for _ in range(n)]
        total = sum(rolls) + (int(mod) if mod else 0)
        return f"굴림 결과: {rolls} {'+'+mod if mod else ''} = {total}"
    return None

# 채팅 처리
def chat_interface():
    st.subheader("채팅창")
    for msg in st.session_state.messages:
        st.markdown(msg)

    user_msg = st.text_input("메시지 입력", key="chat")
    if st.button("보내기"):
        if user_msg.startswith("/r"):
            result = parse_dice_command(user_msg)
            st.session_state.messages.append(f"[SYSTEM] {result}")
        else:
            st.session_state.messages.append(f"[USER] {user_msg}")
        st.experimental_rerun()

# 캐릭터 렌더링
def render_characters():
    for char in st.session_state.characters:
        st.image(char["image_url"], caption=char["name"], width=64)
        if st.button(f"삭제 - {char['name']}", key=char['name']):
            st.session_state.characters.remove(char)
            st.experimental_rerun()

# 배경 설정 및 그림그리기
def drawing_interface():
    st.subheader("배경 이미지 및 그리기")
    bg_img = st.file_uploader("배경 이미지 업로드", type=["png", "jpg", "jpeg"])
    if bg_img:
        st.session_state.background = bg_img

    drawing_mode = st.selectbox("모드 선택", ["freedraw", "line", "rect", "circle"])
    stroke_width = st.slider("선 굵기", 1, 10, 3)
    stroke_color = st.color_picker("선 색상", "#000000")

    result = canvas.st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_image=st.session_state.background,
        update_streamlit=True,
        height=512,
        width=512,
        drawing_mode=drawing_mode,
        key="canvas",
    )

    if st.button("그림 지우기"):
        st.session_state.canvas = None
        st.experimental_rerun()

# 메인 페이지 라우팅
page = st.sidebar.selectbox("페이지 선택", ["TRPG 메인", "캐릭터 생성"])

if page == "캐릭터 생성":
    character_creator_page()
else:
    st.title("16x16 격자 TRPG 보드")
    drawing_interface()
    render_characters()
    chat_interface()
    setup_websocket(WEBSOCKET_SERVER_URL)
