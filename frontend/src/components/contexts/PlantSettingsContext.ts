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
} from "../types";

interface PlantSettings {
  name: string;
  plantType: PlantType;
  voice: VoiceType;
  sassiness: SassLevel;
  isTalking: boolean;
  isFormOpen: boolean;
  setName: Dispatch<SetStateAction<string>>;
  setPlantType: Dispatch<SetStateAction<PlantType>>;
  setVoice: Dispatch<SetStateAction<VoiceType>>;
  setSassiness: Dispatch<SetStateAction<SassLevel>>;
  setIsTalking: Dispatch<SetStateAction<boolean>>;
  setIsFormOpen: Dispatch<SetStateAction<boolean>>;
}

const noop: Dispatch<SetStateAction<string>> = () => {};
const noopPlantType: Dispatch<SetStateAction<PlantType>> = () => {};
const noopVoice: Dispatch<SetStateAction<VoiceType>> = () => {};
const noopSass: Dispatch<SetStateAction<SassLevel>> = () => {};
const noopBool: Dispatch<SetStateAction<boolean>> = () => {};

const defaultSettings = {
  name: "isa",
  plantType: PLANT_TYPES[0],
  voice: VOICE_TYPES[0],
  sassiness: SASS_LEVELS[0],
  isTalking: false,
  isFormOpen: false,
  setName: noop,
  setVoice: noopVoice,
  setPlantType: noopPlantType,
  setSassiness: noopSass,
  setIsTalking: noopBool,
  setIsFormOpen: noopBool,
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
