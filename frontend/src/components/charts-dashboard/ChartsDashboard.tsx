import { useEffect } from "react";
import { useChartSettings } from "../contexts/ChartSettingsContext";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import type { MessageType, PlantState, Audio } from "../types";
import { playAudioFromBase64 } from "../utils";
import "./ChartsDashboard.css";
import Controls from "./Controls";
import SensorsChart from "./SensorsChart";

const ChartsDashboard = () => {
  const { connected, data, setConnected, setData } = useChartSettings();
  const { setIsTalking, setSassyText } = usePlantSettings();
  const MAX_POINTS = 200;

  const activateWebSocket = () => {
    const webSocket = new WebSocket(
      `${import.meta.env.VITE_API_WS_URL}/ws/sensors`,
    );

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
            console.log("she is done talking");
            webSocket.send(
              JSON.stringify({
                type: "voice_done",
              }),
            );

            setIsTalking(false);
          })();
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message:", err);
      }
    };
    webSocket.onerror = (e: Event) => console.error("WebSocket error:", e);
    webSocket.onclose = () => {
      console.log("WebSocket closed");
      setConnected(false);
    };

    return () => webSocket.close();
  };

  useEffect(() => {
    if (connected) {
      activateWebSocket();
    }
  }, [connected]);
  return (
    <div className="charts-dasboard">
      <SensorsChart data={data} />
      <Controls connected={connected} setConnected={setConnected} />
    </div>
  );
};

export default ChartsDashboard;
