import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import io

st.set_page_config(layout="wide")

# 세션 상태 초기화
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "board_image" not in st.session_state:
    # 16x16 칸, 각 칸 30px, 흰 배경
    board_size = 16
    cell_px = 30
    img = Image.new("RGBA", (board_size*cell_px, board_size*cell_px), (255, 255, 255, 255))
    # 격자 그리기
    draw = ImageDraw.Draw(img)
    for i in range(board_size + 1):
        # 가로선
        draw.line((0, i*cell_px, board_size*cell_px, i*cell_px), fill=(200,200,200))
        # 세로선
        draw.line((i*cell_px, 0, i*cell_px, board_size*cell_px), fill=(200,200,200))
    st.session_state.board_image = img

if "drawing_mode" not in st.session_state:
    st.session_state.drawing_mode = "draw"  # draw or erase

if "characters" not in st.session_state:
    st.session_state.characters = {}  # 캐릭터 저장용 dict

# --- 레이아웃 구성 ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 16x16 격자 보드 (그리기 가능)")

    # 격자판 이미지 출력
    img = st.session_state.board_image
    st.image(img, use_column_width=False, width=board_size*cell_px)

    # 그림 그리기 / 지우기 도구 선택
    mode = st.radio("도구 선택", options=["그리기", "지우기"], index=0 if st.session_state.drawing_mode=="draw" else 1)
    st.session_state.drawing_mode = "draw" if mode == "그리기" else "erase"

    # 그림 그리기 영역 - 마우스 클릭으로는 안됨 (Streamlit 제한)
    st.info("현재 Streamlit에서는 직접 마우스 드로잉은 불가능합니다.\n대신 그림 파일을 업로드하여 보드 위에 덧씌우는 방식을 사용하세요.")

    # 그림 이미지 업로드 (그림 또는 지우기용 투명 배경 이미지)
    uploaded_img = st.file_uploader("그림 또는 지우기용 이미지 업로드 (PNG 권장, 투명 배경 가능)", type=["png","jpg","jpeg"])
    if uploaded_img is not None:
        uploaded_pil = Image.open(uploaded_img).convert("RGBA").resize((board_size*cell_px, board_size*cell_px))
        base = st.session_state.board_image.copy()
        if st.session_state.drawing_mode == "draw":
            base.alpha_composite(uploaded_pil)
        else:  # erase 모드면 투명 영역 외 삭제
            base.paste((255,255,255,255), (0,0,board_size*cell_px,board_size*cell_px), uploaded_pil)
        st.session_state.board_image = base
        st.experimental_rerun()

with col2:
    st.markdown("### 채팅")
    chat_input = st.text_input("메시지 입력")
    if st.button("전송"):
        if chat_input.strip() != "":
            st.session_state.chat_messages.append(chat_input.strip())
        st.experimental_rerun()

    for msg in reversed(st.session_state.chat_messages):
        st.write(f"- {msg}")

    st.markdown("---")
    st.markdown("### 캐릭터 관리")

    char_name = st.text_input("캐릭터 이름")
    char_img_file = st.file_uploader("캐릭터 이미지 업로드 (원형으로 표시됨)", type=["png","jpg","jpeg"])
    if st.button("캐릭터 생성/수정"):
        if char_name and char_img_file:
            img_pil = Image.open(char_img_file).convert("RGBA").resize((64,64))
            # 원형 마스크 적용
            mask = Image.new("L", img_pil.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0,0,64,64), fill=255)
            img_circle = Image.new("RGBA", img_pil.size)
            img_circle.paste(img_pil, (0,0), mask=mask)
            # 이미지 바이트로 저장
            buf = io.BytesIO()
            img_circle.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            st.session_state.characters[char_name] = img_bytes
            st.success(f"{char_name} 캐릭터가 저장되었습니다.")
        else:
            st.warning("이름과 이미지를 모두 입력해주세요.")

    if st.session_state.characters:
        st.markdown("#### 저장된 캐릭터")
        for name, img_bytes in st.session_state.characters.items():
            st.image(img_bytes, width=64, caption=name)
            if st.button(f"{name} 삭제"):
                del st.session_state.characters[name]
                st.experimental_rerun()

