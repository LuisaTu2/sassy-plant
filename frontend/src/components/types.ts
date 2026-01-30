export type MessageType = "reading" | "voice";
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
