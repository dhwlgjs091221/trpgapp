import streamlit as st

def character_creator_page():
    st.header("캐릭터 생성")
    name = st.text_input("이름")
    image = st.file_uploader("캐릭터 이미지 업로드")
    password = st.text_input("비밀번호", type="password")
    if st.button("저장"):
        st.success(f"{name} 캐릭터 저장됨 (비밀번호 보호됨)")