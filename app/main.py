import asyncio
from domain.managers.websocket_manager import WebSocketManager
from domain.managers.orchestrator_manager import OrchestratorManager
from clients.llm_client import OpenAIClient
from domain.models.plant import Plant
from domain.managers.sensor_manager import (
    SensorManager,
    start_serial_reader,
)
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.http import create_plant_router
from api.websocket import create_ws_router, router as ws_router
from config import settings


plant = Plant()
llm_client = OpenAIClient()
sensor_manager = SensorManager()
websocket_manager = WebSocketManager()
orchestrator_manager = OrchestratorManager(
    plant=plant,
    sensor_manager=sensor_manager,
    llm_client=llm_client,
    websocket_manager=websocket_manager,
)


def create_app() -> FastAPI:
    app = FastAPI(title="sassy plant")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # vite default
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        create_ws_router(websocket_manager, orchestrator=orchestrator_manager)
    )
    app.include_router(create_plant_router(plant))

    return app


app = create_app()


# schedule sensor reading as a background task
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_serial_reader(sensor_manager))


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
