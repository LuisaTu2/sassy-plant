import { useEffect, useRef, useState } from "react";
import { useChartSettings } from "../contexts/ChartSettingsContext";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import type { MessageType, PlantState, Audio } from "../types";
import { playAudioFromBase64 } from "../utils";
import "./ChartsDashboard.css";
import Controls from "./Controls";
import SensorsChart from "./SensorsChart";
import SassyText from "./SassyText";

const ChartsDashboard = () => {
  const { connected, data, setConnected, setData } = useChartSettings();
  const { setIsTalking, setSassyText } = usePlantSettings();
  const [isReading, setIsReading] = useState<boolean>(false);
  const MAX_POINTS = 300;
  const wsRef = useRef<WebSocket | null>(null);

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
        if (messageType === "reading") {
          const plantState = message["payload"] as PlantState;
          setData((prev) => [...prev.slice(-MAX_POINTS + 1), plantState]);
        } else {
          (async () => {
            setIsTalking(true);
            const text = message["payload"]["text"];
            console.log("text: ", text);
            setSassyText(text);
            await playAudioFromBase64((message.payload as Audio).audio);
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
      console.log("WebSocket closed on unmount");
    };
  }, []); // renders only once

  useEffect(() => {
    if (wsRef == null || wsRef.current == null) {
      return;
    }
    if (connected) {
      setIsReading(true);
      wsRef.current &&
        wsRef.current.send(
          JSON.stringify({
            type: "start_readings",
          }),
        );
    } else {
      if (isReading) {
        setIsReading(false);
        wsRef.current &&
          wsRef.current.send(
            JSON.stringify({
              type: "stop_readings",
            }),
          );
      }
    }
  }, [connected]);

  return (
    <div className="charts-dashboard">
      <div className="charts">
        <SassyText />
        <SensorsChart data={data} />
      </div>
      <Controls connected={connected} setConnected={setConnected} />
    </div>
  );
};

export default ChartsDashboard;
