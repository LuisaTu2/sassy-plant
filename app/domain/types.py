from enum import Enum

from pydantic import BaseModel


class MessageType(Enum):
    DATA_POINT = "data_point"
    STATE_CHANGE = "state_change"
    UPDATE_DAYS_LAST_WATERED = "update_days_last_watered"


class DataPoint(BaseModel):
    soil_moisture: str
    light: str
    timestamp: str


class AudioType(Enum):
    MP3 = "mp3"  # default response format for general use cases
    OPUS = "opus"  # for internet streaming and communications, low latency
    ACC = "acc"  #  for digital audio compression, preferred by YouTube, Androis, iOS
    FLAC = "flac"  # for lossless audio compression, favoured by audio enthusiasts for archiving
    WAV = "wav"  # uncompressed WAV audio, suitable for low-latency applications to avoid decoding overhead
    PCM = "pcm"  # similar to WAV but contains the raw samples in 24kHz (16-bit signed, low-endian), without the header.


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


class SassLevel(Enum):
    LOW = "low"
    MILD = "mild"
    MEDIUM = "medium"
    HIGH = "high"
    EXTRA = "extra"


class PlantSettings(BaseModel):
    name: str
    type: PlantType
    voice: Voice
    sassiness: SassLevel
    days_since_last_watered: int


# | Condition       | Expected analogRead |
# | --------------- | ------------------- |
# | Dark / night    | ~0–200              |
# | Indoor lighting | ~200–700            |
# | Bright sunlight | ~700–1023           |


class LightState(Enum):
    DARK = "dark"
    AMBIENT = "ambient"
    BRIGHT = " bright"


# ≥ 600 → DRY

# 250–600 → OPTIMAL

# < 250 → SATURATED


class WaterState(Enum):
    DRY = "dry"
    OPTIMAL = "optimal"
    OVERWATERED = "overwatered"


class EventType(Enum):
    DRYING = "drying"
    WATERING = "watering"
    GOOD_NIGHT = "good_night"
    GOOD_MORNING = "good_morning"
    WEAR_SUNGLASSES = "wear_sunglasses"
    TAKE_OFF_SUNGLASSES = "take_off_sunglasses"
