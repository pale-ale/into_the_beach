import socket
import json
import os.path

class Player:
    """Represents a physical player at the "table"."""
    
    def __init__(self, id:int, playersocket:socket.socket, color=(0,150,50)):
        self.name = "Player_1"
        self.color = color
        self._initialunitids = PlayerData.roster
        self._controlledunits = []
        self.playerid = id
        self.playersocket = playersocket
        self.localcontrol = False
        self.replicatedproperties = ["name", "color", "_controlledunits", "playerid", "localcontrol"]

    def get_info(self):
        d = {}
        for property in self.replicatedproperties:
            d[property] = self.__dict__[property]
        return d

    def set_info(self, info):
        for property in self.replicatedproperties:
            self.__dict__[property] = info[property]


class PlayerData():
    roster = [1,1,1]
    sensitivity = 10.5
    properties = ["roster", "sensitivity"]

    @staticmethod
    def load(path):
        if os.path.isfile(path):
            with open(path, 'r') as file:
                datadict = json.loads(file.read())
            for p in PlayerData.properties:
                setattr(PlayerData, p, datadict[p])
            
    @staticmethod
    def save(path):
        datadict = dict()
        for p in PlayerData.properties:
            datadict[p] = vars(PlayerData)[p]
        with open(path, 'w') as file:
            file.write(json.dumps(datadict))