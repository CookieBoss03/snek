#!/usr/bin/env python3

import asyncio
import logic
import secret  # username, password


HOST = "gpn-tron.duckdns.org"
PORT = 4000


class PhysicalCallbackInterface(logic.CallbackInterface):
    def __init__(self, writer):
        self.writer = writer

    def send(self, *args):
        assert len(args) > 0
        args_string = '|'.join(arg for arg in args)
        print(f"OO {args_string.replace(secret.PASSWORD, 'PASSWORD')}")
        self.writer.write(args_string.encode() + b"\n")

    def log(self, *args):
        print(f"== {args}")

    def die(self):
        print(f"yolo, now ded")
        exit(1)


async def main():
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    phys_interface = PhysicalCallbackInterface(writer)
    game = logic.Logic(secret.USERNAME, secret.PASSWORD, phys_interface)
    while True:
        line_bytes = await reader.readline()
        line = line_bytes.decode(errors="replace").rstrip("\n")
        print(f"II >{line}<")
        parts = line.split("|")
        game.digest(parts[0], parts[1:])
        await writer.drain()


if __name__ == "__main__":
    asyncio.run(main())
