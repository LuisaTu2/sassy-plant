import "./Panel.css";
import Controls from "./Controls";
import PlantStatePlot from "./PlantStatePlot";
import { useEffect, useState } from "react";
import { sampleData } from "./samples";
import type { Point } from "./types";

const Panel: React.FC = () => {
  const [connected, setConnected] = useState<boolean>(false);
  const [data, setData] = useState<Point[]>(sampleData);
  const MAX_POINTS = 200;

  const activateWebSocket = () => {
    const webSocket = new WebSocket(
      `${import.meta.env.VITE_API_WS_URL}/ws/sensors`,
    );

    webSocket.onopen = () => console.log("Connected to WebSocket server");
    webSocket.onmessage = (event: MessageEvent) => {
      try {
        const point: Point = JSON.parse(event.data);
        setData((prev) => [...prev.slice(-MAX_POINTS + 1), point]);
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
    if (!connected) return;
    activateWebSocket();
  }, [connected]);

  return (
    <div className="panel">
      <PlantStatePlot data={data} />
      <Controls connected={connected} setConnected={setConnected} />
    </div>
  );
};

export default Panel;
