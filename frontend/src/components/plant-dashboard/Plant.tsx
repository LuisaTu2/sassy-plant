import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Plant.css";

const Plant = () => {
  const { isTalking } = usePlantSettings();

  return (
    <div className="plant-section">
      <div className={isTalking ? "plant jump" : "plant"}>🪴</div>
    </div>
  );
};

export default Plant;
