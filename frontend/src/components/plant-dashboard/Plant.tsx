import { useEffect } from "react";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Plant.css";

const Plant = () => {
  const { isTalking, event, lightState, setLightState } = usePlantSettings();

  useEffect(() => {
    if (event === null) {
      return;
    }

    console.log("EVENT: ", event);

    // handle light state changes
    if (event === "good_night") {
      setLightState("dark");
    } else if (event === "good_morning" || event === "take_off_sunglasses") {
      setLightState("ambient");
    } else if (event === "wear_sunglasses") {
      setLightState("bright");
    }

    // handle water state changes
    if (event === "watering") {
      // TODO: short animation
    }
  }, [event]);

  return (
    <div className="plant-section">
      <div className={`plant-background ${lightState}`}>
        {lightState == "dark" && <div className="moon">🌙</div>}
        {lightState == "bright" && (
          <div className={`sunglasses ${isTalking ? "jump" : ""}`}>🕶</div>
        )}
        <div className={`plant ${isTalking ? "jump" : ""} `}>🪴</div>
      </div>
    </div>
  );
};

export default Plant;
