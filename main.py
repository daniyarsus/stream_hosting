from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

# Список активных WebSocket соединений
connections: List[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Отправляем данные всем подключенным клиентам
            for connection in connections:
                await connection.send_text(data)
    except Exception as e:
        connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
