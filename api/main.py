import json

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from openai_client import OpenAIClient
from types_plant import PlantState, AudioType, PlantMood
from utils import simulate_and_send_readings

app = FastAPI(title="sassy plant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize openai
llm_client = OpenAIClient()
llm_client.create_client()

text = "Hola soy tu sassy plantita 😏"
plant_state: PlantState = {
    "soil_moisture": 0,
    "light": 0,
    "mood": PlantMood.EXTRA_SASSY.value,
}


@app.websocket("/ws/sensors")
async def websocket_endpoint(ws: WebSocket):
    try:
        await ws.accept()
        first_reading, last_reading = await simulate_and_send_readings(ws)
        is_state_changed = (
            abs(first_reading["soil_moisture"] - last_reading["soil_moisture"]) >= 100
        )
        # check for any significant changes in sensor readings
        if is_state_changed:
            audio_b64 = await llm_client.get_audio(
                plant_state, user_input="How are you feeling?"
            )
            await ws.send_text(
                json.dumps(
                    {
                        "type": "voice",
                        "payload": {"audio": audio_b64, "format": AudioType.WAV.value},
                    }
                )
            )
    except Exception as e:
        # optionally notify frontend
        # await ws.send_text(json.dumps({"type": "error", "payload": {"message": str(e)}}))
        raise Exception("unable to send voice audio: ", e)


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
