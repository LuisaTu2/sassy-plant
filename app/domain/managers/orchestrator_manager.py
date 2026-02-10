import asyncio
import datetime
import json
from pathlib import Path

from clients.llm_client import OpenAIClient
from clients.prompts import get_base_prompt, get_state_change_prompt
from domain.managers.sensor_manager import SensorManager
from domain.managers.websocket_manager import WebSocketManager
from domain.models.plant import MEMORY_FILE, Plant
from domain.types import (
    AudioType,
    DataPoint,
    EventType,
    LightState,
    MessageType,
    WaterState,
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

        # register callbacks from sensor manager
        self.sensor_manager.publish_data_point = self.publish_data_point

    async def start_reading(self):
        while True:
            # wait until roughly 5s interval
            await asyncio.sleep(5)
            now = datetime.datetime.now()

            avg_light: float = self.sensor_manager.get_avg_light_reading()
            avg_water: float = self.sensor_manager.get_avg_water_reading()

            # not enough readings yet
            if avg_light < 0 or avg_water < 0:
                continue

            new_light_state: LightState = self.plant.map_to_light_state(avg_light)
            new_water_state: WaterState = self.plant.map_to_water_state(avg_water)
            print(
                "readings: ",
                now,
                avg_light,
                avg_water,
                new_light_state,
                new_water_state,
            )

            # first state change is recorded
            if self.plant.light_state == None:
                self.plant.update_states(
                    new_light_state=new_light_state, new_water_state=new_water_state
                )
                continue

            # no state change
            if (
                self.plant.light_state == new_light_state
                and self.plant.water_state == new_water_state
            ):
                continue

            # a state change occurred
            print(
                self.plant.light_state,
                "-->",
                new_light_state,
                "·",
                self.plant.water_state,
                "-->",
                new_water_state,
            )

            await self.handle_state_change(
                new_light_state=new_light_state,
                new_water_state=new_water_state,
                timestamp=now,
            )

    async def handle_state_change(
        self,
        new_light_state: LightState,
        new_water_state: WaterState,
        timestamp: datetime,
    ):
        try:
            event: EventType = self.get_event_type(
                new_light_state=new_light_state, new_water_state=new_water_state
            )
            if event == EventType.WATERING.value:
                self.plant.update_last_watered(timestamp)

            if self.plant.is_talking:
                self.publish_state_change_no_audio(event_type=event)
            else:
                self.plant.is_talking = True
                text, audio = await self.get_text_and_audio(
                    light_state=self.plant.light_state,
                    water_state=self.plant.water_state,
                    new_light_state=new_light_state,
                    new_water_state=new_water_state,
                    event_type=event,
                )
                self.publish_state_change(text=text, audio=audio, event_type=event)

            # finally, update the state of the plant
            self.plant.update_states(
                new_light_state=new_light_state, new_water_state=new_water_state
            )
        except Exception as e:
            print(f"unable to update {self.plant.id}'s state: ", e)

    async def get_text_and_audio(
        self,
        light_state: LightState = None,
        new_light_state: LightState = None,
        water_state: WaterState = None,
        new_water_state: WaterState = None,
        user_input: str = None,
        event_type: EventType = None,
    ):
        try:
            prompt = ""
            if user_input is not None:
                prompt = get_base_prompt(
                    self.plant.name,
                    self.plant.type,
                    self.plant.sassiness,
                    self.plant.days_since_last_watered,
                    user_input,
                )
            else:
                prompt = get_state_change_prompt(
                    plant_name=self.plant.name,
                    plant_type=self.plant.type,
                    sass_level=self.plant.sassiness,
                    light_state=light_state,
                    new_light_state=new_light_state,
                    water_state=water_state,
                    new_water_state=new_water_state,
                    event_type=event_type,
                )

            text = await asyncio.to_thread(self.llm_client.get_text_response, prompt)
            audio_b64 = await asyncio.to_thread(
                self.llm_client.get_audio_response, text, self.plant.voice
            )
            audio_b64 = audio_b64.replace("\n", "").replace(" ", "")
            return text, audio_b64
        except Exception as e:
            print("error when making plant talk on state change:", e)

    def get_event_type(
        self,
        new_light_state: LightState,
        new_water_state: WaterState,
    ):
        # currently prioritizing light change vs water
        # and handles one state change at a time

        # change in light
        event_type: EventType = ""
        if new_light_state != self.plant.light_state:
            if new_light_state == LightState.DARK.value:
                event_type = EventType.GOOD_NIGHT.value
            elif new_light_state == LightState.BRIGHT.value:
                event_type = EventType.WEAR_SUNGLASSES.value
            else:
                if self.plant.light_state == LightState.DARK.value:
                    event_type = EventType.GOOD_MORNING.value
                else:
                    event_type = EventType.TAKE_OFF_SUNGLASSES.value
            return event_type

        # change in water levels
        if new_water_state != self.plant.water_state:
            if new_water_state == WaterState.DRY.value:
                event_type = EventType.DRYING.value
            elif new_water_state == WaterState.OVERWATERED.value:
                event_type = EventType.WATERING.value
            else:
                if self.plant.water_state == WaterState.DRY.value:
                    event_type = EventType.WATERING.value
                else:
                    event_type = EventType.DRYING.value
        return event_type

    # handle notifications
    def publish_data_point(self, data, timestamp):
        water = data["water"]
        light = data["light"]
        payload = DataPoint(
            soil_moisture=str(1 - water / 1000),
            light=str(light / 1023),
            timestamp=str(timestamp),
        )
        asyncio.create_task(
            self.websocket_manager.broadcast(
                message_type=MessageType.DATA_POINT.value, payload=payload.dict()
            )
        )

    def publish_state_change(self, text: str, audio: str, event_type: EventType):
        payload = {
            "audio": audio,
            "format": AudioType.WAV.value,
            "text": text,
            "event": event_type,
        }
        print("publishing state change: ", event_type)

        asyncio.create_task(
            self.websocket_manager.broadcast(
                message_type=MessageType.STATE_CHANGE.value, payload=payload
            )
        )

    def publish_state_change_no_audio(self, event_type: EventType):
        payload = {
            "event": event_type,
        }
        print("publishing state change, no audio: ", event_type)

        asyncio.create_task(
            self.websocket_manager.broadcast(
                message_type=MessageType.STATE_CHANGE_NO_AUDIO.value, payload=payload
            )
        )

    def publish_response_to_human(
        self,
        text: str,
        audio: str,
    ):
        try:
            payload = {
                "audio": audio,
                "format": AudioType.WAV.value,
                "text": text,
            }
            print("responding to human")

            asyncio.create_task(
                self.websocket_manager.broadcast(
                    message_type=MessageType.RESPOND_TO_HUMAN.value,
                    payload=payload,
                )
            )

        except Exception as e:
            print("unable to respond to human: ", e)

    async def handle_ws_message(self, message: dict):
        try:
            if message["type"] == "stopped_talking":
                self.plant.is_talking = False
            else:
                print("is plant talking? ", self.plant.is_talking)
                if self.plant.is_talking:
                    return
                user_input = message["text"]
                text, audio = await self.get_text_and_audio(user_input=user_input)
                self.publish_response_to_human(text=text, audio=audio)
                print("done talking to human")
        except Exception as e:
            print("unable to respond to human message: ", e)

    # async def get_and_send_text_and_audio_stream(
    #     self,
    #     user_input: str = None,
    # ):
    #     try:
    #         prompt = get_base_prompt(
    #             self.plant.name,
    #             self.plant.type,
    #             self.plant.sassiness,
    #             self.plant.days_since_last_watered,
    #             user_input,
    #         )

    #         text = await asyncio.to_thread(self.llm_client.get_text_response, prompt)

    #         print("streaming audio")
    #         audio_bytes = self.llm_client.get_audio_bytes(
    #             text=text, voice=self.plant.voice
    #         )
    #         chunk_size = 4096
    #         for i in range(0, len(audio_bytes), chunk_size):
    #             chunk = audio_bytes[i : i + chunk_size]
    #             await self.websocket_manager.broadcast_bytes(
    #                 chunk=chunk, audio_msg_type=AudioMessageType.AUDIO_CHUNK.value
    #             )
    #         # send end message
    #         await self.websocket_manager.broadcast_bytes(
    #             chunk=chunk, audio_msg_type=AudioMessageType.AUDIO_END.value
    #         )
    #         return
    #     except Exception as e:
    #         print("error when making plant talk on talking to human:", e)
