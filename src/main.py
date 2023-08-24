# DONE Add debug mode
import argparse
# [argparse — Parser for command-line options, arguments and sub-commands — Python 3.11.4 documentation](https://docs.python.org/3.8/library/argparse.html#const)
# [Python argparse 用法與範例 | ShengYu Talk](https://shengyu7697.github.io/python-argparse/)

parser = argparse.ArgumentParser(description='Main function of the project of Google HPS 2023 Team 8. Created by Andrew Chiu.')
parser.add_argument('-d', '--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help="turn on debug mode (default: off); will set the logging level to 'DEBUG'")
parser.add_argument('-l', '--log', dest='log_level',
                    default="INFO", type=str,
                    help="set the logging level (default: 'INFO')")

args = parser.parse_args()

import os
os.environ["LOG_LEVEL"] = "DEBUG" if args.debug else args.log_level

import time
from time import sleep
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic_core import ValidationError
from settings import S, create_logger
log = create_logger(__file__, S.LOG_LEVEL)

from src.arduino.arduino import ArduinoThread, ArduinoControl


THRESHOLD = 2000
SLEEP_SEC = 0.2


USING_0th = False

V_in = 1024
R_f = 10E+3
SCALE = 1E+6
SLOTS_SIZE = 5

class Message(BaseModel):
    timestamp: str
    sender: str
    command: str
    sensors: List[Optional[int]] = list([None] * (SLOTS_SIZE+1))
    leds: List[Optional[int]] = list([None] * (SLOTS_SIZE+1)) # TODO 2 LEDs for each slot


def main():
    with ArduinoThread(port=S.ARDUINO_PORT) as arduino: # TODO What if arduino fails?
        arduino: ArduinoControl # NOT a ArduinoThread object!!!
        arduino.debug = S.DEBUG

        # TODO SERIAL MONITOR
        # TODO send Ctrl+C
        # FLUSH ANYTHING
        arduino.transport.serial.flush()
        arduino.buffer = bytearray()

        # [Step 1] Arduino responds that ARDUINO_IS_READY
        # [Step 2] Server waits until ARDUINO_IS_READY
        while True:
            # [Step 3] Server responds that SERVER_IS_READY
            if arduino.read() == "ARDUINO_IS_READY":
                arduino.write_line("SERVER_IS_READY")
                break
            else:
                log.info("Waiting for 'ARDUINO_IS_READY'...")
                sleep(SLEEP_SEC)
        
        # [Step 4] Arduino waits until server is ready
        # [Step 5] Server starts to send messages

        def get_respond(command):  # TODO very ugly
            raw_respond = arduino.read()
            log.info(f"{raw_respond = }")
            # Ignore the initial state
            if raw_respond == "ARDUINO_IS_READY":
                return None

            # Ignore the initial state
            if raw_respond == r"{}":
                return None

            # Ignore echos
            if raw_respond.startswith("[[ECHO]]"):
                return None
            # Ignore DEBUG
            if raw_respond.startswith("[["):
                return None

            try:
                respond: Message = Message.model_validate_json(raw_respond)
                if respond.command != command:
                    raise Exception(f"Expected {command = }")
            except Exception as e:
                log.info(f"{e !r}")
                return None
            respond.timestamp = datetime.now().isoformat()
            return respond
        
        def command(command, **kwarg):
            log.info(f"{command = }")
            msg = Message(command=command, sender="server", timestamp=datetime.now().isoformat(), **kwarg)
            arduino.write_line(msg.model_dump_json())

        while True:

            command("read_sensors")
            while True:
                sleep(SLEEP_SEC)
                read_sensors_respond = get_respond("read_sensors")
                if read_sensors_respond:
                    break

            log.info(f"{read_sensors_respond!r}")
            sensors = [int(SCALE * (V_in-V_out)/(V_out*R_f)) 
                       for V_out in read_sensors_respond.sensors]
            
            if not USING_0th: sensors[0] = None # Not used
            log.debug(f"{sensors = }")
            sleep(SLEEP_SEC)

            def threshold(sensor: int) -> int:
                if sensor is None:
                    return None
                else:
                    return int(sensor > THRESHOLD)

            leds = list(map(threshold, sensors))
            if not USING_0th: leds[0] = None # Not used


            command("write_leds", leds=leds)            
            while True:
                sleep(SLEEP_SEC)
                write_leds_respond = get_respond("write_leds")
                if write_leds_respond:
                    log.info(f"{write_leds_respond!r}")
                    break

            log.debug(f"{write_leds_respond.leds = }")

            sleep(SLEEP_SEC)




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception(e)