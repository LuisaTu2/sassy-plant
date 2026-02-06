import base64
from abc import ABC, abstractmethod

import numpy as np
import sounddevice as sd
from openai import OpenAI

from clients.constants import MODEL_GPT, MODEL_GPT_MINI_TTS, OPENAI_API_KEY
from clients.utils import (
    get_reading_based_prompt,
    get_generic_prompt,
    get_state_change_prompt,
)
from domain.types import (
    AudioType,
    LightState,
    PlantMood,
    PlantReading,
    PlantType,
    StateChange,
    Voice,
    current_plant_settings,
)


class LLMClient(ABC):
    """Generic LLM client interface for provider-agnostic usage"""

    def __init__(self, api_key=None):
        self.api_key = api_key

    @abstractmethod
    def create_client(self):
        pass


class OpenAIClient(LLMClient):

    def __init__(self):
        self.client = None
        self.gpt_model: str = MODEL_GPT
        self.tts_model: str = MODEL_GPT_MINI_TTS

        self.plant_name: str = ""
        self.plant_type: PlantType = PlantType.POTHOS.value
        self.voice: Voice = Voice.ECHO.value
        self.temperature: float = 0.8
        self.audio_output_type: AudioType = AudioType.WAV.value
        self.speed: float = 1

    def create_client(self):
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            raise Exception("Could not initialize OpenAI client: ", e)
        print("OpenAI client initialized")
        return self.client

    def get_voice_msg_answer(self, user_voice_msg):
        if not self.client:
            raise Exception("unable to initialize openai client")
        try:
            prompt = get_generic_prompt(
                self.plant_name, self.plant_type, user_voice_msg
            )
            print("prompt:", prompt)
            res = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                # max_tokens=50,
            )
            text = res.choices[0].message.content.strip()
        except Exception as e:
            raise Exception("unable to get sassy answer: ", e)
        return text

    def get_llm_answer(
        self,
        light_state: LightState,
        new_light_state: LightState,
        user_input=None,
    ):
        if not self.client:
            raise Exception("unable to initialize openai client")
        try:
            prompt = get_state_change_prompt(
                plant_name=current_plant_settings["name"],
                plant_type=current_plant_settings["plant_type"],
                light_state=light_state,
                new_light_state=new_light_state,
            )

            print("prompt:", prompt)
            res = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                # max_tokens=50,
            )
            text = res.choices[0].message.content.strip()
        except Exception as e:
            raise Exception("unable to get sassy answer: ", e)
        return text

    def get_sassy_answer(
        self,
        state_change: StateChange,
        user_input=None,
        m1=0,
        m2=0,
        l1=0,
        l2=0,
    ):
        if not self.client:
            raise Exception("unable to initialize openai client")
        try:
            prompt = get_reading_based_prompt(
                plant_name=current_plant_settings["name"],
                plant_type=current_plant_settings["plant_type"],
                state_change=state_change,
                # water_state_1=state_change.water_state_1,
                # water_state_2=state_change.water_state_2,
                # light_state_1=state_change.light_state_1,
                # light_state_2=state_change.light_state_2,
                # has_water_state_changed=state_change.has_water_state_changed,
                # has_light_state_changed=state_change.has_light_state_changed,
                # user_input,
            )
            print("prompt:", prompt)
            res = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                # max_tokens=50,
            )
            text = res.choices[0].message.content.strip()
        except Exception as e:
            raise Exception("unable to get sassy answer: ", e)
        return text

    def get_audio(
        self,
        text,
    ):
        if not self.client:
            raise Exception("unable to initialize openai client")
        try:
            response = self.client.audio.speech.create(
                model=self.tts_model,
                voice=self.voice,
                input=text,
                response_format=self.audio_output_type,
                speed=self.speed,
            )
            audio_bytes = response.read()  # WAV bytes
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            return audio_b64
        except Exception as e:
            raise Exception("plant is unable to chat right now: ", e)
