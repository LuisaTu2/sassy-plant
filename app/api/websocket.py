import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.sensor_manager import SensorManager

# from domain.utils import simulate_and_send_readings
# from domain.sensor_readings import get_water_and_light_reading

router = APIRouter()


# async def send_audio(response, ws):
#     audio_bytes = response.read()  # WAV bytes
#     audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
#     message: AudioMessage = {
#         "type": MessageType.AUDIO.value,
#         "payload": {"audio": audio_b64, "format": AudioType.WAV.value},
#     }
#     await ws.send_text(json.dumps(message))


# is_talking = False
# is_reading = False


# async def receiver(ws: WebSocket):
#     global is_talking
#     global is_reading
#     while True:
#         msg = await ws.receive_text()
#         data = json.loads(msg)

#         if data["type"] == "voice_done":
#             print("\n\n\n received done talking notification \n\n\n")
#             is_talking = False

#         if data["type"] == "get_readings":
#             print("start readings")
#             is_reading = True
#             await handle_readings(ws)

#         if data["type"] == "stop_readings":
#             print("\n\n\n\nstop readings\n\n\n\n")
#             is_reading = False

#         if data["type"] == "disconnect":
#             print("received disconnect notification ")
#             is_talking = False
#             await ws.close(1000, "client disconnected")


# async def plant_talks(
#     llm_client,
#     ws: WebSocket,
#     state_change: StateChange,
# ):

#     # print("PLANT TALKS: ", water_state_1, water_state_2, should_comment_on_water, should_comment_on_light)
#     text = await asyncio.to_thread(llm_client.get_sassy_answer, state_change)
#     print(text)

#     audio_b64 = await asyncio.to_thread(llm_client.get_audio, text)
#     await ws.send_text(
#         json.dumps(
#             {
#                 "type": "voice",
#                 "payload": {
#                     "audio": audio_b64,
#                     "format": AudioType.WAV.value,
#                     "text": text,
#                 },
#             }
#         )
#     )


# async def handle_readings(ws: WebSocket):
#     # global is_talking
#     # global is_reading

#     moisture_readings = deque()
#     light_readings = deque()
#     print("\n\n\nNEW BATCH: ")
#     for t in range(200):
#         global is_reading
#         global is_talking
#         print("is talking?? ", t, is_talking, is_reading)
#         if not is_reading:
#             return
#         moisture_reading, light_reading = await get_water_and_light_reading(ws, t)
#         moisture_readings.append(moisture_reading)
#         light_readings.append(light_reading)

#         if len(moisture_readings) >= 5:
#             state_change = get_state_changes(moisture_readings, light_readings)

#             # maybe, record in database
#             if not is_talking and (
#                 state_change.has_water_state_changed
#                 or state_change.has_light_state_changed
#             ):
#                 print("\n\nplant wants to talk\n\n")
#                 is_talking = True
#                 asyncio.create_task(
#                     plant_talks(
#                         llm_client=llm_client,
#                         ws=ws,
#                         state_change=state_change,
#                     )
#                 )
#             moisture_readings.popleft()
#             light_readings.popleft()

#         await asyncio.sleep(0.1)


# @router.websocket("/ws/sensors")
# async def websocket_endpoint(ws: WebSocket):
#     try:
#         global is_talking

#         await ws.accept()
#         asyncio.create_task(receiver(ws))
#         print("connection established ")
#         # await handle_readings(ws)
#         await asyncio.sleep(10)

#     except Exception as e:
#         # optionally notify frontend
#         # await ws.send_text(json.dumps({"type": "error", "payload": {"message": str(e)}}))
#         raise Exception("unable to send voice audio: ", e)

sensor_manager = SensorManager()


@router.websocket("/ws/sensors")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    sensor_manager.clients.append(ws)

    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("type") == "start_readings":
                if not sensor_manager.reading_active:
                    print("start readings")
                    asyncio.create_task(sensor_manager.start_readings())
            elif msg.get("type") == "stop_readings":
                print("stop readings")
                await sensor_manager.stop_readings()
            elif msg.get("type") == "stopped_talking":
                sensor_manager.is_talking = False
    except WebSocketDisconnect:
        sensor_manager.clients.remove(ws)
        print("Client disconnected")
