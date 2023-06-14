from logic import CallbackInterface

class Snek:
    mapWidth = 0
    mapHeight = 0
    callbacks = CallbackInterface()

    def HandleMotd(self, mapWidth, mapHeight):
        self.callbacks.move("down")

    
