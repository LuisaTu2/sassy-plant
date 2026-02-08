from domain.types import PlantSettings, PlantType, SassLevel, Voice


class Plant:
    def __init__(self):
        self.name: str = "Fernie Green"
        self.type: PlantType = PlantType.FERN.value
        self.voice: Voice = Voice.ALLOY.value
        self.sassiness: SassLevel = SassLevel.MEDIUM.value
        self.is_talking: bool = False

    def get_plant_settings(self):
        plant_settings = PlantSettings(
            name=self.name, type=self.type, voice=self.voice, sassiness=self.sassiness
        )
        return plant_settings

    def get_last_watered(self):
        pass
