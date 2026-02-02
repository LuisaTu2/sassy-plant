import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Plant.css";

const Plant = () => {
  const { isTalking } = usePlantSettings();

  return (
    <div className="plant-section">
      <div className={isTalking ? "plant jump" : "plant"}>🪴</div>
      {/* <div className={`plant-greetings ${sassyText ? "sassy" : ""}`}>
        {sassyText && isTalking
          ? sassyText
          : `Hi there, I'm ${name} a sassy ${plantType}!`}
      </div> */}
    </div>
  );
};

export default Plant;
