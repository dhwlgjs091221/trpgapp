import streamlit as st

# 스크롤 막는 CSS
hide_scroll_css = """
<style>
html, body, #root, #root > div, #root > div > div, #root > div > div > div {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    height: 100vh !important;
    width: 100vw !important;
}
</style>
"""

st.markdown(hide_scroll_css, unsafe_allow_html=True)

st.title("스크롤 없는 Streamlit 보드 예제")

# 여기에 보드 구현 (가변 크기)
# 예: 그냥 div로 보드 박스 표시 (임시)
board_html = """
<div style="
    width: 100%;
    height: 80vh;  /* 화면 높이의 80% 차지 */
    background-color: #ddd;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 24px;
">
    보드 영역 (스크롤 없음)
</div>
"""

st.markdown(board_html, unsafe_allow_html=True)

# 아래에 다른 UI 요소 자유롭게 추가 가능
st.write("아래에 다른 UI가 있어도 스크롤 안 생김")
