# global manager
import asyncio
import datetime
import json
from collections import deque

import serial_asyncio


sensor_port = "/dev/ttyACM0"
sensor_baudrate = 9600


class SensorManager(asyncio.Protocol):
    def __init__(self):
        self.water_readings = deque()
        self.light_readings = deque()
        self.buffer = b""

        self.publish_data_point = lambda *args, **kwargs: None  # callback

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

        return

    def get_avg_light_reading(self):
        if not len(self.light_readings):
            return -1
        return sum(self.light_readings) / len(self.light_readings)

    def get_avg_water_reading(self):
        if not len(self.water_readings):
            return -1
        return sum(self.water_readings) / len(self.water_readings)


# lambda is used to specify instance of sensor manager as instantiated in here
async def start_serial_reader(sensor_manager: SensorManager):
    loop = asyncio.get_running_loop()
    await serial_asyncio.create_serial_connection(
        loop, lambda: sensor_manager, sensor_port, sensor_baudrate
    )
