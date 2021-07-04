import socket

class Player:
    def __init__(self, id:int, playersocket:socket.socket):
        self.name = "Player_1"
        self.color = (0,150,50,255)
        self._initialunits = [1,1,2]
        self._controlledunits = []
        self.playerid = id
        self.playersocket = playersocket
        self.localcontrol = False
    
    def get_info(self):
        d = self.__dict__.copy()
        d.pop("playersocket")
        return d

    def set_info(self, info):
        for key in info.keys():
            self.__dict__[key] = info[key]
    