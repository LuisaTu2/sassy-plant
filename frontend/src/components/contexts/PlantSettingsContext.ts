import {
  createContext,
  useContext,
  type Dispatch,
  type SetStateAction,
} from "react";
import {
  type PlantType,
  type VoiceType,
  type SassLevel,
  VOICE_TYPES,
  PLANT_TYPES,
  SASS_LEVELS,
  type EventType,
  type PlantLightState,
  type PlantWaterState,
} from "../types";

interface PlantSettings {
  name: string;
  plantType: PlantType;
  voice: VoiceType;
  sassiness: SassLevel;
  isTalking: boolean;
  isFormOpen: boolean;
  sassyText: string;
  daysSinceLastWatered: number;
  event: EventType | null; // better on a different context but for now leave here
  lightState: PlantLightState | null;
  waterState: PlantWaterState | null;
  setName: Dispatch<SetStateAction<string>>;
  setPlantType: Dispatch<SetStateAction<PlantType>>;
  setVoice: Dispatch<SetStateAction<VoiceType>>;
  setSassiness: Dispatch<SetStateAction<SassLevel>>;
  setIsTalking: Dispatch<SetStateAction<boolean>>;
  setIsFormOpen: Dispatch<SetStateAction<boolean>>;
  setSassyText: Dispatch<SetStateAction<string>>;
  setDaysSinceLastWatered: Dispatch<SetStateAction<number>>;
  setEvent: Dispatch<SetStateAction<EventType | null>>;
  setLightState: Dispatch<SetStateAction<PlantLightState | null>>;
  setWaterState: Dispatch<SetStateAction<PlantWaterState | null>>;
}

const noop: Dispatch<SetStateAction<string>> = () => {};
const noopPlantType: Dispatch<SetStateAction<PlantType>> = () => {};
const noopVoice: Dispatch<SetStateAction<VoiceType>> = () => {};
const noopSass: Dispatch<SetStateAction<SassLevel>> = () => {};
const noopBool: Dispatch<SetStateAction<boolean>> = () => {};
const noopNumber: Dispatch<SetStateAction<number>> = () => {};
const noopEvent: Dispatch<SetStateAction<EventType | null>> = () => {};
const noopLightState: Dispatch<
  SetStateAction<PlantLightState | null>
> = () => {};
const noopWaterState: Dispatch<
  SetStateAction<PlantWaterState | null>
> = () => {};

const defaultSettings = {
  name: "Fernie Ferndale",
  plantType: PLANT_TYPES[0],
  voice: VOICE_TYPES[0],
  sassiness: SASS_LEVELS[0],
  isTalking: false,
  isFormOpen: false,
  sassyText: "",
  daysSinceLastWatered: 0,
  event: null,
  lightState: null,
  waterState: null,
  setName: noop,
  setVoice: noopVoice,
  setPlantType: noopPlantType,
  setSassiness: noopSass,
  setIsTalking: noopBool,
  setIsFormOpen: noopBool,
  setSassyText: noop,
  setDaysSinceLastWatered: noopNumber,
  setEvent: noopEvent,
  setLightState: noopLightState,
  setWaterState: noopWaterState,
};
export const PlantSettingsContext =
  createContext<PlantSettings>(defaultSettings);

export const usePlantSettings = () => {
  const ctx = useContext(PlantSettingsContext);
  if (!ctx)
    throw new Error(
      "usePlantSettings must be used inside a PlantSettingsProvider",
    );
  return ctx;
};
