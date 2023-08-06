import time
from time import sleep
from datetime import datetime
from typing import List
from pydantic import BaseModel, ValidationError

from settings import S

from src.arduino.arduino import ArduinoThread, ArduinoControl

class Message(BaseModel):
    timestamp: str
    sender: str
    command: str
    sensors: List[int] = list()
    leds: List[int] = list()


THRESHOLD = 0.2
SLEEP_SEC = 0.5
DEBUG = True
DEBUG = False

V_in = 1024
R_f = 10E+3
SCALE = 1E+6

def weight(sensor: int) -> float:
    return sensor/1024

def main():
    with ArduinoThread(port=S.ARDUINO_PATH) as arduino:
        arduino: ArduinoControl # NOT a ArduinoThread object!!!
        arduino.debug = DEBUG
        CONNECTION_MADE = arduino.read()
        print(f"{CONNECTION_MADE = }")
        # if CONNECTION_MADE != "CONNECTION_MADE":
        #     print(f"[ERROR] {CONNECTION_MADE = }")
            # return

        sleep(1)

        def get_respond():
            raw_respond = arduino.read()
            
            try:
                respond: Message = Message.model_validate_json(raw_respond)
            except ValidationError as e:
                return None
            respond.timestamp = datetime.now().isoformat()
            return respond
        
        def command(command, **kwarg):
            msg = Message(command=command, sender="server", timestamp=datetime.now().isoformat(), **kwarg)
            print(f"Send {msg = !r}")
            arduino.write_line(msg.model_dump_json())

        # arduino.write_line("Hello world")
        while True:
            if arduino.read() == r"{}": continue
            command("read_sensors")
            

            while True:
                sleep(SLEEP_SEC)
                read_sensors_respond = get_respond()
                if read_sensors_respond:
                    break

            # print(f"{read_sensors_respond!r}")
            sensors = [ int(SCALE * (V_in-V_out)/(V_out*R_f)) for V_out in read_sensors_respond.sensors]
            print(sensors)
            print()
            
            sleep(SLEEP_SEC)
            
            
            
            
            # leds = list()
            # for sensor in read_sensors_respond.sensors:
            #     leds.append(int(weight(sensor) > THRESHOLD))
            
            # command("write_leds", leds=leds)
            
            # sleep(SLEEP_SEC)

            # write_leds_respond = get_respond()
            # print(f"{write_leds_respond!r}")
            # print()
            # sleep(SLEEP_SEC)
            
            



if __name__ == "__main__":
    main()