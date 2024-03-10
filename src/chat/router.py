from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import async_session_maker, get_async_session
from src.chat.models import Message
from src.chat.schemas import MessageBase


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            async function getLastMessages() {
                const url = 'http://localhost:8000/chat/message_history/'
                const response = await fetch(url, {
                    method: "GET"
                })
                return response.json()
            }
            getLastMessages().then(messages => {
                appendMessage("Last 5 messages: ")
                messages.forEach(msg => {
                    appendMessage(msg.message)
                })
                appendMessage("New messages: ")
            })
            function appendMessage(msg) {
                let messages = document.getElementById("messages")
                let message = document.createElement("li")
                let content = document.createTextNode(msg)
                message.appendChild(content)
                messages.appendChild(message)
            }

            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/chat/ws/${client_id}`);
            ws.onmessage = function(event) {
                appendMessage(event.data)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_message_to_db(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_message_to_db(message: str):
        async with async_session_maker() as session:
            new_message = Message(message=message)
            session.add(new_message)
            await session.flush()
            await session.commit()


manager = ConnectionManager()


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.get("/message_history/", response_model=list[MessageBase])
async def get_message_history(
    session: AsyncSession = Depends(get_async_session)
):
    query = select(Message).order_by(Message.id.desc()).limit(5)
    result = await session.execute(query)
    messages = result.scalars().all()
    return messages


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
