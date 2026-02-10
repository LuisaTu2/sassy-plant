import base64
from abc import ABC, abstractmethod

from openai import OpenAI

from clients.constants import GPT_MODEL, GPT_MODEL_MINI_TTS, OPENAI_API_KEY
from domain.types import (
    AudioType,
    Voice,
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
        self.gpt_model: str = GPT_MODEL
        self.tts_model: str = GPT_MODEL_MINI_TTS

        self.temperature: float = 0.8
        self.audio_output_type: AudioType = AudioType.WAV.value
        self.speed: float = 1

        self.create_client()  # runs immediately

    def create_client(self):
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            print("openai client initialized")
            return self.client
        except Exception as e:
            raise Exception("unable to initialize openai client: ", e)

    def get_text_response(self, prompt):
        try:
            res = self.client.chat.completions.create(
                model=self.gpt_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                # max_tokens=50,
            )
            text = res.choices[0].message.content.strip()
            # print("received text response from llm")
            return text
        except Exception as e:
            raise Exception("unable to get text response: ", e)

    def get_audio_response(self, text: str, voice: Voice):
        try:
            response = self.client.audio.speech.create(
                model=self.tts_model,
                voice=voice,
                input=text,
                response_format=self.audio_output_type,
                speed=self.speed,
            )
            audio_bytes = response.read()  # WAV bytes
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            # print("received audio response from llm")
            return audio_b64
        except Exception as e:
            raise Exception("unable to get audio response: ", e)

    # def get_audio_bytes(self, text: str, voice: Voice) -> bytes:
    #     response = self.client.audio.speech.create(
    #         model=self.tts_model,
    #         voice=voice,
    #         input=text,
    #         response_format=self.audio_output_type,  # make sure this is raw bytes
    #         speed=self.speed,
    #     )
    #     audio_bytes = response.read()  # raw WAV bytes
    #     return audio_bytes

    # NEED TO PAY FOR STREAMING!
    # def get_audio_stream(self, text, voice):
    #     try:
    #         stream = self.client.audio.speech.create( # udpate the create here
    #             model=self.tts_model,
    #             voice=voice,
    #             input=text,
    #             # response_format=self.audio_output_type,
    #             # speed=self.speed,
    #         )
    #         return stream
    #     except Exception as e:
    #         raise Exception("unable to get audio stream: ", e)
