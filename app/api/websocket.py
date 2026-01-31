import json

from fastapi import APIRouter, WebSocket

from clients.llm_client import llm_client
from domain.types import AudioType, PlantMood, PlantReading
from domain.utils import simulate_and_send_readings

router = APIRouter()


@router.websocket("/ws/sensors")
async def websocket_endpoint(ws: WebSocket):
    try:
        await ws.accept()
        first_reading, last_reading = await simulate_and_send_readings(ws)
        is_state_changed = (
            abs(first_reading["soil_moisture"] - last_reading["soil_moisture"]) >= 100
        )
        # check for any significant changes in sensor readings
        if is_state_changed:
            plant_reading: PlantReading = {
                "soil_moisture": 455,
                "light": 8988,
                "mood": PlantMood.EXTRA_SASSY.value,
            }
            text = llm_client.get_sassy_answer(
                plant_reading,
                "Whats up Patricia",
            )
            print(text)
            audio_b64 = await llm_client.get_audio(text)
            await ws.send_text(
                json.dumps(
                    {
                        "type": "voice",
                        "payload": {
                            "audio": audio_b64,
                            "format": AudioType.WAV.value,
                            "text": text,
                        },
                    }
                )
            )
    except Exception as e:
        # optionally notify frontend
        # await ws.send_text(json.dumps({"type": "error", "payload": {"message": str(e)}}))
        raise Exception("unable to send voice audio: ", e)
