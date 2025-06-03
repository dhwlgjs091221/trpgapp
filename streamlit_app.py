import streamlit as st

# 스크롤 없애는 CSS
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

st.title("보드와 채팅창 예제 (스크롤 없음)")

# 레이아웃: 좌측 보드, 우측 채팅창
container_css = """
<style>
.flex-container {
    display: flex;
    height: 90vh;
    width: 100%;
    gap: 10px;
}
.board {
    flex: 3;
    background-color: #ddd;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 24px;
    border-radius: 8px;
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

st.markdown(container_css, unsafe_allow_html=True)

# 채팅 메시지 저장용
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI 출력
st.markdown('<div class="flex-container">', unsafe_allow_html=True)

# 보드 영역
st.markdown('<div class="board">보드 영역</div>', unsafe_allow_html=True)

# 채팅창 영역
st.markdown('<div class="chat">', unsafe_allow_html=True)

# 메시지 출력 영역
chat_messages_html = "<div class='chat-messages'>"
for msg in st.session_state.messages:
    chat_messages_html += f"<div>{msg}</div>"
chat_messages_html += "</div>"

st.markdown(chat_messages_html, unsafe_allow_html=True)

# 채팅 입력창
with st.form(key="chat_form", clear_on_submit=True):
    msg = st.text_area("메시지 입력", height=60)
    submit = st.form_submit_button("전송")
    if submit and msg.strip() != "":
        st.session_state.messages.append(msg.strip())
        st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)  # chat 닫기
st.markdown('</div>', unsafe_allow_html=True)  # flex-container 닫기
