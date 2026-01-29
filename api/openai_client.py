from llm_client import LLMClient
from constants import OPENAI_API_KEY, OPENAI_MODEL
from openai import OpenAI
import json


class OpenAIClient(LLMClient):

    def __init__(self):
        self.client = None
        self.model = OPENAI_MODEL
        self.plant_state = None
        self.create_client()  # runs as soon as obejct is created

    def create_client(self):
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            raise Exception("Could not initialize OpenAI client: ", e)
        print("Open AI client initialized")
        return

    def create_prompt(self, plant_state, user_input=None):
        """
        plant_state: dict containing soil, light, mood
        user_input: optional string if human says something
        """
        mood = plant_state["mood"]
        soil = plant_state["soil"]
        light = plant_state["light"]

        prompt = f"""
            You are a virtual plant with a sassy personality.
            Current mood: {mood}
            Soil moisture: {soil}
            Light level: {light}

            Rules:
            - If soil is low, be grumpy/sassy.
            - If soil is medium, be neutral.
            - If soil is high, be happy/playful.
            - Include references to light if relevant.
            - Keep responses short and witty.

            Human says: "{user_input}"  # can be empty

            Plant responds in-character.
            """
        return prompt

    def get_response(self, plant_state, user_input=None):
        prompt = self.create_prompt(plant_state, user_input)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            # max_tokens=50,
            temperature=0.8,  # more creative/witty
        )

        return response.choices[0].message.content.strip()


# def get_plant_response(state, user_input=None):
#     prompt = make_prompt(state, user_input)
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=50,
#         temperature=0.8,  # more creative/witty
#     )
#     return response.choices[0].message.content.strip()
