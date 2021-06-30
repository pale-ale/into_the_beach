import socket

class Player:
    def __init__(self, id:int, playersocket:socket.socket):
        self.name = "Player_1"
        self.color = (0,150,50,255)
        self._controlled_units = []
        self.id = id
        self.playersocket = playersocket
