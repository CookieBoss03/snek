#!/bin/false

class CallbackInterface:
    def send(self, *args):
        raise NotImplementedError()
        #assert len(args) > 0
        #self.send_bin(b'|'.join(arg.encode() for arg in args))

    def log(self, *args):
        raise NotImplementedError()

    def die(self):
        raise NotImplementedError()

    def join(self, username, password):
        self.send("join", username, password)

    def chat(self, message):
        self.send("chat", message)

    def move(self, dir_str):
        self.send("move", dir_str)


class Logic:
    def __init__(self, username, password, callbacks):
        self.username = username
        self.password = password
        self.callbacks = callbacks

    def digest(self, cmd, args):
        if cmd == "motd":
            self.callbacks.log("motd", args)
            self.callbacks.join(self.username, self.password)
            self.callbacks.chat("ohai")
        elif cmd == "error":
            self.callbacks.log("Server reports error", *args)
            self.callbacks.die()
        elif cmd == "game":  # width, height, own_id
            self.callbacks.log("not impl", *args)
        elif cmd == "pos":  # id, x, y
            self.callbacks.log("not impl", *args)
        elif cmd == "tick":  # no-arg
            self.callbacks.log("not impl", *args)
        elif cmd == "die":  # all ids that died
            self.callbacks.log("not impl", *args)
        elif cmd == "message":  # id, message
            self.callbacks.log("not impl", *args)
        elif cmd == "win":  # numwins, numlosses
            self.callbacks.log("not impl", *args)
        elif cmd == "lose":  # numwins, numlosses
            self.callbacks.log("not impl", *args)
        else:
            self.callbacks.log("unknown packet type?!", *args)
            self.callbacks.die()
