# global manager
import asyncio
import datetime
import json
from collections import deque

from clients.utils import get_generic_prompt
from fastapi import WebSocket

# import json
# from api.websocket import plant_talks
from clients.llm_client import llm_client
from domain.sensor_readings import (
    update_light,
    update_moisture,
)
from domain.types import AudioType, MessageType, Reading, ReadingMessage
from domain.utils import get_state_changes, plant_mood_score_from_readings


class SensorManager:
    def __init__(self):
        self.clients: list[WebSocket] = []
        self.reading_active = False
        self.is_talking = False
        self.water_readings = deque()
        self.light_readings = deque()

    async def broadcast(self, message: dict):
        for ws in self.clients:
            # print("clients: ", self.clients)
            try:
                await ws.send_text(message)
            except:
                self.clients.remove(ws)

    async def start_readings(self):
        self.reading_active = True
        while self.reading_active:
            reading = await self.get_reading()
            self.record_reading(reading)
            await self.send_reading(reading)

            if len(self.water_readings) >= 5:
                await self.handle_state_changes()

            await asyncio.sleep(0.5)  # adjust frequency

    async def stop_readings(self):
        self.reading_active = False

    async def send_reading(self, reading: Reading):
        message: ReadingMessage = {
            "type": MessageType.READING.value,
            "payload": reading,
        }

        await self.broadcast(json.dumps(message))
        return

    def record_reading(self, reading: Reading):
        self.water_readings.append(reading["soil_moisture"])
        self.light_readings.append(reading["light"])

    async def get_reading(self):
        moisture_val = update_moisture()
        light_val = update_light()
        mood = plant_mood_score_from_readings(moisture_val, light_val)
        print(
            f"[{datetime.datetime.now()}] moisture={moisture_val:4d}  light={light_val:4d} lux "
        )
        reading: Reading = {
            "soil_moisture": moisture_val,
            "light": light_val,
            "mood": mood / 100,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        return reading

    async def plant_talks(self, state_change):
        self.is_talking = True
        self.water_readings.popleft()
        self.light_readings.popleft()

        text = await asyncio.to_thread(llm_client.get_sassy_answer, state_change)
        print(text)
        audio_b64 = await asyncio.to_thread(llm_client.get_audio, text)
        message = json.dumps(
            {
                "type": "voice",
                "payload": {
                    "audio": audio_b64,
                    "format": AudioType.WAV.value,
                    "text": text,
                },
            }
        )
        await self.broadcast(message)

    async def handle_state_changes(self):
        state_change = get_state_changes(self.water_readings, self.light_readings)
        print("is talking in state change? ", self.is_talking, "\n")
        if not self.is_talking and (
            state_change.has_water_state_changed or state_change.has_light_state_changed
        ):
            asyncio.create_task(self.plant_talks(state_change))

    async def answer_user_voice_message(self, user_voice_msg):
        reply = llm_client.get_voice_msg_answer(user_voice_msg)
        print("sassy reply: ", reply)
        audio_b64 = await asyncio.to_thread(llm_client.get_audio, reply)
        message = json.dumps(
            {
                "type": "voice",
                "payload": {
                    "audio": audio_b64,
                    "format": AudioType.WAV.value,
                    "text": reply,
                },
            }
        )
        await self.broadcast(message)
        return reply


sensor_manager = SensorManager()
