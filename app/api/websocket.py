import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.sensor_manager import SensorManager


router = APIRouter()

sensor_manager = SensorManager()


@router.websocket("/ws/sensors")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    sensor_manager.clients.append(ws)

    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("type") == "start_readings":
                if not sensor_manager.reading_active:
                    print("start readings")
                    asyncio.create_task(sensor_manager.start_readings())
            elif msg.get("type") == "stop_readings":
                print("stop readings")
                await sensor_manager.stop_readings()
            elif msg.get("type") == "stopped_talking":
                sensor_manager.is_talking = False
            elif msg.get("type") == "user_voice_message":
                print("message received: ", msg.get("text"))
                await sensor_manager.answer_user_voice_message(msg.get("text"))
    except WebSocketDisconnect:
        sensor_manager.clients.remove(ws)
        print("Client disconnected")
