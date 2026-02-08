import { type ReactNode, useState } from "react";
import { PlantSettingsContext } from "./PlantSettingsContext";
import {
  PLANT_TYPES,
  SASS_LEVELS,
  VOICE_TYPES,
  type PlantType,
  type SassLevel,
  type VoiceType,
} from "../types";

export const PlantSettingsProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [name, setName] = useState<string>("");
  const [plantType, setPlantType] = useState<PlantType>(PLANT_TYPES[0]);
  const [voice, setVoice] = useState<VoiceType>(VOICE_TYPES[0]);
  const [sassiness, setSassiness] = useState<SassLevel>(SASS_LEVELS[1]);
  const [isTalking, setIsTalking] = useState<boolean>(false);
  const [isFormOpen, setIsFormOpen] = useState<boolean>(false);
  const [sassyText, setSassyText] = useState<string>("");
  const [daysSinceLastWatered, setDaysSinceLastWatered] = useState<number>(0);

  return (
    <PlantSettingsContext.Provider
      value={{
        name,
        plantType,
        voice,
        sassiness,
        isTalking,
        isFormOpen,
        sassyText,
        daysSinceLastWatered,
        setName,
        setPlantType,
        setVoice,
        setSassiness,
        setIsTalking,
        setIsFormOpen,
        setSassyText,
        setDaysSinceLastWatered,
      }}
    >
      {children}
    </PlantSettingsContext.Provider>
  );
};
