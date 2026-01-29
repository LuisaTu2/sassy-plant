from fastapi import FastAPI
import os
from openai_client import OpenAIClient
import uvicorn
from config import settings
import asyncio
import random

import pyttsx3


app = FastAPI(title="sassy plant")

openai = OpenAIClient()
openai.create_client()

engine = pyttsx3.init()
engine.setProperty("voice", "gmw/en-us-nyc")


plant_state = {"soil_moisture": 0, "light": 0, "mood": "neutral"}


async def read_sensors():
    while True:
        # simulation
        plant_state["soil_moisture"] = random.randint(0, 1000)
        plant_state["light"] = random.randint(0, 1000)

        # Simple mood logic based on soil
        if plant_state["soil_moisture"] < 300:
            plant_state["mood"] = "sassy 😏"
        elif plant_state["soil_moisture"] < 600:
            plant_state["mood"] = "neutral 😐"
        else:
            plant_state["mood"] = "happy 😄"

        await asyncio.sleep(0.1)  # simulate 1-second sensor interval


# --- APIs --- #
@app.get("/get-plant-mood")
async def get_plant_mood():
    return plant_state["mood"]


@app.get("/talk-to-me-plant")
async def talk(user_input: str = ""):
    if not openai:
        raise Exception("unable to initialize openai client")
    response_text = openai.get_plant_response(plant_state, user_input)
    return {"mood": plant_state["mood"], "response": response_text}


async def speak(text):
    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print(f"[PLANT SAYS]: {text}")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(speak("Hello! I am your sassy plant 😏"))
    asyncio.create_task(read_sensors())


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # auto-reload in dev
    )


# <Voice id=gmw/en-us
#           name=English (America)
#           languages=['en-us']
#           gender=Male
#           age=None> gmw/en-us
# <Voice id=gmw/en-us-nyc
#           name=English (America, New York City)
#           languages=['en-us-nyc']
#           gender=Male
#           age=None> gmw/en-us-nyc
