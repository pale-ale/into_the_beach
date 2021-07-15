import socket

class Player:
    """Represents a physical player at the "table"."""
    
    def __init__(self, id:int, playersocket:socket.socket):
        self.name = "Player_1"
        self.color = (0,150,50,255)
        self._initialunitids = [1,2,3]
        self._controlledunits = []
        self.playerid = id
        self.playersocket = playersocket
        self.localcontrol = False
        self.replicatedproperties = ["name", "color", "_initialunitids", "_controlledunits", "playerid", "localcontrol"]
    
    def get_info(self):
        d = {}
        for property in self.replicatedproperties:
            d[property] = self.__dict__[property]
        return d

    def set_info(self, info):
        for property in self.replicatedproperties:
            self.__dict__[property] = info[property]
    