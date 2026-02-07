import asyncio
import datetime
import json
import math
import random

from fastapi import WebSocket

from domain.types import (
    LightState_1,
    MessageType,
    Sassiness,
    StateChange,
    WaterState,
)


def get_water_state(reading):
    match reading:
        case r if 850 <= r <= 10000:
            return WaterState.EXTRA_DRY.value
        case r if 700 <= r < 850:
            return WaterState.DRY.value
        case r if 450 <= r < 700:
            return WaterState.MOIST.value
        case r if 300 <= r < 450:
            return WaterState.WET.value
        case r if r < 300:
            return WaterState.OVERWATERED.value


def get_light_state(reading):
    match reading:
        case r if r <= 10:
            return LightState_1.DARK.value
        case r if 10 < r <= 100:
            return LightState_1.VERY_LOW.value
        case r if 100 < r <= 300:
            return LightState_1.LOW.value
        case r if 300 < r <= 1000:
            return LightState_1.OK.value
        case r if 1000 < r <= 10000:
            return LightState_1.GREAT.value
        case r if r > 10000:
            return LightState_1.INTENSE.value


def get_state_changes(moisture, light):
    water1 = moisture[0]
    water2 = moisture[-1]
    if water1 - water2 >= 100:
        water_state_1 = get_water_state(water1)
        water_state_2 = get_water_state(water2)
    else:
        water_state_1 = WaterState.UNCHANGED.value
        water_state_2 = WaterState.UNCHANGED.value

    light_1 = light[0]
    light_2 = light[-1]

    if light_2 - light_1 >= 20:
        light_state_1 = get_light_state(light_1)
        light_state_2 = get_light_state(light_2)
    else:
        light_state_1 = LightState_1.UNCHANGED.value
        light_state_2 = LightState_1.UNCHANGED.value

    state_chage = StateChange(
        water_state_1=water_state_1,
        water_state_2=water_state_2,
        light_state_1=light_state_1,
        light_state_2=light_state_2,
        has_water_state_changed=water_state_1 != water_state_2,
        has_light_state_changed=light_state_1 != light_state_2,
    )
    return state_chage


# Assign numeric indices for mood calculation
WATER_INDEX = {"extra dry": 0, "dry": 1, "moist": 2, "wet": 3, "overwatered": 4}

LIGHT_INDEX = {"dark": 0, "very low": 1, "low": 2, "ok": 3, "great": 4, "intense": 5}


# Mood score calculation (0-100)
def plant_mood_score_from_readings(light_reading: int, water_reading: int) -> float:
    light_state = get_light_state(light_reading)
    water_state = get_water_state(water_reading)

    # Convert to indices
    li = LIGHT_INDEX[light_state]
    wi = WATER_INDEX[water_state]

    # Define “ideal” for Gaussian peak
    ideal_light = 4  # GREAT
    ideal_water = 2  # MOIST

    sigma_light = 1.2
    sigma_water = 1.2

    score = math.exp(
        -(
            (li - ideal_light) ** 2 / (2 * sigma_light**2)
            + (wi - ideal_water) ** 2 / (2 * sigma_water**2)
        )
    )
    return round(score * 100, 1)


async def simulate_and_send_readings(websocket: WebSocket):
    first_reading = None
    last_reading = None
    for i in range(20):
        plant_data = {
            "soil_moisture": random.randint(0, 1000),
            "timestamp": datetime.datetime.now().isoformat(),
        }
        if i == 0:
            first_reading = plant_data
        if i == 19:
            last_reading = plant_data
        message = {
            "type": MessageType.READING.value,
            "payload": plant_data,
        }
        await websocket.send_text(json.dumps(message))
        await asyncio.sleep(0.1)
    return first_reading, last_reading


def temperature_sassiness_mapping(sassiness: Sassiness):
    match sassiness:
        case Sassiness.LOW.value:
            return 0.2
        case Sassiness.MILD.value:
            return 0.4
        case Sassiness.MEDIUM.value:
            return 0.5
        case Sassiness.HIGH.value:
            return 0.7
        case Sassiness.EXTRA.value:
            return 1.5
    pass


sensor_port = "/dev/ttyACM0"
sensor_baudrate = 9600
