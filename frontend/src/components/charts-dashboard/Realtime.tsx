// ADD THIS TO CHARTSDASHBOARD FOR REALTIME

// const pcRef = useRef<RTCPeerConnection | null>(null);
// const audioEl = useRef<HTMLAudioElement | null>(null);

// const handleWebRTC = async () => {
//   try {
//     const session = await getRealtimeSession();
//     // console.log("session: ", session);
//     const ephemeralKey = session.client_secret.value;

//     // create a new rtc peer connection
//     const pc = new RTCPeerConnection();
//     pcRef.current = pc;

//     // add a micophone
//     const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//     stream.getTracks().forEach((track) => pc.addTrack(track, stream));

//     // data channel for events with openai websocket
//     const dc = pc.createDataChannel("oai-events");
//     dc.onmessage = (event) => {
//       // const d = event.data;
//       const data = JSON.parse(event.data);
//       console.log("event from realtime openai api:", data["type"]);
//     };

//     dc.onopen = () => {
//       console.log("data channel open, telling plant to speak...");
//     };

//     // create local sdp offer
//     const offer = await pc.createOffer();
//     await pc.setLocalDescription(offer);

//     // send offer to openai realtime api
//     const baseUrl = "https://api.openai.com/v1/realtime";
//     const model = "gpt-realtime"; // same as in ephemeral session

//     const sdpResponse = await fetch(`${baseUrl}?model=${model}`, {
//       method: "POST",
//       body: offer.sdp,
//       headers: {
//         Authorization: `Bearer ${ephemeralKey}`,
//         "Content-Type": "application/sdp",
//       },
//     });

//     const answerSdp = await sdpResponse.text();

//     console.log("PC: ", pc);

//     if (!audioEl.current) {
//       audioEl.current = document.createElement("audio");
//       audioEl.current.autoplay = true;
//       audioEl.current.controls = true;
//       document.body.appendChild(audioEl.current);
//     }

//     // receive audio from open ai
//     pc.ontrack = (event) => {
//       for (const stream of event.streams) {
//         if (!audioEl.current) return;
//         audioEl.current.srcObject = stream;
//         audioEl.current
//           .play()
//           .then(() => console.log("Playing stream:", stream))
//           .catch((err) => console.error("Play failed:", err));
//       }

//       // console.log("Incoming track:", event.track);
//     };

//     await pc.setRemoteDescription({ type: "answer", sdp: answerSdp });
//   } catch (error) {
//     console.log("error while handling webRC connection: ", error);
//   }
// };

// async function getRealtimeSession() {
//   const response = await fetch("http://localhost:9000/session", {
//     method: "POST",
//   });

//   if (!response.ok) {
//     throw new Error("Failed to fetch realtime session");
//   }
//   const session = await response.json();
//   return session;
// }

// useEffect(() => {
//   handleWebRTC();
// }, []);
