import streamlit as st

# --- CSS: 스크롤 없애고, 툴바 고정, 레이아웃 잡기 ---
st.markdown(
    """
    <style>
    /* 화면 전체 스크롤 제거 */
    html, body, #root, #root > div, #root > div > div, #root > div > div > div {
        margin: 0; padding: 0; overflow: hidden; height: 100vh; width: 100vw;
    }

    /* 툴바 고정 및 스타일 */
    .toolbar {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 50px;
        background: rgba(33, 150, 243, 0.95);
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        padding: 0 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        z-index: 9999;
        user-select: none;
    }

    /* 툴바 높이만큼 공간 확보 */
    .main-container {
        display: flex;
        height: calc(100vh - 50px);
        width: 100vw;
        padding-top: 50px;
        gap: 10px;
        box-sizing: border-box;
    }

    /* 보드 영역 */
    .board {
        flex-grow: 3;
        background-color: #ddd;
        display: grid;
        grid-template-columns: repeat(16, 1fr);
        grid-template-rows: repeat(16, 1fr);
        gap: 2px;
        border-radius: 8px;
        padding: 10px;
        overflow: hidden;
    }
    .tile {
        background-color: #bbb;
        border-radius: 3px;
        aspect-ratio: 1 / 1;
    }

    /* 채팅 영역 */
    .chat {
        flex-grow: 1;
        background-color: #eee;
        display: flex;
        flex-direction: column;
        border-radius: 8px;
        padding: 10px;
        overflow: hidden;
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
    textarea {
        flex-grow: 1;
        resize: none;
        border-radius: 4px;
        border: 1px solid #ccc;
        padding: 6px;
    }
    button {
        margin-left: 8px;
        padding: 6px 12px;
        border-radius: 4px;
        border: none;
        background-color: #2196F3;
        color: white;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 툴바 표시 ---
st.markdown('<div class="toolbar">🛠️ 툴바 - 여기서 도구를 추가하세요</div>', unsafe_allow_html=True)

# --- 메시지 세션 초기화 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 메인 컨테이너 시작 ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# 보드 생성
board_html = '<div class="board">'
for _ in range(16 * 16):
    board_html += '<div class="tile"></div>'
board_html += '</div>'
st.markdown(board_html, unsafe_allow_html=True)

# 채팅 영역 시작
st.markdown('<div class="chat">', unsafe_allow_html=True)

# 채팅 메시지 출력
chat_messages_html = '<div class="chat-messages">'
for msg in st.session_state.messages:
    chat_messages_html += f'<div>{msg}</div>'
chat_messages_html += '</div>'
st.markdown(chat_messages_html, unsafe_allow_html=True)

# 채팅 입력 폼
with st.form(key="chat_form", clear_on_submit=True):
    msg = st.text_area("", height=60, placeholder="메시지를 입력하세요")
    submit = st.form_submit_button("전송")
    if submit and msg.strip() != "":
        st.session_state.messages.append(msg.strip())
        st.experimental_rerun()

# 채팅 영역 닫기
st.markdown('</div>', unsafe_allow_html=True)

# 메인 컨테이너 닫기
st.markdown('</div>', unsafe_allow_html=True)
