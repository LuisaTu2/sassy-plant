from typing import List

from fastapi import WebSocket, WebSocketDisconnect

from domain.types import MessageType


class WebSocketManager:
    def __init__(self):
        self.clients: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.append(ws)
        print("connection to websocket successful: ", ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.clients:
            self.clients.remove(ws)

    async def broadcast(self, message_type: MessageType, payload: dict):
        disconnected = []
        message = {
            "type": message_type,
            "payload": payload,
        }
        try:
            for ws in self.clients:
                await ws.send_json(message)
        except WebSocketDisconnect:
            disconnected.append(ws)
        for ws in disconnected:
            self.disconnect(ws)
