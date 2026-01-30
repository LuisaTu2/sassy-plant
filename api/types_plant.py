from enum import Enum

from pydantic import BaseModel


class PlantMood(Enum):
    HAPPY = "happy"
    SAD = "sad"
    THIRSTY = "thirsty"
    SLEEPY = "sleepy"
    EXTRA_SASSY = "extra_sassy"
    ANGRY = "angry"


class PlantState(BaseModel):
    soil_moisture: int
    light: int
    mood: PlantMood


class MessageType(Enum):
    READING = "reading"
    AUDIO = "audio"


class Reading(BaseModel):
    timestamp: str
    soil_moisture: int
    light: str | None


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
