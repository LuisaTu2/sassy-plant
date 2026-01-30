import asyncio
import json

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from openai_client import OpenAIClient

# import pyttsx3
from types_plant import PlantState
from utils import read_sensors, simulate_readings

app = FastAPI(title="sassy plant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize open ai
llm_client = OpenAIClient()
llm_client.create_client()

text = "Hola soy tu sassy plantita 😏"

plant_state: PlantState = {"soil_moisture": 0, "light": 0, "mood": "neutral"}


@app.on_event("startup")
async def probe_and_talk():
    await asyncio.create_task(read_sensors(plant_state))
    print("final plant state: ", plant_state)
    # await asyncio.create_task(
    #     llm_client.talk_to_me_plant(
    #         plant_state, "I just watered you. Are you feeling better now? "
    #     )
    # )


@app.websocket("/ws/sensors")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    print("\n\nwebSocket is connected\n\n")

    for _ in range(20):
        plant_data = simulate_readings()
        await ws.send_text(json.dumps(plant_data))
        await asyncio.sleep(0.1)


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
