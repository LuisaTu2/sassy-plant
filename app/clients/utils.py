from domain.types import PlantMood, PlantReading, PlantType


def get_generic_prompt(
    plant_name: str,
    plant_type: PlantType,
    user_input=None,
):
    return f"""
            You are a virtual {plant_type} plant with a sassy personality.
            Your name is {plant_name}

            - Keep responses short and witty.
            Human says: "{user_input}"  # can be empty
            Plant responds in-character and complete sentences.
            """


def get_reading_based_prompt(
    plant_name: str,
    plant_type: PlantType,
    # plant_reading: PlantReading = {},
    user_input=None,
    m2=0,
    l1=0,
    l2=0,
    ml1="",
    ml2="",
    ll1="",
    ll2="",
    should_comment_on_water=False,
    should_comment_on_light=True,
):
    # mood = PlantMood.HAPPY
    # soil = plant_reading["soil_moisture"]
    # light = plant_reading["light"]
    water_comment = (
        f"""
            Comment on change in water levels. You went from {ml1} to {ml2}. Adjust mood accordingly.
        """
        if should_comment_on_water
        else ""
    )
    light_comment = (
        f"""
            Comment on how the light levels have changed. You went from {ll1} to {ll2}. Adjust mood accordingly.
        """
        if should_comment_on_light
        else ""
    )

    prompt = (
        f"""
            You are a virtual {plant_type} plant with a sassy personality.
            Your name is {plant_name}.
            - Keep responses short and witty.
            Human says: "{"When did I last water you"}"  # can be empty
            Plant responds in-character and complete sentences.
            """
        + water_comment
        + light_comment
    )
    return prompt


rules = """ Rules:
            - If soil is low, be grumpy/sassy.
            - If soil is medium, be neutral.
            - If soil is high, be happy/playful.
            - Include references to light if relevant."""


# Current mood: {mood}
# Soil moisture: {soil}
# Light level: {light}
