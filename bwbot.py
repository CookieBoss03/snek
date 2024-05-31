#!/usr/bin/env python3

import asyncio
import logic
#import secret  # username, password
import time


HOST = "151.216.74.213"
PORT = 4000
TIME_START = time.time()

PASSWORD = "wieso"
USERNAME = "Ser Leo, Warden of Alsacia"

def timestamp():
    return f"[{time.time() - TIME_START:9.3f}]"


class PhysicalCallbackInterface(logic.CallbackInterface):
    def __init__(self, writer):
        self.writer = writer

    def send(self, *args):
        assert len(args) > 0
        args_string = '|'.join(arg for arg in args)
        print(f"OO {timestamp()} {args_string.replace(PASSWORD,'PASSWORD')}")
        self.writer.write(args_string.encode() + b"\n")

    def log(self, *args):
        print(f"== {timestamp()} {args}")

    def die(self):
        print(f"XX {timestamp()} yolo, now ded")



async def main():
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    try:
        phys_interface = PhysicalCallbackInterface(writer)
        game = logic.Logic(USERNAME, PASSWORD, phys_interface)
        while True:
            line_bytes = await reader.readline()
            line = line_bytes.decode(errors="replace").rstrip("\n")
            print(f"II {timestamp()} >{line}<")

            if not line:
                print("Closing connection, empty line received")
                raise ConnectionError("Empty line received")


            parts = line.split("|")
            game.digest(parts[0], parts[1:])
            await writer.drain()
    finally:
        # Close the connection
        writer.close()
        await writer.wait_closed()
        print("Closing connection, program finished")


if __name__ == "__main__":
    asyncio.run(main())
