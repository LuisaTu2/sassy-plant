import asyncio
import base64
import datetime
import json
import random

from fastapi import WebSocket

from domain.types import (
    AudioMessage,
    AudioType,
    MessageType,
    PlantMood,
    PlantReading,
    ReadingMessage,
    Sassiness,
)


def get_plant_mood(plant_reading: PlantReading):
    # Simple mood logic based on soil
    soil_moisture = plant_reading["soil_moisture"]
    mood: PlantMood = PlantMood.HAPPY
    if soil_moisture < 300:
        mood = PlantMood.ANGRY
    elif 300 < soil_moisture < 600:
        mood = PlantMood.SAD
    else:
        mood = PlantMood.EXTRA_SASSY
    return mood


async def simulate_and_send_readings(websocket: WebSocket):
    first_reading = None
    last_reading = None
    for i in range(20):
        plant_data = {
            "soil_moisture": random.randint(0, 1000),
            "timestamp": datetime.datetime.now().isoformat(),
        }
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


def temperature_sassiness_mapping(sassiness: Sassiness):
    match sassiness:
        case Sassiness.LOW.value:
            return 0.2
        case Sassiness.MILD.value:
            return 0.4
        case Sassiness.MEDIUM.value:
            return 0.5
        case Sassiness.HIGH.value:
            return 0.7
        case Sassiness.EXTRA.value:
            return 1.5
    pass
