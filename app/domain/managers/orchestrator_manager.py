import asyncio

from domain.managers.websocket_manager import WebSocketManager
from clients.llm_client import OpenAIClient
from clients.utils import get_base_prompt, get_state_change_prompt
from domain.managers.sensor_manager import SensorManager
from domain.models.plant import Plant

from domain.types import (
    AudioType,
    MessageType,
    LightState,
    MessageType,
    DataPoint,
)


class OrchestratorManager:
    def __init__(
        self,
        plant: Plant,
        sensor_manager: SensorManager,
        llm_client: OpenAIClient,
        websocket_manager: WebSocketManager,
    ):
        self.plant = plant
        self.sensor_manager = sensor_manager
        self.llm_client = llm_client
        self.websocket_manager = websocket_manager

        # register callback from sensor manager
        self.sensor_manager.publish_data_point = self.publish_data_point
        self.sensor_manager.make_plant_talk_on_state_change = (
            self.make_plant_talk_on_state_change
        )

    def publish_data_point(self, data, timestamp):
        print("data and timestamp: ", data, timestamp)

        payload = DataPoint(
            soil_moisture=str(data["water"]),
            light=str(data["light"]),
            timestamp=str(timestamp),
        )
        asyncio.create_task(
            self.websocket_manager.broadcast(
                message_type=MessageType.DATA_POINT.value, payload=payload.dict()
            )
        )

    def publish_text_and_audio(self, text: str, audio: str):
        payload = {
            "audio": audio,
            "format": AudioType.WAV.value,
            "text": text,
        }

        asyncio.create_task(
            self.websocket_manager.broadcast(
                message_type=MessageType.TEXT_AND_AUDIO.value, payload=payload
            )
        )

    async def make_plant_talk_on_state_change(
        self, light_state: LightState, new_light_state: LightState
    ):
        try:
            prompt = get_state_change_prompt(
                self.plant.name, self.plant.type, light_state, new_light_state
            )
            text = await asyncio.to_thread(self.llm_client.get_text_response, prompt)
            audio_b64 = await asyncio.to_thread(
                self.llm_client.get_audio_response, text, self.plant.voice
            )
            audio_b64 = audio_b64.replace("\n", "").replace(" ", "")
            self.publish_text_and_audio(text, audio=audio_b64)
        except Exception as e:
            print("error when making plant talk on state change:", e)

    async def make_plant_respond_to_user_input(self, user_input):
        try:
            prompt = get_base_prompt(self.plant.name, self.plant.type, user_input)
            text = await asyncio.to_thread(self.llm_client.get_text_response, prompt)
            audio_b64 = await asyncio.to_thread(
                self.llm_client.get_audio_response, text, self.plant.voice
            )
            audio_b64 = audio_b64.replace("\n", "").replace(" ", "")
            self.publish_text_and_audio(text, audio=audio_b64)
        except Exception as e:
            print("error when making plant talk after user input:", e)

    def handle_ws_message(self, message: dict):
        try:
            if message["type"] == "stopped_talking":
                self.plant.is_talking = False
            else:
                user_input = message["text"]
                asyncio.create_task(self.make_plant_respond_to_user_input(user_input))
        except Exception as e:
            print("unable to process message from websocket: ", e)
