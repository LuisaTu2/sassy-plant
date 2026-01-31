import asyncio
import base64
import datetime
import json
import random

from fastapi import WebSocket

from types_plant import (
    AudioMessage,
    AudioType,
    MessageType,
    PlantMood,
    PlantState,
    ReadingMessage,
)


def get_plant_mood(plant_state):
    # Simple mood logic based on soil
    soil_moisture = plant_state["soil_moisture"]
    mood: PlantMood = PlantMood.HAPPY
    if soil_moisture < 300:
        mood = PlantMood.ANGRY
    elif 300 < soil_moisture < 600:
        mood = PlantMood.SAD
    else:
        mood = PlantMood.EXTRA_SASSY
    return mood


async def read_sensors(plant_state: PlantState):
    for _ in range(10):
        plant_state["soil_moisture"] = random.randint(0, 1000)
        plant_state["light"] = random.randint(0, 1000)
        plant_mood: PlantMood = get_plant_mood(plant_state)
        plant_state["mood"] = plant_mood
        print("plant state: ", plant_state["mood"].value)
        await asyncio.sleep(0.1)  # simulate 1-second sensor interval


def simulate_reading():
    return {
        "soil_moisture": random.randint(0, 1000),
        "timestamp": datetime.datetime.now().isoformat(),
    }


async def simulate_and_send_readings(websocket: WebSocket):
    first_reading = None
    last_reading = None
    for i in range(20):
        plant_data = simulate_reading()
        if i == 0:
            first_reading = plant_data
        if i == 19:
            last_reading = plant_data
        message: ReadingMessage = {
            "type": MessageType.READING.value,
            "payload": plant_data,
        }
        await websocket.send_text(json.dumps(message))
        await asyncio.sleep(0.1)
    return first_reading, last_reading


async def send_audio(response, ws):
    audio_bytes = response.read()  # WAV bytes
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    message: AudioMessage = {
        "type": MessageType.AUDIO.value,
        "payload": {"audio": audio_b64, "format": AudioType.WAV.value},
    }
    await ws.send_text(json.dumps(message))
