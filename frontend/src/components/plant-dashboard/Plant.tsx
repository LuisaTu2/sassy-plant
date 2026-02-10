import { useEffect, useState } from "react";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Plant.css";

const Plant = () => {
  const { isTalking, event, lightState, plantType, setLightState } =
    usePlantSettings();

  const [animation, setAnimation] = useState<string>("");

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
      setAnimation("watering");
      setTimeout(() => setAnimation(""), 20000);
    }
  }, [event]);

  return (
    <div className="plant-section">
      <div className={`plant-background ${lightState}`}>
        {lightState === "dark" && <div className="moon"></div>}
        {lightState === "bright" && (
          <div className={`sunglasses ${isTalking ? "jump" : ""}`}></div>
        )}
        {animation === "watering" && <div className="watercan"></div>}
        {plantType === "swiss cheese" ? (
          <div className={`plant plant-monstera ${isTalking ? "jump" : ""}`} />
        ) : (
          <div className={`plant ${isTalking ? "jump" : ""} `}>🪴</div>
        )}
      </div>
    </div>
  );
};

export default Plant;
