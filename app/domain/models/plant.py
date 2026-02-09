import datetime
import json

from domain.types import (
    EventType,
    LightState,
    PlantSettings,
    PlantType,
    SassLevel,
    Voice,
    WaterState,
)

MEMORY_FILE = "domain/models/memories.json"


class Plant:
    def __init__(self):
        self.id: str = "plant_0"
        self.name: str = "Lady Monstera McGreen, Queen of Swiss Cheesia"
        self.type: PlantType = PlantType.SWISS_CHEESE.value
        self.voice: Voice = Voice.ALLOY.value
        self.sassiness: SassLevel = SassLevel.MEDIUM.value

        self.water_state: WaterState = None
        self.light_state: LightState = None

        self.is_talking: bool = False
        self.last_watered: str = ""
        self.days_since_last_watered: int = 0

        self.get_last_watered()  # loads immediately

    def get_plant_settings(self):
        plant_settings = PlantSettings(
            name=self.name,
            type=self.type,
            voice=self.voice,
            sassiness=self.sassiness,
            days_since_last_watered=self.days_since_last_watered,
        )
        return plant_settings

    def get_last_watered(self):
        try:
            with open(MEMORY_FILE) as f:
                memory = json.load(f)
            plant_memory = memory.get(self.id)
            last_watered = datetime.datetime.fromisoformat(plant_memory["last_watered"])
            self.last_watered = last_watered
            time_passed = datetime.datetime.now().date() - last_watered.date()
            self.days_since_last_watered = time_passed.days
            return last_watered
        except Exception as e:
            print(f"unable to retrieve last time {self.name} was watered, ", e)

    def update_last_watered(self, last_watered_ts: datetime):
        try:
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)

            plant_memory = memory.get(self.id, {})
            self.last_watered = str(last_watered_ts)
            plant_memory["last_watered"] = str(last_watered_ts)
            time_passed = datetime.datetime.now().date() - last_watered_ts.date()
            self.days_since_last_watered = time_passed.days

            memory[self.id] = plant_memory
            with open(MEMORY_FILE, "w") as f:
                json.dump(memory, f, indent=4)  # indent=4 makes the JSON readable

            print(
                "successfully updated when last watered: ", self.days_since_last_watered
            )
        except Exception as e:
            print(f"unable to update last time {self.name} was watered", e)

    def get_light_state(self, light):
        match light:
            case light if light < 200:
                return LightState.DARK.value
            case light if 200 <= light < 700:
                return LightState.AMBIENT.value
            case light if light >= 700:
                return LightState.BRIGHT.value

    def get_water_state(self, water):
        match water:
            case water if water >= 600:
                return WaterState.DRY.value
            case water if 250 <= water < 600:
                return WaterState.OPTIMAL.value
            case water if water < 250:
                return WaterState.OVERWATERED.value

    def update_states(self, new_light_state: LightState, new_water_state: WaterState):
        self.light_state = new_light_state
        self.water_state = new_water_state
        pass
