import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./SassyText.css";

const SassyText = () => {
  const { name, isTalking, sassyText, plantType } = usePlantSettings();

  return (
    <div className="sassy-text">
      {sassyText && isTalking
        ? sassyText
        : `Hi there, I'm ${name} a sassy ${plantType}!`}
    </div>
  );
};

export default SassyText;
