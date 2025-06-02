# TRPG Streamlit 앱

## 구성
- `streamlit_app.py`: 메인 실행 파일
- `character_creator.py`: 캐릭터 생성 페이지
- `websocket_client.py`: 실시간 채팅/이벤트용 웹소켓 클라이언트
- `config_sample.py`: 설정 예시 파일
- `requirements.txt`: 필요한 패키지 목록

## 설정 방법
1. `config_sample.py`를 `config.py`로 복사하세요.
2. 본인의 Supabase 프로젝트 및 WebSocket 서버 정보를 입력하세요.

## 실행
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```