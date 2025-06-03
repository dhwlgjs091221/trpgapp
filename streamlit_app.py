import streamlit as st
import streamlit_drawable_canvas as canvas

# 1. 페이지 설정은 맨 위에 무조건!
st.set_page_config(layout="wide")

# 2. CSS: 스크롤 완전 제거 + 채팅창 고정 스타일
st.markdown("""
<style>
html, body, #root > div, #root > div > div, #root > div > div > div {
    overflow: hidden !important;
    height: 100vh !important;
    margin: 0; padding: 0;
}
.fixed-chat-wrapper {
    position: fixed;
    bottom: 10px;
    right: 10px;
    width: 300px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 8px;
    z-index: 9999;
    font-size: 13px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.fixed-chat-wrapper textarea {
    width: 100%;
    height: 180px;
    resize: none;
    font-size: 12px;
    padding: 4px;
    border-radius: 4px;
}
.fixed-chat-wrapper input[type="text"] {
    width: 70%;
    font-size: 12px;
    padding: 4px;
    margin-top: 6px;
    border-radius: 4px;
    border: 1px solid #ccc;
}
.fixed-chat-wrapper button {
    width: 28%;
    font-size: 12px;
    padding: 5px 0;
    margin-left: 4%;
    border-radius: 4px;
    background-color: #0b79d0;
    color: white;
    border: none;
    cursor: pointer;
}
.fixed-chat-wrapper button:hover {
    background-color: #095a9d;
}
</style>
""", unsafe_allow_html=True)

# 3. 도구 바 (가로 배치)
tool_col1, tool_col2, _ = st.columns([1, 1, 8])
with tool_col1:
    drawing_tool = st.radio("도구", ["펜", "지우개"], horizontal=True, label_visibility="collapsed")

# 4. 캔버스 그리기 (크기 고정 안함, 800px 기본)
canvas_size = 800  # 기본 크기, 필요시 나중에 확대/축소 기능 추가 가능
stroke_color = "#000000" if drawing_tool == "펜" else "#ffffff"
stroke_width = 4

canvas_result = canvas.st_canvas(
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#ffffff",
    height=canvas_size,
    width=canvas_size,
    drawing_mode="freedraw",
    key="main_canvas"
)

# 5. 채팅 상태 관리
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 6. 채팅창 (고정 위치, HTML+JS로 구현)
chat_log = "\n".join(st.session_state.chat_history)
chat_html = f"""
<div class='fixed-chat-wrapper'>
    <b style='font-size: 13px;'>💬 채팅</b>
    <textarea readonly id='chat_log'>{chat_log}</textarea><br>
    <input type='text' id='chat_input' name='msg' placeholder='메시지 입력'>
    <button onclick="sendMessage()">전송</button>
</div>
<script>
function sendMessage() {{
    const input = window.parent.document.getElementById('chat_input');
    const value = input.value;
    if (value.trim() !== '') {{
        const streamlitInput = window.parent.document.querySelectorAll('input[data-testid="stTextInput"]')[0];
        if (streamlitInput) {{
            streamlitInput.value = value;
            const inputEvent = new Event('input', {{ bubbles: true }});
            streamlitInput.dispatchEvent(inputEvent);
            input.value = '';
        }}
    }}
}}
window.parent.document.getElementById('chat_input')?.addEventListener("keypress", function(e) {{
    if (e.key === "Enter") {{
        e.preventDefault();
        sendMessage();
    }}
}});
</script>
"""
st.markdown(chat_html, unsafe_allow_html=True)

# 7. 숨겨진 텍스트 입력으로 실제 Streamlit 상태 업데이트 + 채팅 추가
new_msg = st.text_input("숨김 채팅 입력", label_visibility="collapsed", key="hidden_chat_input")
if new_msg.strip():
    st.session_state.chat_history.append(f"나: {new_msg}")
    # send_message(new_msg)  # 웹소켓 보내는 함수가 있으면 호출

# 8. (옵션) 받는 메시지 처리 부분 구현 시 이곳에 추가

