import streamlit as st

# 툴바 고정 - Streamlit 앱 상단에 간단한 메시지 띄우기 (Streamlit 상단 영역 활용)
st.markdown(
    """
    <style>
    .toolbar {
        position: sticky;
        top: 0;
        background-color: #2196F3;
        color: white;
        padding: 10px;
        font-size: 20px;
        font-weight: bold;
        z-index: 1000;
        user-select: none;
    }
    .board {
        display: grid;
        grid-template-columns: repeat(16, 1fr);
        grid-template-rows: repeat(16, 1fr);
        gap: 2px;
        background-color: #ddd;
        border-radius: 8px;
        padding: 10px;
    }
    .tile {
        background-color: #bbb;
        border-radius: 4px;
        aspect-ratio: 1 / 1;
    }
    .chat-container {
        margin-top: 20px;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 8px;
        background-color: #eee;
    }
    .chat-messages {
        max-height: 200px;
        overflow-y: auto;
        background-color: white;
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    textarea {
        width: 100%;
        height: 60px;
        border-radius: 4px;
        border: 1px solid #ccc;
        padding: 6px;
        resize: none;
    }
    button {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
    }
    </style>
    <div class="toolbar">🛠️ 툴바 - 도구 선택</div>
    """,
    unsafe_allow_html=True,
)

# 보드 출력
board_html = '<div class="board">'
for _ in range(16 * 16):
    board_html += '<div class="tile"></div>'
board_html += '</div>'
st.markdown(board_html, unsafe_allow_html=True)

# 채팅 영역
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

chat_messages_html = '<div class="chat-messages">'
for msg in st.session_state.messages:
    chat_messages_html += f'<div>{msg}</div>'
chat_messages_html += '</div>'
st.markdown(chat_messages_html, unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    msg = st.text_area("메시지 입력", "")
    submit = st.form_submit_button("전송")
    if submit and msg.strip() != "":
        st.session_state.messages.append(msg.strip())
        st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)
