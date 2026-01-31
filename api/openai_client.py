import base64

import numpy as np
import sounddevice as sd
from openai import OpenAI

from constants import MODEL_GPT, MODEL_GPT_MINI_TTS, OPENAI_API_KEY
from llm_client import LLMClient
from types_plant import AudioType, PlantMood, PlantState, Voice


class OpenAIClient(LLMClient):

    def __init__(self):
        self.client = None
        self.gpt_model: str = MODEL_GPT
        self.tts_model: str = MODEL_GPT_MINI_TTS

        self.plant_state: PlantState = None

        self.voice: Voice = Voice.ECHO.value
        self.audio_output_type: AudioType = AudioType.WAV.value
        self.speed: int = 1.2

    def create_client(self):
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            raise Exception("Could not initialize OpenAI client: ", e)
        print("OpenAI client initialized")
        return self.client

    def get_prompt(self, plant_state: PlantState, user_input=None):
        """
        plant_state: dict containing soil, light, mood
        user_input: optional string if human says something
        """
        mood = plant_state["mood"]
        soil = plant_state["soil_moisture"]
        light = plant_state["light"]

        """ Rules:
            - If soil is low, be grumpy/sassy.
            - If soil is medium, be neutral.
            - If soil is high, be happy/playful.
            - Include references to light if relevant."""

        prompt = f"""
            You are a virtual plant with a sassy personality.
            Current mood: {mood}
            Soil moisture: {soil}
            Light level: {light}
            - Keep responses short and witty.
            Human says: "{user_input}"  # can be empty
            Must finish sentences.
            Plant responds in-character.
            """
        return prompt

    def get_sassy_answer(
        self, plant_state: PlantState, user_input=None, temperature=0.8
    ):
        if not self.client:
            raise Exception("unable to initialize openai client")
        try:
            prompt = self.get_prompt(plant_state, user_input)
            res = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                # max_tokens=50,
            )
            text = res.choices[0].message.content.strip()
        except Exception as e:
            raise Exception("unable to get sassy answer: ", e)
        return text

    def get_audiob64(self, text):
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
        except Exception as e:
            raise Exception("unable to convert text to audio: ", e)
        return audio_b64

    async def get_audio(
        self,
        plant_state,
        user_input=None,
    ):
        if not self.client:
            raise Exception("unable to initialize openai client")
        try:
            text = self.get_sassy_answer(
                plant_state,
                user_input,
            )
            print("text: ", text)
            return self.get_audiob64(text)
        except Exception as e:
            raise Exception("plant is unable to chat right now: ", e)

    # PLANT talks in BE directly
    # async def talk_to_me_plant(self, plant_state: PlantState, user_input=None):
    #     prompt = self.get_prompt(plant_state, user_input)
    #     if not self.client:
    #         raise Exception("unable to initialize openai client")
    #     try:
    #         vibe = self.client.chat.completions.create(
    #             model=self.gpt_model,
    #             messages=[{"role": "user", "content": prompt}],
    #             # max_tokens=50,
    #             temperature=0.8,  # more creative/witty
    #         )
    #         print("vibe: ", vibe)
    #         vibe = vibe.choices[0].message.content.strip()

    #         response = self.client.audio.speech.create(
    #             model=self.tts_model,
    #             voice=self.voice.value,
    #             input=vibe,
    #             response_format=self.audio_output_type.value,
    #             speed=self.speed,
    #         )
    #         print("response: ", "")
    #         # Convert to playable format
    #         audio_bytes = response.read()  # bytes of WAV
    #         audio_np = (
    #             np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768
    #         )

    #         # Play locally
    #         sd.play(audio_np, samplerate=22050)  # adjust sample rate to your TTS output
    #         sd.wait()
    #     except Exception as e:
    #         raise Exception("Plant is unable to chat at the moment: ", e)
    #     return
