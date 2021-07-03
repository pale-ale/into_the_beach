import socket

class Player:
    def __init__(self, id:int, playersocket:socket.socket):
        self.name = "Player_1"
        self.color = (0,150,50,255)
        self._initialunits = [1,1,2]
        self._controlledunits = []
        self.playerid = id
        self.playersocket = playersocket
