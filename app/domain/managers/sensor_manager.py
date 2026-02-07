# global manager
import asyncio
import serial_asyncio
import datetime
import json
from collections import deque

from fastapi import WebSocket

from clients.llm_client import llm_client
from domain.sensor_readings import (
    update_light,
    update_moisture,
)
from domain.types import AudioType, LightState, MessageType, Reading, ReadingMessage
from domain.utils import (
    get_state_changes,
    plant_mood_score_from_readings,
    sensor_port,
    sensor_baudrate,
)
import datetime


class SensorManager(asyncio.Protocol):
    def __init__(self):
        self.clients: list[WebSocket] = []
        self.reading_active = False
        self.is_talking = False
        self.water_readings = deque()
        self.light_readings = deque()
        self.light_states = deque()
        self.average_light_value: float
        self.current_light_state: LightState | None = None
        self.buffer = b""

    async def send_reading(self, reading: Reading):
        message: ReadingMessage = {
            "type": MessageType.READING.value,
            "payload": reading.dict(),
        }

        for ws in self.clients:
            try:
                await ws.send_text(json.dumps(message))
            except:
                self.clients.remove(ws)
        return

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

    async def plant_talks(self, light_state: LightState, new_light_state: LightState):
        self.is_talking = True
        try:
            text = await asyncio.to_thread(
                llm_client.get_llm_answer, light_state, new_light_state
            )
            print("\n\n\n\n\n\nTEXT: ", text, "\n\n\n\n")
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

            for ws in self.clients:
                await ws.send_text(message)

        finally:
            self.is_talking = False

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
        # await self.broadcast(message)

        for ws in self.clients:
            await ws.send_text(message)
        return reply

    def connection_made(self, transport):
        self.transport = transport
        print("successfully connected to sensor\n")

    # automatically runs when serial data is received
    def data_received(self, data):
        # line = data.decode().strip()
        self.buffer += data

        # check if there’s a full line (ending with \n)
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            line_str = line.decode().strip()
            if line_str:
                try:
                    import json

                    data = json.loads(line_str)
                    water = data["water"]
                    light = data["light"]
                    timestamp = datetime.datetime.now()
                    reading = Reading(
                        soil_moisture=str(water),
                        light=str(light),
                        timestamp=str(timestamp),
                        mood="",
                    )
                    print("reading:", reading)

                    # send the message to frontend
                    asyncio.create_task(self.send_reading(reading))

                    self.water_readings.append(int(water))
                    self.light_readings.append(int(light))
                    if len(self.water_readings) >= 6:
                        self.water_readings.popleft()
                        self.light_readings.popleft()
                    if timestamp.second % 5 == 0:
                        # print("CURRENT STATE: ", self.current_light_state)
                        new_state = self.get_updated_state()
                        if self.current_light_state is None:
                            self.current_light_state = new_state
                            continue
                        if new_state != self.current_light_state:
                            asyncio.create_task(
                                self.plant_talks(
                                    light_state=self.current_light_state,
                                    new_light_state=new_state,
                                )
                            )
                            self.current_light_state = new_state

                except json.JSONDecodeError:
                    print("malformed JSON, skipping:", line_str)

    def get_updated_state(
        self,
    ):
        average_light_value = sum(self.light_readings) / len(self.light_readings)
        print("Average light value: ", average_light_value)
        return self.light_to_state_mapping(average_light_value)

    def light_to_state_mapping(self, light_value):
        match light_value:
            case light_value if light_value < 200:
                return LightState.DARK.value
            case light_value if 200 <= light_value < 700:
                return LightState.SOFT.value
            case light_value if light_value >= 700:
                return LightState.BRIGHT.value


sensor_manager = SensorManager()


# lambda is used to specify instance of sensor manager as instantiated in here
async def start_serial_reader():
    loop = asyncio.get_running_loop()
    await serial_asyncio.create_serial_connection(
        loop, lambda: sensor_manager, sensor_port, sensor_baudrate
    )
