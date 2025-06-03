import streamlit as st
from character_creator import character_creator_page
from websocket_client import setup_websocket
from config import SUPABASE_URL
from config import SUPABASE_KEY
from config import STORAGE_BUCKET
from config import WEBSOCKET_SURVER_URL

st.set_page_config(layout="wide")

# 페이지 라우팅
page = st.sidebar.selectbox("페이지 선택", ["TRPG 메인", "캐릭터 생성"])

if page == "캐릭터 생성":
    character_creator_page()
else:
    st.title("16x16 격자 TRPG 보드")
    st.write("여기에 보드, 채팅창, 캐릭터 렌더링, 주사위 굴림 등이 들어갑니다.")
    setup_websocket(WEBSOCKET_SERVER_URL)
