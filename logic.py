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
        self.snek = Snek2(callbacks)
        self.bots = []


    def digest(self, cmd, args):
        if cmd == "motd":
            self.callbacks.log("motd", args)
            self.callbacks.join(self.username, self.password)
            self.snek.HandleMotd()
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


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = np.full((width, height), -1)
    
    def setTile(self, pos, id):
        self.map[pos[0], pos[1]] = id
    
    def getTile(self, pos):
        if pos == None or pos == -1:
            print('ERROR: pos is None (in getTile)')
            return None
        print("Pos: ", pos)
        return self.map[pos[0]% self.width, pos[1]% self.height]
    
    def removePlayer(self, id):
        for x in range(self.width):
            for y in range(self.height):
                if self.map[x, y] == id:
                    self.map[x, y] = -1
    
    def isFree(self, pos):
        return self.getTile(pos) == -1
    
    def getUpTile(self, pos):
        return self.getTile((pos[0], pos[1] - 1))
    
    def getDownTile(self, pos):
        return self.getTile((pos[0], pos[1] + 1))
    
    def getLeftTile(self, pos):
        return self.getTile((pos[0] - 1, pos[1]))
    
    def getRightTile(self, pos):
        return self.getTile((pos[0] + 1, pos[1]))

    def printMapToFile(self):
        with open("map.txt", "w") as file:
            for y in range(self.height):
                for x in range(self.width):
                    id = self.map[x, y]
                    if id == -1:
                        file.write(".")
                    else:
                        file.write(str(id))
                file.write("\n")

class Player:
    def __init__(self, id, name, map):
        self.id = id
        self.name = name
        self.map = map
        self.pos = None
    
    def updatePosition(self, pos):
        self.pos = pos
        self.map.setTile(pos, self.id)
    
    def die(self):
        self.pos = None
        self.map.removePlayer(self.id)
        self.dead = True

class Snek2:
    def __init__(self, callbacks):
        self.game_running = False
        self.callbacks = callbacks
        self.chosenMessage = None
        self.players = []
        for i in range(100):
            self.players.append(None)
        
    def Reset(self):
        self.players = []
        for i in range(100):
            self.players.append(None)

    def HandlePlayer(self, args):
        id = int(args[0])
        name = args[1]
        self.players[id] = Player(id, name, self.map)
    
    def HandleWin(self):
        self.chosenMessage = "You dont even come close to me, fools!"

    def HandleMotd(self):
        #self.callbacks.chat("Perish before the new King Léo, second of his name!")
        self.chosenMessage = "Make place for Ser Leo, always moving up!"
        self.chosenDirection = "up"

    def HandleGame(self, args):
        self.game_running = True
        self.Reset()
        self.id = int(args[2])
        self.mapWidth = int(args[0])
        self.mapHeight = int(args[1])
        self.map = Map(self.mapWidth, self.mapHeight)

    def HandlePos(self, args):
        id = int(args[0])
        x = int(args[1])
        y = int(args[2])
        self.players[id].updatePosition((x, y))

    def HandleTick(self):
        if self.game_running:
            direction = self.ChooseDirectionBasic()
            self.callbacks.move(direction)
            if self.chosenMessage:
                self.callbacks.chat(self.chosenMessage)
                self.chosenMessage = None
        self.map.printMapToFile()

    def HandleDeath(self, ids : list):
        for id in ids:
            self.players[int(id)].die()
        if self.player().dead:
            self.game_running = False

    def HandleMessage(eslf, args):
        pass

    def player(self):
        return self.players[self.id]
    
    def ChooseDirectionBasic(self):
        # this bot chooses first free square
        dir = "up"
        if self.map.isFree(self.map.getUpTile(self.player().pos)):
            dir = "up"
        elif self.map.isFree(self.map.getLeftTile(self.player().pos)):
            dir = "left"
        elif self.map.isFree(self.map.getDownTile(self.player().pos)):
            dir = "down"
        elif self.map.isFree(self.map.getRightTile(self.player().pos)):
            dir = "right"
        return dir
        
























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

    
    def HandleWin(self):
        self.callbacks.chat("You dont even come close to me, you dirty little rats!")

    def HandleMotd(self):
        NotImplemented

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
