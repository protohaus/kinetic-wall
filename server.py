#!/usr/bin/env python3

import asyncio
import json
import traceback
from typing import List, Optional

import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Phidget import *
from Phidget22.PhidgetException import *

PORT = 9876  # Port to listen on (non-privileged ports are > 1023)


class PhidgetController:
    def __init__(self, channel: int):
        self.io = DigitalOutput()
        self.queue = asyncio.Queue()
        self._io_handler_task: Optional[asyncio.Task] = None

        # Set addressing parameters to specify which channel to open (if any)
        self.io.setChannel(channel)
        # Assign any event handlers you need before calling open so that no events are missed.
        self.io.setOnAttachHandler(self.onAttach)
        self.io.setOnDetachHandler(self.onDetach)
        self.io.setOnErrorHandler(self.onError)
        # Open your Phidgets and wait for attachment
        self.io.openWaitForAttachment(5000)

    async def start(self):
        try:
            while True:
                command = await self.queue.get()
                if self._io_handler_task:
                    self._io_handler_task.cancel()
                if command["mode"] == "end":
                    break
                self._io_handler_task = asyncio.get_event_loop().create_task(
                    self._io_handler(command)
                )
        finally:
            print("Closing phidget")
            try:
                self.io.setDutyCycle(0)
                self.io.close()
            except PhidgetException:
                print("device not connected")
            # if self._io_handler_task:
            #     self._io_handler_task.cancel()

    async def _io_handler(self, command: dict):
        print(command)
        try:
            if command["mode"] == "wave":
                phase_s = (1 / command["frequency_hz"]) / 2
                while True:
                    self.io.setDutyCycle(0)
                    await asyncio.sleep(phase_s)
                    self.io.setDutyCycle(1)
                    await asyncio.sleep(phase_s)
            if command["mode"] == "pwm":
                period_s = 1 / command["frequency_hz"]
                on_phase_s = command["duty_cycle"] * period_s
                off_phase_s = period_s - on_phase_s
                while True:
                    self.io.setDutyCycle(0)
                    await asyncio.sleep(on_phase_s)
                    self.io.setDutyCycle(1)
                    await asyncio.sleep(off_phase_s)
            if command["mode"] == "off":
                self.io.setDutyCycle(0)
                while True:
                    await asyncio.sleep(3600)
            if command["mode"] == "on":
                self.io.setDutyCycle(1)
                while True:
                    await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass

    @staticmethod
    def onAttach(io):
        print("Attach [" + str(io.getChannel()) + "]!")

    @staticmethod
    def onDetach(io):
        print("Detach [" + str(io.getChannel()) + "]!")

    @staticmethod
    def onError(io, code, description):
        print("Code [" + str(io.getChannel()) + "]: " + ErrorEventCode.getName(code))
        print("Description [" + str(io.getChannel()) + "]: " + str(description))
        print("----------")


phidgets: List[PhidgetController] = []


async def echo(websocket, path):
    try:
        async for message in websocket:
            command = json.loads(message)
            for i in phidgets:
                await i.queue.put(command)
            await websocket.send(message)
    except ConnectionClosedOK:
        print("Normally closing connection")
    except ConnectionClosedError:
        print("Abnormal connection close")


def main() -> None:
    loop = asyncio.get_event_loop()

    try:
        for i in range(4):
            # Create your Phidget channels
            controller = PhidgetController(i)
            phidgets.append(controller)
    except PhidgetException as ex:
        traceback.print_exc()
        print("")
        print(f"PhidgetException {ex.code} ({ex.description}): {ex.details}")
        exit(1)

    coroutines = [i.start() for i in phidgets]
    coroutines.append(websockets.serve(echo, "0.0.0.0", PORT))
    try:
        gather = asyncio.gather(*coroutines)
        loop.run_until_complete(gather)
    except KeyboardInterrupt:
        print("Shutting down")
        gather.cancel()
        loop.close()


if __name__ == "__main__":
    main()
