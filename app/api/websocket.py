from collections import deque
import json

from fastapi import APIRouter, WebSocket

from clients.llm_client import llm_client
from domain.types import AudioType, PlantMood, PlantReading, WaterState
from domain.utils import simulate_and_send_readings
from domain.sensor_readings import get_water_and_light_reading
import asyncio


router = APIRouter()


def get_water_state(reading):
    match reading:
        case r if 850 <= r <= 950:
            return WaterState.EXTRA_DRY.value
        case r if 700 <= r < 850:
            return WaterState.DRY.value
        case r if 450 <= r < 700:
            return WaterState.MOIST.value
        case r if 300 <= r < 450:
            return WaterState.WET.value
        case r if r < 300:
            return WaterState.OVERWATERED.value


def get_comments(moisture, light):
    should_comment_on_water = False
    m1 = moisture[0]
    m2 = moisture[-1]
    if m1 - m2 >= 100:
        ml1 = get_water_state(m1)
        ml2 = get_water_state(m2)
        if ml1 != ml2:
            should_comment_on_water = True
    else:
        ml1 = WaterState.UNCHANGED.value
        ml2 = WaterState.UNCHANGED.value
    return m1, m2, ml1, ml2, should_comment_on_water, False


is_talking = False


async def receiver(ws: WebSocket):
    global is_talking
    while True:
        msg = await ws.receive_text()
        data = json.loads(msg)

        if data["type"] == "voice_done":
            print("received done talking notification ")
            is_talking = False


@router.websocket("/ws/sensors")
async def websocket_endpoint(ws: WebSocket):
    try:
        await ws.accept()
        global is_talking

        receiver_task = asyncio.create_task(receiver(ws))

        moisture_readings = deque()
        light_readings = deque()

        for t in range(2000):
            moisture_reading, light_reading = await get_water_and_light_reading(ws, t)
            moisture_readings.append(moisture_reading)
            light_readings.append(light_reading)
            if len(moisture_readings) >= 5:
                m1, m2, ml1, ml2, should_comment_on_water, should_comment_on_light = (
                    get_comments(moisture_readings, light_readings)
                )
                print(
                    "readings: ",
                    m1,
                    m2,
                    ml1,
                    ml2,
                    should_comment_on_water,
                    should_comment_on_light,
                )
                if not is_talking and ml1 != ml2:
                    is_talking = True
                    text = llm_client.get_sassy_answer(
                        user_input="Whats up gurl",
                        ml1=ml1,
                        ml2=ml2,
                        should_comment_on_water=should_comment_on_water,
                        should_comment_on_light=should_comment_on_light,
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

                moisture_readings.popleft()
                light_readings.popleft()

            await asyncio.sleep(0.1)
        receiver_task.cancel()
    except Exception as e:
        # optionally notify frontend
        # await ws.send_text(json.dumps({"type": "error", "payload": {"message": str(e)}}))
        raise Exception("unable to send voice audio: ", e)
