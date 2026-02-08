export type MessageType = "data_point" | "state_change";
export type Message = {
  type: MessageType;
  payload: PlantState | Audio;
};

export type Audio = {
  audio: string;
};

export type PlantState = {
  timestamp: string; // ISO string, e.g. "2026-01-29T00:00:00Z"
  soil_moisture: number;
};

export const PLANT_TYPES = [
  "cactus",
  "pothos",
  "fern",
  "spider plant",
  "bamboo",
  "basil",
  "snake plant",
] as const;

export type PlantType = (typeof PLANT_TYPES)[number];

export const VOICE_TYPES = [
  "alloy",
  "ash",
  "ballad",
  "coral",
  "echo",
  "fable",
  "nova",
  "onyx",
  "sage",
  "shimmer",
  "verse",
  "marin",
  "cedar",
] as const;

export type VoiceType = (typeof VOICE_TYPES)[number];

export const SASS_LEVELS = ["low", "mild", "medium", "high", "extra"] as const;

export type SassLevel = (typeof SASS_LEVELS)[number];

export type PlantSettings = {
  name: string;
  type: PlantType;
  voice: VoiceType;
  sassLevel: SassLevel;
  days_since_last_watered: number;
};

export type EventType =
  | "drying"
  | "watering"
  | "good_night"
  | "good_morning"
  | "wear_sunglasses"
  | "take_off_sunglasses";
