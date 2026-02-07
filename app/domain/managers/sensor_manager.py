# global manager
import asyncio
import datetime
import json
from collections import deque

import serial_asyncio

from domain.types import LightState
from domain.utils import (
    sensor_baudrate,
    sensor_port,
)


class SensorManager(asyncio.Protocol):
    def __init__(self):
        self.water_readings = deque()
        self.light_readings = deque()
        self.light_states = deque()
        self.current_light_state: LightState | None = None
        self.buffer = b""
        self.publish_data_point = lambda *args, **kwargs: None  # callback
        self.make_plant_talk_on_state_change = lambda *args, **kwargs: None

    def connection_made(self, transport):
        self.transport = transport
        print("successfully connected to sensor\n")

    # automatically runs when serial data is received
    def data_received(self, data):
        self.buffer += data

        # check if there’s a full line (ending with \n)
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            line_str = line.decode().strip()
            if line_str:
                try:
                    data = json.loads(line_str)
                    self.handle_data(data=data)
                except json.JSONDecodeError:
                    print("malformed JSON, skipping:", line_str)

    def handle_data(self, data: dict):
        timestamp = datetime.datetime.now()

        # publish data to frontend
        self.publish_data_point(data, timestamp)

        self.water_readings.append(int(data["water"]))
        self.light_readings.append(int(data["light"]))
        if len(self.water_readings) >= 6:
            self.water_readings.popleft()
            self.light_readings.popleft()
        if timestamp.second % 5 == 0:
            new_state = self.get_updated_state()
            if self.current_light_state is None:
                self.current_light_state = new_state
                return
            if new_state != self.current_light_state:
                asyncio.create_task(
                    self.make_plant_talk_on_state_change(
                        light_state=self.current_light_state,
                        new_light_state=new_state,
                    )
                )
                self.current_light_state = new_state

    def get_updated_state(
        self,
    ):
        average_light_value = sum(self.light_readings) / len(self.light_readings)
        # print("average light value: ", average_light_value)
        return self.light_to_state_mapping(average_light_value)

    def light_to_state_mapping(self, light):
        match light:
            case light if light < 200:
                return LightState.DARK.value
            case light if 200 <= light < 700:
                return LightState.AMBIENT.value
            case light if light >= 700:
                return LightState.BRIGHT.value


# lambda is used to specify instance of sensor manager as instantiated in here
async def start_serial_reader(sensor_manager: SensorManager):
    loop = asyncio.get_running_loop()
    await serial_asyncio.create_serial_connection(
        loop, lambda: sensor_manager, sensor_port, sensor_baudrate
    )
