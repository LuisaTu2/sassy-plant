import { useEffect, useState } from "react";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Plant.css";

const Plant = () => {
  const { isTalking, event } = usePlantSettings();
  const [animation, setAnimation] = useState<string>("");

  useEffect(() => {
    if (event === null) {
      return;
    }

    if (event === "good_night") {
      setAnimation("good_night");
    }
  }, [event]);

  return (
    <div className="plant-section">
      <div
        className={`plant-background ${animation == "good_night" ? "plant-background-good-night" : ""}`}
      >
        {animation == "good_night" && <div className="good-night">🌙</div>}
        <div className={`plant ${isTalking ? "jump" : ""} `}>🪴</div>
      </div>
    </div>
  );
};

export default Plant;
