import datetime
import json

from domain.types import PlantSettings, PlantType, SassLevel, Voice

MEMORY_FILE = "domain/models/memories.json"


class Plant:
    def __init__(self):
        self.id: str = "plant_0"
        self.name: str = "Fernie Green"
        self.type: PlantType = PlantType.FERN.value
        self.voice: Voice = Voice.ALLOY.value
        self.sassiness: SassLevel = SassLevel.MEDIUM.value
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
            last_watered = datetime.datetime.fromisoformat(
                plant_memory["last_time_watered"]
            )
            self.last_watered = last_watered
            time_passed = datetime.datetime.now().date() - last_watered.date()
            self.days_since_last_watered = time_passed.days
            return last_watered
        except Exception as e:
            print(f"unable to retrieve last time {self.name} was watered, ", e)
