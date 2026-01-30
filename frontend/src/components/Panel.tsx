import "./Panel.css";
import Controls from "./Controls";
import PlantStatePlot from "./PlantStatePlot";
import { useEffect, useState } from "react";
import { sampleData } from "./samples";
import type { PlantState, Message, MessageType, Audio } from "./types";

function playAudioFromBase64(b64: string) {
  const binary = atob(b64);
  const len = binary.length;
  const buffer = new Uint8Array(len);

  for (let i = 0; i < len; i++) {
    buffer[i] = binary.charCodeAt(i);
  }

  const blob = new Blob([buffer], { type: "audio/wav" });
  const url = URL.createObjectURL(blob);

  const audio = new Audio(url);
  audio.play();
}

const Panel: React.FC = () => {
  const [connected, setConnected] = useState<boolean>(false);
  const [data, setData] = useState<PlantState[]>(sampleData);
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
          if (messageType === "voice") {
            playAudioFromBase64((message.payload as Audio).audio);
          }
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
