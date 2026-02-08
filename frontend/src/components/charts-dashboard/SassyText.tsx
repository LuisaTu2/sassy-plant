import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./SassyText.css";

const SassyText = () => {
  const { name, isTalking, sassyText, plantType, voice } = usePlantSettings();

  return (
    <div className="sassy-text">
      <div className="sassy-text-title">meet the plant </div>
      {name && (
        <div className="sassy-text-details">
          <div className="sassy-text-detail">
            <div className="sassy-text-detail-title">name: </div>
            <div className="sassy-text-detail-value">{name}</div>
          </div>
          <div className="sassy-text-detail">
            <div className="sassy-text-detail-title">type: </div>
            <div className="sassy-text-detail-value">{plantType}</div>
          </div>
          <div className="sassy-text-detail">
            <div className="sassy-text-detail-title">voice: </div>
            <div className="sassy-text-detail-value">{voice}</div>
          </div>
        </div>
      )}

      {sassyText && isTalking ? sassyText : ``}
    </div>
  );
};

export default SassyText;
