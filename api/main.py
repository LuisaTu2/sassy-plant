import asyncio

import uvicorn
from config import settings
from fastapi import FastAPI
from openai_client import OpenAIClient

# import pyttsx3
from types_plant import PlantState
from utils import read_sensors

app = FastAPI(title="sassy plant")

# initialize open ai
llm_client = OpenAIClient()
llm_client.create_client()

text = "Hola soy tu sassy plantita 😏"

plant_state: PlantState = {"soil_moisture": 0, "light": 0, "mood": "neutral"}


@app.on_event("startup")
async def probe_and_talk():
    await asyncio.create_task(read_sensors(plant_state))
    print("final plant state: ", plant_state)
    await asyncio.create_task(
        llm_client.talk_to_me_plant(
            plant_state, "I just watered you. Are you feeling better now? "
        )
    )


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
