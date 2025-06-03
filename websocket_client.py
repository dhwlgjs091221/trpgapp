import asyncio
import threading
import queue
import websockets

_ws = None
_receive_queue = queue.Queue()

def start_websocket(url):
    """웹소켓 연결 시작, 별도 스레드에서 실행"""
    def run():
        asyncio.run(_websocket_loop(url))
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

async def _websocket_loop(url):
    global _ws
    async with websockets.connect(url) as websocket:
        _ws = websocket
        while True:
            msg = await websocket.recv()
            _receive_queue.put(msg)

def send_message(message):
    """웹소켓에 메시지 전송 (비동기지만 동기처럼 호출 가능하도록 단순 래핑)"""
    if _ws is None:
        print("웹소켓 연결이 아직 설정되지 않았습니다.")
        return
    asyncio.create_task(_ws.send(message))

def get_received_messages():
    """수신된 메시지를 큐에서 꺼내 리스트로 반환"""
    msgs = []
    while not _receive_queue.empty():
        msgs.append(_receive_queue.get())
    return msgs
