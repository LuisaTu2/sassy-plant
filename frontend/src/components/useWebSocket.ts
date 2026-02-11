import { useEffect, useRef } from "react";
import { useChartSettings } from "./contexts/ChartSettingsContext";
import { usePlantSettings } from "./contexts/PlantSettingsContext";
import type { EventType, MessageType, PlantState } from "./types";

const playAudioFromBase64 = (b64: string): Promise<void> => {
  const binary = atob(b64);
  const len = binary.length;
  const buffer = new Uint8Array(len);

  for (let i = 0; i < len; i++) {
    buffer[i] = binary.charCodeAt(i);
  }

  const blob = new Blob([buffer], { type: "audio/wav" });
  const url = URL.createObjectURL(blob);

  return new Promise((resolve) => {
    const audio = new Audio(url);
    audio.play();
    audio.onended = () => resolve();
  });
};

export const useWebSocket = () => {
  const wsRef = useRef<WebSocket | null>(null);

  const { setData } = useChartSettings();
  const { setIsTalking, setSassyText, setDaysSinceLastWatered, setEvent } =
    usePlantSettings();

  const handleEvent = (eventType: EventType) => {
    if (eventType == "watering") {
      setDaysSinceLastWatered(0);
    }
    setEvent(eventType);
  };

  const handlePlantStateChange = async (message: any) => {
    try {
      const payload = message["payload"];
      const eventType = payload["event"];
      handleEvent(eventType);
      const text = payload["text"];
      const audio = payload["audio"];

      handleTalking(text, audio);
    } catch (error) {
      console.log("unable to handle plant state change: ", error);
    }
  };

  const handlePlantStateChangeNoAudio = (message: any) => {
    try {
      const payload = message["payload"];
      const eventType = payload["event"];
      handleEvent(eventType);
    } catch (error) {
      console.log("unable to handle plant state change: ", error);
    }
  };

  const handleResponseToHuman = async (message: any) => {
    try {
      const payload = message["payload"];
      const text = payload["text"];
      const audio = payload["audio"];
      handleTalking(text, audio);
    } catch (error) {
      console.log("unable to handle plant state change: ", error);
    }
  };

  const handleTalking = async (text: string, audio: string) => {
    try {
      // update text
      setSassyText(text);
      setIsTalking(true);

      // update audio
      await playAudioFromBase64(audio);

      // handle after talking
      setIsTalking(false);
      setSassyText("");
      console.log("plant stopped talking");
      sendWsMessage("stopped_talking", "");
    } catch (error) {
      console.log("unable to handle plant state change: ", error);
    }
  };

  const handleWebsocketMsg = (event: MessageEvent) => {
    try {
      const MAX_POINTS = 300;

      const message = JSON.parse(event.data);
      const messageType: MessageType = message["type"];
      if (messageType === "data_point") {
        const plantState = message["payload"] as PlantState;
        setData((prev) => [...prev.slice(-MAX_POINTS + 1), plantState]);
      } else if (messageType === "state_change") {
        handlePlantStateChange(message);
      } else if (messageType === "state_change_no_audio") {
        handlePlantStateChangeNoAudio(message);
      } else if (messageType === "respond_to_human") {
        handleResponseToHuman(message);
      }
    } catch (err) {
      console.error("Failed to parse WebSocket message:", err);
    }
  };

  const sendWsMessage = (msgType: string, msg: string) => {
    try {
      console.log("sending message: ", msgType, msg);
      wsRef.current &&
        wsRef.current.send(
          JSON.stringify({
            type: msgType,
            text: msg,
          }),
        );
    } catch (error) {
      console.log("unable to handle plant state change: ", error);
    }
  };

  useEffect(() => {
    wsRef.current = new WebSocket(
      `${import.meta.env.VITE_API_WS_URL}/ws/sensors`,
    );

    const webSocket = wsRef.current;
    webSocket.onopen = () => {
      console.log("connected to websocket server");
    };
    webSocket.onmessage = (event: MessageEvent) => {
      handleWebsocketMsg(event);
    };

    return () => {
      webSocket.close();
      console.log("websocket closed on unmount");
    };
  }, []);
  return { sendWsMessage };
};
