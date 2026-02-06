import asyncio

from domain.managers.sensor_manager import sensor_manager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter()


@router.websocket("/ws/sensors")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    sensor_manager.clients.append(ws)

    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("type") == "stopped_talking":
                sensor_manager.is_talking = False
            elif msg.get("type") == "user_voice_message":
                print("message received: ", msg.get("text"))
                await sensor_manager.answer_user_voice_message(msg.get("text"))
    except WebSocketDisconnect:
        sensor_manager.clients.remove(ws)
        print("Client disconnected")
