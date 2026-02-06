from domain.types import Voice, PlantMood, PlantType


class Plant:
    def __init__(self, name: str, species: PlantType):
        self.name: str = name
        self.species: PlantType = species
        self.voice: Voice = Voice.ALLOY.value
        self.sass_level: PlantMood = PlantMood.EXTRA_SASSY.value
        self.is_talking: bool = False
        # self.last_moisture = None

    # def update_mood(self, moisture_level: int):
    # self.mood = "thirsty" if moisture_level < 300 else "content"
