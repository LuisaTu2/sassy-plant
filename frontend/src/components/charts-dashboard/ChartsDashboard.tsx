import { useEffect, useRef } from "react";
import { useChartSettings } from "../contexts/ChartSettingsContext";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import type { EventType, MessageType, PlantState } from "../types";
import { playAudioFromBase64 } from "../utils";
import "./ChartsDashboard.css";
import SensorsChart from "./SensorsChart";
import SassyText from "./SassyText";

const ChartsDashboard = () => {
  const { data, setData } = useChartSettings();
  const { setIsTalking, setSassyText, setDaysSinceLastWatered, setEvent } =
    usePlantSettings();
  const MAX_POINTS = 300;

  const wsRef = useRef<WebSocket | null>(null);

  const handleEvent = (eventType: EventType) => {
    if (eventType == "watering") {
      setDaysSinceLastWatered(0);
    }
    setEvent(eventType);
  };

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
        } else if (messageType === "state_change") {
          (async () => {
            setIsTalking(true);
            const payload = message["payload"];
            const text = payload["text"];
            const eventType = payload["event"];
            handleEvent(eventType);
            setSassyText(text);
            await playAudioFromBase64(payload["audio"]);
            console.log("stopped talking");
            webSocket.send(
              JSON.stringify({
                type: "stopped_talking",
              }),
            );

            setIsTalking(false);
            setEvent(null);
            // TODO: stop animation
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

  return (
    <div className="charts-dashboard">
      <div className="charts">
        <SassyText wsRef={wsRef} />
        <SensorsChart data={data} />
      </div>
    </div>
  );
};

export default ChartsDashboard;
