export const PLANT_TYPES = [
  "cactus",
  "photos",
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
