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

  // this is understood to contain text and audio for talking
  const handlePlantStateChange = async (message: any, websocket: WebSocket) => {
    try {
      const payload = message["payload"];
      const eventType = payload["event"];
      handleEvent(eventType);

      const text = payload["text"];
      const audio = payload["audio"];

      // update text
      setSassyText(text);
      setIsTalking(true);

      // update audio
      await playAudioFromBase64(audio);

      // handle after talking
      setIsTalking(false);
      setSassyText("");

      // send notification that plant has stopped talking
      console.log("plant stopped talking");
      websocket.send(
        JSON.stringify({
          type: "stopped_talking",
        }),
      );
    } catch (error) {
      console.log("unable to handle plant state change: ", error);
    }
  };

  // this is understood to contain text and audio for talking
  const handlePlantStateChangeNoAudio = (message: any) => {
    try {
      const payload = message["payload"];
      const eventType = payload["event"];
      handleEvent(eventType);
      // TODO: handle animation
    } catch (error) {
      console.log("unable to handle plant state change: ", error);
    }
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
          handlePlantStateChange(message, webSocket);
        } else if (messageType === "state_change_no_audio") {
          handlePlantStateChangeNoAudio(message);
        } else if (messageType === "respond_to_human") {
          console.log("will be implementing here");
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
