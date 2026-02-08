from domain.types import PlantSettings, PlantType, Sassiness, Voice


class Plant:
    def __init__(self):
        self.name: str = "Fernie Green"
        self.type: PlantType = PlantType.FERN
        self.voice: Voice = Voice.ALLOY.value
        self.sassiness: Sassiness = Sassiness.MEDIUM.value
        self.is_talking: bool = False

    def get_plant_settings(self):
        plant_settings = PlantSettings(
            name=self.name, type=self.type, voice=self.voice, sassiness=self.sassiness
        )
        return plant_settings

    def get_last_watered(self):
        pass
