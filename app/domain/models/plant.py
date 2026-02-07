from domain.types import PlantMood, PlantType, Voice


class Plant:
    def __init__(self):
        self.name: str = "Fernie Green"
        self.type: PlantType = PlantType.FERN
        self.voice: Voice = Voice.ALLOY.value
        self.sass_level: PlantMood = PlantMood.EXTRA_SASSY.value
        self.is_talking: bool = False

    def get_last_watered(self):
        pass
