from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from domain.managers.orchestrator_manager import OrchestratorManager
from domain.managers.websocket_manager import WebSocketManager

router = APIRouter()


def create_ws_router(ws_manager: WebSocketManager, orchestrator: OrchestratorManager):
    router = APIRouter()

    @router.websocket("/ws/sensors")
    async def websocket_endpoint(ws: WebSocket):
        await ws_manager.connect(ws)
        try:
            while True:
                msg = await ws.receive_json()
                print("\n\nreceived message from user: ", msg, "\n\n")
                await orchestrator.handle_ws_message(msg)
        except WebSocketDisconnect:
            ws_manager.disconnect(ws)
            print("websocket disconnected")

    return router
