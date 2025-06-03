import streamlit as st

# --- 스크롤 막는 CSS 유지 + 툴바 고정 CSS 추가 ---
hide_scroll_css = """
<style>
html, body, #root, #root > div, #root > div > div, #root > div > div > div {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    height: 100vh !important;
    width: 100vw !important;
}
.toolbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 50px;
    background: rgba(33, 150, 243, 0.9);
    color: white;
    display: flex;
    align-items: center;
    padding: 0 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    z-index: 9999;
    font-weight: 600;
    font-size: 1.1rem;
    user-select: none;
}
.flex-container {
    display: flex;
    height: calc(100vh - 50px); /* 툴바 높이만큼 빼줌 */
    width: 100%;
    gap: 10px;
    padding-top: 50px; /* 툴바 공간 확보 */
}
.board {
    flex: 3;
    background-color: #ddd;
    display: grid;
    grid-template-columns: repeat(16, 1fr);
    grid-template-rows: repeat(16, 1fr);
    gap: 2px;
    border-radius: 8px;
}
.tile {
    background-color: #bbb;
    border-radius: 3px;
    aspect-ratio: 1 / 1;
}
.chat {
    flex: 1;
    background-color: #eee;
    display: flex;
    flex-direction: column;
    border-radius: 8px;
    padding: 8px;
    overflow-y: auto;
}
.chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 8px;
    background: white;
    border-radius: 4px;
    margin-bottom: 8px;
}
.chat-input {
    display: flex;
}
.chat-input textarea {
    flex-grow: 1;
    resize: none;
    border-radius: 4px;
    border: 1px solid #ccc;
    padding: 6px;
}
.chat-input button {
    margin-left: 8px;
    padding: 6px 12px;
    border-radius: 4px;
    border: none;
    background-color: #2196F3;
    color: white;
    cursor: pointer;
}
</style>
"""

st.markdown(hide_scroll_css, unsafe_allow_html=True)

# --- 툴바 HTML ---
toolbar_html = """
<div class="toolbar">
    🛠️ 툴바 - 여기에 원하는 도구 아이콘 및 버튼 넣기
</div>
"""
st.markdown(toolbar_html, unsafe_allow_html=True)

# 채팅 메시지 저장용
if "messages" not in st.session_state:
    st.session_state.messages = []

# 메인 컨테이너 시작
st.markdown('<div class="flex-container">', unsafe_allow_html=True)

# 보드 영역
board_html = '<div class="board">'
for _ in range(16*16):
    board_html += '<div class="tile"></div>'
board_html += '</div>'
st.markdown(board_html, unsafe_allow_html=True)

# 채팅창 영역
st.markdown('<div class="chat">', unsafe_allow_html=True)

chat_messages_html = "<div class='chat-messages'>"
for msg in st.session_state.messages:
    chat_messages_html += f"<div>{msg}</div>"
chat_messages_html += "</div>"

st.markdown(chat_messages_html, unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    msg = st.text_area("메시지 입력", height=60)
    submit = st.form_submit_button("전송")
    if submit and msg.strip() != "":
        st.session_state.messages.append(msg.strip())
        st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)  # chat 닫기
st.markdown('</div>', unsafe_allow_html=True)  # flex-container 닫기
