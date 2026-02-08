import { useEffect, useState } from "react";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./SassyText.css";

interface SassyTextProps {
  wsRef: React.RefObject<WebSocket | null>;
}

const SassyText = ({ wsRef }: SassyTextProps) => {
  const { name, isTalking, sassyText, plantType, voice, daysSinceLastWatered } =
    usePlantSettings();
  const [isListening, setIsListening] = useState(false);
  const SpeechRecognition =
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition;

  useEffect(() => {
    if (isListening) {
      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onresult = (event: any) => {
        const text = event.results[0][0].transcript;
        console.log("user input: ", text);
        wsRef.current &&
          wsRef.current.send(
            JSON.stringify({
              type: "user_voice_message",
              text,
            }),
          );
      };
      recognition.onerror = (e: any) => {
        console.error("speech error", e);
      };
      recognition.start();
    }
  }, [isListening]);

  const toggleListening = () => {
    if (isListening) {
      // stopListening();
      setIsListening(false);
    } else {
      // startListening();
      setIsListening(true);
    }
  };

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
          <div className="sassy-text-detail">
            <div className="sassy-text-detail-title">watered:</div>
            <div className="sassy-text-detail-value">
              {daysSinceLastWatered} days ago
            </div>
          </div>
        </div>
      )}
      <div className="mic-button-wrapper">
        <button
          onClick={toggleListening}
          className={`mic-button ${isListening ? "listening" : ""} ${isTalking ? "plant-talking" : ""}`}
        ></button>
      </div>
      <div className="sassy-text-text">
        {sassyText && isTalking ? sassyText : ""}
      </div>
    </div>
  );
};

export default SassyText;
