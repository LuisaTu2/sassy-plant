import math
import random


# -------------------------
# CONFIG
# -------------------------

TICK_SECONDS = 10

# Soil moisture (analogRead-like)
MOISTURE_MIN = 350
MOISTURE_MAX = 900
DRY_RATE = 1.2  # per tick
WATER_JUMP = -980
MOISTURE_NOISE = 6

# Light (lux)
LUX_MIN = 8
LUX_MAX = 1200
LUX_NOISE = 20
DAY_CYCLE_SECONDS = 50 * 60  # 5-minute compressed day
SUNRISE = 0.15
SUNSET = 0.85


# -------------------------
# SENSOR STATE
# -------------------------

moisture = random.randint(650, 800)
time_in_cycle = 0
occluded = False
water_event = False


# -------------------------
# UPDATE FUNCTIONS
# -------------------------


def update_moisture():
    global moisture, water_event

    if water_event:
        moisture += WATER_JUMP
        water_event = False
    else:
        moisture += DRY_RATE

    # noise
    moisture += random.uniform(-MOISTURE_NOISE, MOISTURE_NOISE)

    # mean reversion (after watering)
    if moisture < 500:
        moisture += random.uniform(0, 2)

    moisture = max(MOISTURE_MIN, min(MOISTURE_MAX, moisture))
    return int(moisture)


def update_light():
    global time_in_cycle

    phase = (time_in_cycle % DAY_CYCLE_SECONDS) / DAY_CYCLE_SECONDS

    if phase < SUNRISE or phase > SUNSET:
        base_lux = LUX_MIN
    else:
        day_phase = (phase - SUNRISE) / (SUNSET - SUNRISE)
        base_lux = LUX_MIN + math.sin(day_phase * math.pi) * (LUX_MAX - LUX_MIN)

    if occluded:
        base_lux *= 0.1

    lux = base_lux + random.uniform(-LUX_NOISE, LUX_NOISE)
    lux = max(0, lux)

    time_in_cycle += TICK_SECONDS
    return int(lux)


# -------------------------
# EVENT HELPERS
# -------------------------


def pour_water():
    global water_event
    water_event = True


def cover_sensor():
    global occluded
    occluded = True


def uncover_sensor():
    global occluded
    occluded = False


# -------------------------
# MAIN LOOP (demo)
# -------------------------


# async def get_water_and_light_reading(ws: WebSocket, t):
#     if t == 50:
#         pour_water()  # simulate watering
#     # if t == 30:
#     #     cover_sensor()  # simulate shade
#     # if t == 90:
#     #     uncover_sensor()
#     # if t == 110:
#     #     pour_water()

#     moisture_val = update_moisture()
#     light_val = update_light()
#     mood = plant_mood_score_from_readings(moisture_val, light_val)

#     plant_data: Reading = {
#         "soil_moisture": moisture_val / 1000,
#         "light": light_val / 1400,
#         "mood": mood / 100,
#         "timestamp": datetime.datetime.now().isoformat(),
#     }
#     message: ReadingMessage = {
#         "type": MessageType.READING.value,
#         "payload": plant_data,
#     }

#     # print(
#     #     f"[{t:02d}] moisture={moisture_val:4d}  light={light_val:4d} lux {datetime.datetime.now()}"
#     # )

#     await ws.send_text(json.dumps(message))
#     return moisture_val, light_val
