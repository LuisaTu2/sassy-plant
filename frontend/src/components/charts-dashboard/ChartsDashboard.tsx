import { useEffect, useRef, useState } from "react";
import { useChartSettings } from "../contexts/ChartSettingsContext";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import type { MessageType, PlantState } from "../types";
import { playAudioFromBase64 } from "../utils";
import "./ChartsDashboard.css";
import SensorsChart from "./SensorsChart";
import SassyText from "./SassyText";

const ChartsDashboard = () => {
  const { data, setData } = useChartSettings();
  const { setIsTalking, setSassyText } = usePlantSettings();
  // const [isReading, setIsReading] = useState<boolean>(false);
  const MAX_POINTS = 300;
  const wsRef = useRef<WebSocket | null>(null);

  const [isListening, setIsListening] = useState(false);
  const SpeechRecognition =
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition;

  useEffect(() => {
    wsRef.current = new WebSocket(
      `${import.meta.env.VITE_API_WS_URL}/ws/sensors`,
    );
    const webSocket = wsRef.current;
    webSocket.onopen = () => console.log("Connected to WebSocket server");
    webSocket.onmessage = (event: MessageEvent) => {
      try {
        const message = JSON.parse(event.data);
        const messageType: MessageType = message["type"];
        if (messageType === "data_point") {
          const plantState = message["payload"] as PlantState;
          setData((prev) => [...prev.slice(-MAX_POINTS + 1), plantState]);
        } else {
          (async () => {
            setIsTalking(true);
            const payload = message["payload"];
            const text = payload["text"];
            setSassyText(text);
            await playAudioFromBase64(payload["audio"]);
            console.log("stopped talking");
            webSocket.send(
              JSON.stringify({
                type: "stopped_talking",
              }),
            );

            setIsTalking(false);
          })();
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message:", err);
      }
    };

    return () => {
      webSocket.close();
      console.log("websocket closed on unmount");
    };
  }, []); // renders only once

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
        console.error("Speech error", e);
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
    <div className="charts-dashboard">
      <div className="charts">
        <SassyText />
        <SensorsChart data={data} />
      </div>
      <button
        onClick={toggleListening}
        className={`mic-button ${isListening ? "talking" : ""}`}
      ></button>
    </div>
  );
};

export default ChartsDashboard;
