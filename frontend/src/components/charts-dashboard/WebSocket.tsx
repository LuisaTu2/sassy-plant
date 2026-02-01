// import React, { useEffect, useRef } from "react";
// import type { MessageType, PlantState, Audio } from "../types";
// import { playAudioFromBase64 } from "../utils";
// import { useChartSettings } from "../contexts/ChartSettingsContext";
// import { usePlantSettings } from "../contexts/PlantSettingsContext";

// const WebSocketComponent = () => {
//   const socketRef: React.RefObject<WebSocket | null> = useRef(null);
//   const { connected, setConnected, setData } = useChartSettings();
//   const { setIsTalking, setSassyText } = usePlantSettings();

//   useEffect(() => {
//     // Open the WebSocket connection
//     if (connected) {
//       socketRef.current = new WebSocket(
//         `${import.meta.env.VITE_API_WS_URL}/ws/sensors`,
//       );

//       // Assign event listeners
//       socketRef.current.onopen = () => {
//         // setConnected(true);
//         console.log("WebSocket connection opened");
//       };

//       socketRef.current.onmessage = (event: MessageEvent) => {
//         try {
//           const message = JSON.parse(event.data);
//           const messageType: MessageType = message["type"];
//           if (messageType === "reading") {
//             const plantState = message["payload"] as PlantState;
//             setData((prev) => [...prev.slice(-300 + 1), plantState]);
//           } else {
//             (async () => {
//               setIsTalking(true);
//               const text = message["payload"]["text"];
//               console.log("text: ", text);
//               setSassyText(text);
//               await playAudioFromBase64((message.payload as Audio).audio);
//               console.log("she is done talking");
//               socketRef.current &&
//                 socketRef.current.send(
//                   JSON.stringify({
//                     type: "voice_done",
//                   }),
//                 );

//               setIsTalking(false);
//             })();
//           }
//         } catch (err) {
//           console.error("Failed to parse WebSocket message:", err);
//         }
//       };

//       // Handle the close event
//       socketRef.current.onclose = (event: Event) => {
//         // setConnected(false);
//         console.log("WebSocket connection closed:", event);
//       };

//       socketRef.current.onerror = (error: Event) => {
//         console.error("WebSocket error:", error);
//         // setConnected(false);
//       };
//     } else {
//       console.log("closing connection");

//       if (socketRef.current) {
//         socketRef.current.close(1000, "Manually disconnected");
//         socketRef.current = null;
//         console.log("WebSocket manually closed");
//       }
//       return;
//     }
//     // Cleanup function: closes the WebSocket when the component unmounts
//     // return () => {
//     //   if (
//     //     socketRef.current &&
//     //     socketRef.current.readyState === WebSocket.OPEN
//     //   ) {
//     //     socketRef.current.close(1000, "Component Unmount"); // Use close code 1000 for normal closure
//     //   }
//     // };
//   }, [connected]); // Reruns if the URL changes

//   return (
//     <div>
//       <p> is websocket connected: {connected}</p>
//       {/* Rest of your component UI */}
//     </div>
//   );
// };

// export default WebSocketComponent;
