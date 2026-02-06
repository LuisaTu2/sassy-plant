from enum import Enum

from pydantic import BaseModel

# 850–950	Bone dry	🚨 Bad – severely thirsty
# 700–850	Dry	⚠️ Needs water soon
# 450–700	Moist	✅ Good / ideal
# 300–450	Wet	😐 Okay short-term
# < 300	Saturated	❌ Bad – risk of root rot


class WaterState(Enum):
    EXTRA_DRY = "extra dry"
    DRY = "dry"
    MOIST = "moist"
    WET = "wet"
    OVERWATERED = "overwatered"
    UNCHANGED = "unchanged"


class WaterGradient(Enum):
    EXTRA_DRY = "#FFFFFF"
    DRY = "#B3D1FF"
    MOIST = "#66A3FF"
    WET = "#3366CC"
    OVERWATERED = "#003399"


# MOISTURE_GRADIENT_5 = [
#     "#FFFFFF",  # very dry / start
#     "#B3D1FF",  # light blue
#     "#66A3FF",  # medium blue
#     "#3366CC",  # rich blue
#     "#003399",  # deep dark blue / fully wet
# ]


class LightState_1(Enum):
    DARK = "dark"
    VERY_LOW = "very low"
    LOW = "low"
    OK = "ok"
    GREAT = "great"
    INTENSE = "intense"
    UNCHANGED = "unchanged"


class LightGradient(Enum):
    DARK = "#000000"
    VERY_LOW = "#333333"
    LOW = "#666666"
    OK = "#999999"
    GREAT = "#CCCCCC"
    INTENSE = "#FFFFFF"


class PlantMood(Enum):
    HAPPY = "happy"
    SAD = "sad"
    SLEEPY = "sleepy"
    EXTRA_SASSY = "extra_sassy"
    ANGRY = "angry"


class PlantReading(BaseModel):
    soil_moisture: int
    light: int
    mood: PlantMood


class MessageType(Enum):
    READING = "reading"
    AUDIO = "audio"


class Reading(BaseModel):
    soil_moisture: str
    light: str
    mood: str
    timestamp: str


class ReadingMessage(BaseModel):
    type: MessageType.READING.value
    payload: Reading


class AudioType(Enum):
    MP3 = "mp3"  # default response format for general use cases
    OPUS = "opus"  # for internet streaming and communications, low latency
    ACC = "acc"  #  for digital audio compression, preferred by YouTube, Androis, iOS
    FLAC = "flac"  # for lossless audio compression, favoured by audio enthusiasts for archiving
    WAV = "wav"  # uncompressed WAV audio, suitable for low-latency applications to avoid decoding overhead
    PCM = "pcm"  # similar to WAV but contains the raw samples in 24kHz (16-bit signed, low-endian), without the header.


class AudioMessage(BaseModel):
    type: MessageType.AUDIO.value
    payload: AudioType


class Voice(Enum):
    ALLOY = "alloy"
    ASH = "ash"
    BALLAD = "ballad"
    CORAL = "coral"
    ECHO = "echo"
    FABLE = "fable"
    NOVA = "nova"
    ONYX = "onyx"
    SAGE = "sage"
    SHIMMER = "shimmer"
    VERSE = "verse"
    MARIN = "marin"
    CEDAR = "cedar"


class PlantType(Enum):
    CACTUS = "cactus"
    POTHOS = "pothos"
    FERN = "fern"
    SPIDER_PLANT = "spider plant"
    BAMBOO = "bamboo"
    BASIL = "basil"
    SNAKE_PLANT = "snake plant"


# class VoiceType(Enum):
#     ALLOY = "alloy"
#     ASH = "ash"
#     BALLAD = "ballad"
#     CORAL = "coral"
#     ECHO = "echo"
#     FABLE = "fable"
#     NOVA = "nova"
#     ONYX = "onyx"
#     SAGE = "sage"
#     SHIMMER = "shimmer"
#     VERSE = "verse"
#     MARIN = "marin"
#     CEDAR = "cedar"


class Sassiness(Enum):
    LOW = "low"
    MILD = "mild"
    MEDIUM = "medium"
    HIGH = "high"
    EXTRA = "extra"


class PlantSettings(BaseModel):
    name: str
    plant_type: PlantType
    voice: Voice
    sassiness: Sassiness


current_plant_settings: dict = {
    "name": "Maria",
    "plant_type": "BASIL",
    "voice": "ALLOY",
    "sassiness": "HIGH",
}


from dataclasses import dataclass


@dataclass
class StateChange:
    water_state_1: WaterState
    water_state_2: WaterState
    light_state_1: LightState_1
    light_state_2: LightState_1
    has_water_state_changed: bool
    has_light_state_changed: bool


# | Condition       | Expected analogRead |
# | --------------- | ------------------- |
# | Dark / night    | ~0–200              |
# | Indoor lighting | ~200–700            |
# | Bright sunlight | ~700–1023           |


class LightState(Enum):
    DARK = "dark"
    SOFT = "soft"
    BRIGHT = " bright"
