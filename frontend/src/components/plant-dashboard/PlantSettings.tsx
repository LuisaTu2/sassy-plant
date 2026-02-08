import { useEffect, useRef } from "react";
import "./PlantSettings.css";
import {
  type PlantType,
  type VoiceType,
  type SassLevel,
  PLANT_TYPES,
  SASS_LEVELS,
  VOICE_TYPES,
} from "../types";
import { usePlantSettings } from "../contexts/PlantSettingsContext";

const PlantSettings = () => {
  const {
    name,
    plantType,
    voice,
    sassiness,
    isFormOpen,
    setName,
    setPlantType,
    setVoice,
    setSassiness,
    setIsFormOpen,
    setDaysSinceLastWatered,
  } = usePlantSettings();

  const plantSettingsRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const request_body = JSON.stringify({
      name: name,
      type: plantType,
      voice: voice,
      sassiness,
    });

    try {
      const response = await fetch(
        "http://127.0.0.1:9000/update-plant-settings/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: request_body,
        },
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log("result: ", result);
    } catch (error) {
      console.log("an error occurred", error);
    } finally {
      setIsFormOpen(false);
    }
  };

  // close settings on click outside of form
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        plantSettingsRef.current &&
        !plantSettingsRef.current.contains(event.target as Node)
      ) {
        setIsFormOpen(false);
      }
    };

    if (isFormOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isFormOpen, setIsFormOpen]);

  const fetchPlantSettings = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:9000/get-plant-settings/",
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setName(result["name"]);
      setPlantType(result["type"]);
      setVoice(result["voice"]);
      setSassiness(result["sassiness"]);
      setDaysSinceLastWatered(result["days_since_last_watered"]);
    } catch (error) {
      console.error("an error occurred:", error);
    } finally {
      setIsFormOpen(false);
    }
  };

  useEffect(() => {
    fetchPlantSettings();
  }, []);

  return (
    <div
      className={`plant-settings-form ${isFormOpen ? "open-form" : ""} `}
      ref={plantSettingsRef}
    >
      <div className="close-btn-wrapper">
        {" "}
        <button
          className="close-btn"
          onClick={() => {
            setIsFormOpen(false);
          }}
        >
          &times;
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
              <div className="plant-settings-input-label">sassiness: </div>
              <select
                value={sassiness}
                onChange={(e) => setSassiness(e.target.value as SassLevel)}
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
        <button type="submit">Save Settings</button>
      </form>
    </div>
  );
};

export default PlantSettings;
