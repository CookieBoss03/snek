import numpy as np

class Player:
    def __init__(self, id : int, pos) -> None:
        self.id = id
        self.moveOrder = "up"
        self.lastPos = pos

class SnekGame:
    def __init__(self, mapSize):             
        self.h = Helpers()
        self.log = Log()
        self.reset(mapSize)
    def reset(self, mapSize):
        self.players = dict() 
        self.alivePlayers = []
        self.positions = np.full((mapSize, mapSize), -1)    
        self.mapSize = mapSize
        self.log.resetLogs()
    
    def addPlayer(self, id : int, pos):  
        player = Player(id,self.h.castPosToInt(pos))
        self.alivePlayers.append(player)
        self.players[id] = player
        self.updatePos(id, self.h.castPosToInt(pos))
    
    def removePlayer(self, id : int):    
        self.alivePlayers.remove(self.players[id])
        for x in range(self.mapSize):
            for y in range(self.mapSize):
                if self.positions[x,y] == id:
                    self.positions[x,y] = -1;
     
    def updatePos(self, id : int, pos):
        self.log.logMove(self.players[id], self.h.getPosFromMove(self.players[id], self.mapSize))
        self.positions[self.h.castPosToInt(pos)] = id
    
    def handleMoves(self): 
        newPositions = dict()
        #hanfle collisions
        collidedPlayers = set()
        alivePlayers = set()
        for player in self.alivePlayers:
            newPositions[player.id] = self.h.getPosFromMove(player, self.mapSize)
            alivePlayers.add(player.id)
            if self.positions[self.h.castPosToInt(newPositions[player.id] )] != -1:
                collidedPlayers.add(player.id)
                self.log.logDeath(player, newPositions[player.id], False)
        collidedPlayers.update(self.h.getCollidedPlayers(newPositions))
        for id in self.h.getCollidedPlayers(newPositions):
            self.log.logDeath(self.alivePlayers[id], newPositions[id], True)
        alivePlayers -= collidedPlayers
        #die
        for id in collidedPlayers:
            self.removePlayer(id)
        #move
        for id in alivePlayers:
            self.log.logMove(self.alivePlayers[id], newPositions[id])
            self.updatePos(id, newPositions[id])
    
    def tick(self):
        self.handleMoves()
        self.log.logTick()
        self.h.visualize(self)
        
       
    
class Helpers:
    def getVectorFromOrder(self, player : Player):
        match player.moveOrder:
            case "up":
                return (0,-1)
            case "down":
                return (0,1)
            case "right":
                return (1,0)
            case "left":
                return (-1,0)
    
    def getPosFromMove(self, player : Player, mapSize : int):
        oldPos = player.lastPos
        moveVec = self.getVectorFromOrder(player)
        return ((oldPos[0] + moveVec[0])%mapSize, (oldPos[1] + moveVec[1])%mapSize)
    
    def visualize(self, game: SnekGame):
        #Map
        lastPositions = []
        for player in game.alivePlayers:
            lastPositions.append(player.lastPos)
        with open("map.txt", 'w') as file:
            for i, row in enumerate(game.positions):
                for j, element in enumerate(row):
                    if element == -1:
                        file.write('.')
                    elif (i, j) in lastPositions:
                        file.write(f"o")  # Add bold formatting to the head of the snake
                    else:
                        file.write(str(element))
                    file.write(' ')  # Add space between elements for better readability
                file.write('\n')  # Add a newline at the end of each row
            # log
            file.write("\nLogs:\n")
            for log in game.log.getLogs():
                file.write(log + '\n')

    def getCollidedPlayers(self, positions):
        collided_players = set()
        # Find players with the same next position
        positions_count = {}
        for player_id, next_position in positions.items():
            if next_position not in positions_count:
                positions_count[next_position] = []
            positions_count[next_position].append(player_id)
        
        # Add players with collisions to collided_players set
        for players in positions_count.values():
            if len(players) > 1:
                collided_players.update(players)
        return collided_players

    def castPosToInt(self, pos):
        return (int(pos[0]), int(pos[1]))
    
class Log:
    logs = []
    def addLog(self, message):
        self.logs.append(message)
    
    def logMove(self, player:Player, newPos):
        self.addLog("Player " + str(player.id) + " moved " + player.moveOrder + " to cell " + str(newPos) + "."  )

    def logDeath(self, player:Player, newPos, collidedWithPlayer:bool):
        if collidedWithPlayer:
            collisionType = "Player Head"
        else:
            collisionType = "Player Body" 
        self.addLog("Player " + str(player.id) + " moved " + player.moveOrder + " to cell " + str(newPos) + "and died due to collision with " + collisionType)
    
    def logTick(self):
        self.addLog("-"*15)
    def getLogs(self):
        return self.logs

    def resetLogs(self):
        self.logs = []