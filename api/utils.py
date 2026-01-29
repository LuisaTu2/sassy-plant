import asyncio
import random

from types_plant import PlantMood, PlantState


def get_plant_mood(plant_state):
    # Simple mood logic based on soil
    soil_moisture = plant_state["soil_moisture"]
    mood: PlantMood = PlantMood.HAPPY
    if soil_moisture < 300:
        mood = PlantMood.ANGRY
    elif 300 < soil_moisture < 600:
        mood = PlantMood.SAD
    else:
        mood = PlantMood.EXTRA_SASSY
    return mood


async def read_sensors(plant_state: PlantState):
    for _ in range(10):
        plant_state["soil_moisture"] = random.randint(0, 1000)
        plant_state["light"] = random.randint(0, 1000)
        plant_mood: PlantMood = get_plant_mood(plant_state)
        plant_state["mood"] = plant_mood
        print("plant state: ", plant_state["mood"].value)
        await asyncio.sleep(0.1)  # simulate 1-second sensor interval
