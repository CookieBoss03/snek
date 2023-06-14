#!/bin/false
import numpy as np
import random as rd
from game import Helpers
class CallbackInterface:
    def send(self, *args):       
        assert len(args) > 0
        self.send_bin(b'|'.join(arg.encode() for arg in args))

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
        self.snek = Snek(callbacks)
        self.bots = []


    def digest(self, cmd, args):
        if cmd == "motd":
            self.callbacks.log("motd", args)
            self.callbacks.join(self.username, self.password)
            self.snek.HandleMotd()
            # self.callbacks.move("left")
        elif cmd == "player":
            self.snek.HandlePlayer(args)
        elif cmd == "error":
            self.callbacks.log("Server reports error", *args)
            self.callbacks.die()
        elif cmd == "game":  # width, height, own_id
            self.callbacks.log("game", *args)
            self.snek.HandleGame(args)
        elif cmd == "pos":  # id, x, y
            self.callbacks.log("pos", *args)
            self.snek.HandlePos(args)
            if int(args[0]) == self.snek.bots[-1]:
                self.snek.HandleEndOfInfo()
        elif cmd == "tick":  # no-arg
            self.callbacks.log("tick", *args)
            self.snek.HandleTick()
        elif cmd == "die":  # all ids that died
            self.callbacks.log("die", *args)
            self.snek.HandleDeath(args)
        elif cmd == "message":  # id, message
            self.callbacks.log("message", *args)
            self.snek.HandleMessage(args)
        elif cmd == "win":  # numwins, numlosses
            self.callbacks.log("win", *args)
            self.snek.HandleWin()
        elif cmd == "lose":  # numwins, numlosses
            self.callbacks.log("lose", *args)
        else:
            self.callbacks.log("unknown packet type?!", *args)
            self.callbacks.die()

class Snek:
    def __init__(self, callbacks):
        self.callbacks = callbacks
        self.bots = []
        self.chosenDirection = "down"
        self.chosenMessage = "Hello bissame!"
        self.helpers = Helpers()
        
    def Reset(self):
        self.bots = []

    def HandlePlayer(self, args):
        id = int(args[0])
        self.bots.append(id)
        self.lastPositions.__setitem__(id, -1)

    def HandleMessage(self, args):
        id = args[0]
        msg = args[1]
        if(id != self.id):
            self.callbacks.chat("Hey " + id +", Que te caillas!")

    
    def HandleWin(self):
        self.callbacks.chat("You dont even come close to me, you dirty little rats!")

    def HandleMotd(self):
        NotImplemented

    def SendMessage(self):
        if self.chosenMessage != "":
            self.callbacks.chat(self.chosenMessage)
        self.chosenMessage = ""

    def HandleGame(self, args):
        self.Reset()
        self.id = int(args[2])
        self.mapWidth = int(args[0])
        self.mapHeight = int(args[1])
        self.positions = np.full((self.mapWidth, self.mapHeight), -1)    
        self.dangers = np.full((self.mapWidth, self.mapHeight), 0) 
        self.lastPositions = dict()

    def HandlePos(self, args):
        id = int(args[0])
        x = int(args[1])
        y = int(args[2])
        #update danger Matrix:
        if self.lastPositions[id] != -1:
            for pos in self.GetAdjacentCells(self.lastPositions[id]):
                self.dangers[pos[0], pos[1]] -= 2
        for pos in self.GetAdjacentCells((x,y)):
            self.dangers[pos[0], pos[1]] += 3
        #update position matrix and last position
        self.positions[x, y] = id
        self.lastPositions[id] = (x,y)
    
    def HandleTick(self):
        self.helpers.visualizeMatrix((self.dangers, self.positions), "dangerMap.txt", True)
        self.callbacks.move(self.chosenDirection)


    def HandleEndOfInfo(self):
        #calculate next move
        newDirection = self.ChooseDirection()
        if newDirection != "":
            self.chosenDirection = newDirection;
        #say next message
        self.SendMessage()

    def HandleDeath(self, ids : list):
        self.callbacks.chat("Hahaha you noobs!")
        for id in ids:
            if self.bots.__contains__(int(id)):
                
                self.bots.remove(int(id))
        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                if ids.__contains__(str(self.positions[x,y])):
                    self.positions[x,y] = -1
        


    def ChooseDirection(self):
        availableCells = []
        for pos in self.GetAdjacentCells(self.lastPositions[self.id]):
            if self.positions[pos[0], pos[1]] == -1:
                availableCells.append(pos)
        if(availableCells == []):
            self.chosenMessage = "Stepbro I'm stuck!"
            return ""
        #choose best available cell
        chosenCell = rd.choice(availableCells)
        for pos in availableCells:
            if(self.GetDanger(pos) < self.GetDanger(chosenCell)):
                chosenCell = pos
        
        chosenDirection = self.CellToDirection(self.lastPositions[self.id], chosenCell)
        return chosenDirection

    def GetDanger(self, pos):
        return self.dangers[pos[0], pos[1]]

    def GetAdjacentCells(self, pos):
        return [((pos[0] + 1)%self.mapWidth, pos[1]),((pos[0] - 1)%self.mapWidth, pos[1]),(pos[0], (pos[1] + 1)%self.mapHeight),(pos[0], (pos[1] - 1)%self.mapHeight)]

    def CellToDirection(self, posFrom, posTo):
        if((posFrom[0] + 1)%self.mapWidth == posTo[0]): return "right"
        elif ((posFrom[0] - 1)%self.mapWidth == posTo[0]): return "left"
        elif ((posFrom[1] + 1)%self.mapHeight == posTo[1]): return "down"
        elif ((posFrom[1] - 1)%self.mapHeight == posTo[1]): return "up"
        else :
            return "up"
