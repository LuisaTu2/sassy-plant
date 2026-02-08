from domain.types import (
    LightState,
    PlantType,
    WaterState,
)


def get_base_prompt(
    plant_name: str,
    plant_type: PlantType,
    user_input,
):
    return f"""
            Your name is {plant_name} and you are a virtual {plant_type} plant with a sassy personality.
            Keep responses short and witty. Respond in 2 complete sentences.
            Human says: "{user_input}". You respond in-character.
            """


def get_state_change_prompt(
    plant_name: str,
    plant_type: PlantType,
    light_state: LightState,
    new_light_state: LightState,
    water_state: WaterState,
    new_water_state: WaterState,
):
    prompt = f"""
            Your name is {plant_name} and you are a virtual {plant_type} plant with a sassy personality.
            Keep responses short and witty. Respond in 2 complete sentences.
            You respond in-character.
            """

    if light_state != new_light_state:
        prompt += f"""
            Comment on how the light level has gone from {light_state} to {new_light_state}. Adjust mood accordingly.
        """

    if water_state != new_water_state:
        prompt += f"""
            Comment on how the light level has gone from {water_state} to {new_water_state}. Adjust mood accordingly.
        """

    return prompt
