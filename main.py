from fastapi import FastAPI, WebSocket, Request, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Монтируем статическую папку
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# Список активных WebSocket соединений
connections: List[WebSocket] = []


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


#@app.get("/", response_class=HTMLResponse)
#async def read_index(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/")
def read_root():
    return FileResponse('static/index.html')


