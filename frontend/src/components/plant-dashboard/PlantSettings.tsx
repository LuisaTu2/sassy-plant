import { useEffect, useRef, useState } from "react";
import "./PlantSettings.css";
import {
  PLANT_TYPES,
  SASS_LEVELS,
  VOICE_TYPES,
  type PlantType,
  type SassLevel,
  type VoiceType,
} from "./plant-settings";

interface PlantSettingsProps {
  showSettings: boolean;
  setShowSettings: React.Dispatch<React.SetStateAction<boolean>>;
}

const PlantSettings = ({
  showSettings,
  setShowSettings,
}: PlantSettingsProps) => {
  const [name, setName] = useState<string>("");
  const [plantType, setPlantType] = useState<PlantType>();
  const [voice, setVoice] = useState<VoiceType>();
  const [sassLevel, setSassLevel] = useState<SassLevel>();
  const plantSettingsRef = useRef<HTMLDivElement>(null);
  const handleSubmit = () => {
    console.log("show settings: ", setShowSettings);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        plantSettingsRef.current &&
        !plantSettingsRef.current.contains(event.target as Node)
      ) {
        setShowSettings(false);
      }
    };

    if (showSettings) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showSettings, setShowSettings]);
  return (
    <div
      className={`plant-settings-form ${showSettings ? "open-form" : ""} `}
      ref={plantSettingsRef}
    >
      <div className="close-btn-wrapper">
        {" "}
        <button
          className="close-btn"
          onClick={() => {
            setShowSettings(false);
          }}
        >
          X
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="settings-wrapper">
          <div>
            <label className="plant-settings-input">
              <div className="plant-settings-input-label">plant name: </div>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                defaultValue={"plant name"}
                className="name-input"
              />
            </label>
          </div>

          <div>
            <label className="plant-settings-input">
              <div className="plant-settings-input-label">plant type: </div>
              <select
                value={plantType}
                onChange={(e) => setPlantType(e.target.value as PlantType)}
              >
                {PLANT_TYPES.map((pt) => (
                  <option value={pt} key={pt}>
                    {pt}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div>
            <label className="plant-settings-input">
              <div className="plant-settings-input-label">plant voice: </div>
              <select
                value={voice}
                onChange={(e) => setVoice(e.target.value as VoiceType)}
              >
                {VOICE_TYPES.map((vt) => (
                  <option value={vt} key={vt}>
                    {vt}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div>
            <label className="plant-settings-input">
              <div className="plant-settings-input-label">sass level: </div>
              <select
                value={sassLevel}
                onChange={(e) => setSassLevel(e.target.value as SassLevel)}
              >
                {SASS_LEVELS.map((sl) => (
                  <option value={sl} key={sl}>
                    {sl}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>
        <button
          type="submit"
          onClick={(e) => {
            e.preventDefault();
            // setShowSettings(false);
          }}
        >
          Save Settings
        </button>
      </form>
    </div>
  );
};

export default PlantSettings;
