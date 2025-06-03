import React, { useState, useRef, useEffect } from "react";

// 16x16 격자 보드 크기 상수
const GRID_SIZE = 16;
const CELL_SIZE = 30; // px

// 툴바에서 사용할 툴 종류
const TOOLS = {
  DRAW: "DRAW",
  ERASE: "ERASE",
  CHAR_MANAGE: "CHAR_MANAGE",
  GAME: "GAME",
};

// 기본 캐릭터 데이터 예시
const defaultCharacters = [];

export default function GameApp() {
  // 현재 선택된 툴
  const [selectedTool, setSelectedTool] = useState(TOOLS.DRAW);
  // 그림 그리기 위한 canvas ref
  const canvasRef = useRef(null);
  // 그림 그리기 상태 (마우스 다운 여부)
  const [isDrawing, setIsDrawing] = useState(false);

  // 채팅 메시지 리스트
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");

  // 캐릭터 관리
  const [characters, setCharacters] = useState(defaultCharacters);
  const [charNameInput, setCharNameInput] = useState("");
  const [charImgInput, setCharImgInput] = useState(null);
  const [charManageVisible, setCharManageVisible] = useState(false);

  // 게임 모드 상태
  const [gameMode, setGameMode] = useState(false);

  // canvas 초기 세팅 (격자 무늬)
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // 캔버스 크기 세팅
    canvas.width = GRID_SIZE * CELL_SIZE;
    canvas.height = GRID_SIZE * CELL_SIZE;

    // 흰 배경 칠하기
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 격자 그리기
    ctx.strokeStyle = "#ccc";
    for (let i = 0; i <= GRID_SIZE; i++) {
      // 수평선
      ctx.beginPath();
      ctx.moveTo(0, i * CELL_SIZE);
      ctx.lineTo(canvas.width, i * CELL_SIZE);
      ctx.stroke();
      // 수직선
      ctx.beginPath();
      ctx.moveTo(i * CELL_SIZE, 0);
      ctx.lineTo(i * CELL_SIZE, canvas.height);
      ctx.stroke();
    }
  }, []);

  // 그림 그리기 / 지우기 함수
  const handleDraw = (e) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // 마우스 위치 계산 (캔버스 좌표)
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // 격자 셀 좌표로 변환
    const cellX = Math.floor(x / CELL_SIZE);
    const cellY = Math.floor(y / CELL_SIZE);

    // 셀의 좌측 상단 좌표
    const drawX = cellX * CELL_SIZE;
    const drawY = cellY * CELL_SIZE;

    if (selectedTool === TOOLS.DRAW) {
      ctx.fillStyle = "black";
      ctx.fillRect(drawX + 1, drawY + 1, CELL_SIZE - 2, CELL_SIZE - 2);
    } else if (selectedTool === TOOLS.ERASE) {
      ctx.fillStyle = "white";
      ctx.fillRect(drawX + 1, drawY + 1, CELL_SIZE - 2, CELL_SIZE - 2);

      // 다시 격자선 그리기 (erase로 선 사라지는 문제 방지)
      ctx.strokeStyle = "#ccc";
      ctx.strokeRect(drawX, drawY, CELL_SIZE, CELL_SIZE);
    }
  };

  // 채팅 메시지 전송
  const sendChat = () => {
    if (chatInput.trim() === "") return;
    setChatMessages((msgs) => [...msgs, chatInput.trim()]);
    setChatInput("");
  };

  // 캐릭터 이미지 업로드 핸들러
  const handleCharImgChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (ev) => setCharImgInput(ev.target.result);
      reader.readAsDataURL(file);
    }
  };

  // 캐릭터 생성
  const createCharacter = () => {
    if (!charNameInput || !charImgInput) {
      alert("이름과 이미지를 모두 입력하세요.");
      return;
    }
    setCharacters((chars) => [
      ...chars,
      { id: Date.now(), name: charNameInput, img: charImgInput },
    ]);
    setCharNameInput("");
    setCharImgInput(null);
  };

  // 캐릭터 삭제
  const deleteCharacter = (id) => {
    setCharacters((chars) => chars.filter((c) => c.id !== id));
  };

  // 게임 모드로 전환 함수
  const enterGameMode = () => {
    setGameMode(true);
    setCharManageVisible(false);
  };

  // 게임 모드에서 캐릭터 불러오기(여기선 그냥 표시)
  // 원형 이미지 스타일은 CSS로 처리
  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* 좌측 보드 + 그림 그리기 캔버스 */}
      <div
        style={{
          position: "relative",
          width: GRID_SIZE * CELL_SIZE,
          height: GRID_SIZE * CELL_SIZE,
          userSelect: "none",
        }}
      >
        <canvas
          ref={canvasRef}
          style={{ border: "1px solid #000", cursor: "crosshair" }}
          onMouseDown={() => setIsDrawing(true)}
          onMouseUp={() => setIsDrawing(false)}
          onMouseLeave={() => setIsDrawing(false)}
          onMouseMove={handleDraw}
        />
      </div>

      {/* 우측 영역 */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: 10,
          background: "#f0f0f0",
        }}
      >
        {/* 툴바 */}
        <div
          style={{
            position: "sticky",
            top: 0,
            backgroundColor: "#2196F3",
            color: "white",
            padding: "10px",
            fontWeight: "bold",
            fontSize: "18px",
            display: "flex",
            gap: 10,
            zIndex: 10,
          }}
        >
          <button
            onClick={() => setSelectedTool(TOOLS.DRAW)}
            style={{
              background: selectedTool === TOOLS.DRAW ? "#1565C0" : "transparent",
              color: "white",
              border: "none",
              padding: "6px 10px",
              cursor: "pointer",
            }}
          >
            그리기
          </button>
          <button
            onClick={() => setSelectedTool(TOOLS.ERASE)}
            style={{
              background: selectedTool === TOOLS.ERASE ? "#1565C0" : "transparent",
              color: "white",
              border: "none",
              padding: "6px 10px",
              cursor: "pointer",
            }}
          >
            지우기
          </button>
          <button
            onClick={() => {
              setSelectedTool(TOOLS.CHAR_MANAGE);
              setCharManageVisible(true);
            }}
            style={{
              background:
                selectedTool === TOOLS.CHAR_MANAGE ? "#1565C0" : "transparent",
              color: "white",
              border: "none",
              padding: "6px 10px",
              cursor: "pointer",
            }}
          >
            캐릭터 관리
          </button>
          <button
            onClick={enterGameMode}
            style={{
              background: selectedTool === TOOLS.GAME ? "#1565C0" : "transparent",
              color: "white",
              border: "none",
              padding: "6px 10px",
              cursor: "pointer",
              marginLeft: "auto",
            }}
          >
            게임 화면으로
          </button>
        </div>

        {/* 캐릭터 관리 영역 */}
        {charManageVisible && !gameMode && (
          <div
            style={{
              backgroundColor: "white",
              padding: 10,
              borderRadius: 6,
              marginTop: 10,
              maxHeight: "40vh",
              overflowY: "auto",
            }}
          >
            <h3>캐릭터 생성</h3>
            <input
              placeholder="캐릭터 이름"
              value={charNameInput}
              onChange={(e) => setCharNameInput(e.target.value)}
              style={{ width: "100%", marginBottom: 8, padding: 6 }}
            />
            <input type="file" accept="image/*" onChange={handleCharImgChange} />
            {charImgInput && (
              <img
                src={charImgInput}
                alt="preview"
                style={{ width: 80, height: 80, objectFit: "cover", marginTop: 8 }}
              />
            )}
            <button
              onClick={createCharacter}
              style={{
                marginTop: 10,
                padding: "6px 10px",
                cursor: "pointer",
                width: "100%",
              }}
            >
              생성
            </button>

            <h3 style={{ marginTop: 20 }}>캐릭터 목록</h3>
            <div>
              {characters.length === 0 && <p>생성된 캐릭터가 없습니다.</p>}
              {characters.map((char) => (
                <div
                  key={char.id}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    marginBottom: 8,
                    background: "#e0e0e0",
                    padding: 6,
                    borderRadius: 4,
                  }}
                >
                  <img
                    src={char.img}
                    alt={char.name}
                    style={{
                      width: 40,
                      height: 40,
                      borderRadius: "50%",
                      objectFit: "cover",
                      marginRight: 8,
                    }}
                  />
                  <span style={{ flex: 1 }}>{char.name}</span>
                  <button
                    onClick={() => deleteCharacter(char.id)}
                    style={{
                      background: "red",
                      color: "white",
                      border: "none",
                      padding: "4px 8px",
                      cursor: "pointer",
                      borderRadius: 4,
                    }}
                  >
                    삭제
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 게임 모드 화면 */}
        {gameMode && (
          <div
            style={{
              backgroundColor: "white",
              padding: 10,
              borderRadius: 6,
              marginTop: 10,
              flex: 1,
              overflowY: "auto",
            }}
          >
            <h2>게임 화면</h2>
            <button
              onClick={() => setGameMode(false)}
              style={{ marginBottom: 10, cursor: "pointer" }}
            >
              게임 종료
            </button>
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: 10,
              }}
            >
              {characters.length === 0 && <p>불러올 캐릭터가 없습니다.</p>}
              {characters.map((char) => (
                <div
                  key={char.id}
                  style={{
                    width: 80,
                    height: 80,
                    borderRadius: "50%",
                    overflow: "hidden",
                    border: "2px solid #2196F3",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    cursor: "pointer",
                  }}
                  title={char.name}
                >
                  <img
                    src={char.img}
                    alt={char.name}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      borderRadius: "50%",
                    }}
                  />
                  <small>{char.name}</small>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 채팅 영역 */}
        <div
          style={{
            marginTop: 10,
            background: "white",
            borderRadius: 6,
            padding: 10,
            maxHeight: "30vh",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              border: "1px solid #ddd",
              padding: 6,
              marginBottom: 6,
              background: "#fafafa",
            }}
          >
            {chatMessages.length === 0 && <p>채팅 메시지가 없습니다.</p>}
            {chatMessages.map((msg, idx) => (
              <div key={idx} style={{ marginBottom: 4 }}>
                {msg}
              </div>
            ))}
          </div>
          <div style={{ display: "flex" }}>
            <input
              style={{ flex: 1, padding: 6 }}
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") sendChat();
              }}
              placeholder="채팅 입력 후 Enter"
              disabled={gameMode} // 게임 모드에선 채팅 비활성화(원하면 변경 가능)
            />
            <button
              onClick={sendChat}
              style={{
                marginLeft: 6,
                padding: "6px 12px",
                cursor: "pointer",
                backgroundColor: "#2196F3",
                color: "white",
                border: "none",
                borderRadius: 4,
              }}
              disabled={gameMode}
            >
              전송
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
