import socket
import json
import os.path
from itblib.Log import log

class Player:
    """Represents a physical player at the "table"."""
    
    def __init__(self, id:int, playersocket:socket.socket, color=(0,150,50)):
        self.name = "Player_" + str(id)
        self.color = color
        self._initialunitids:list[int] = []
        for unitidstr, unitcount in PlayerData.roster.items():
            self._initialunitids.extend([int(unitidstr)]*unitcount)
        self._controlledunits = []
        self.playerid = id
        self.level = 0
        self.playersocket = playersocket
        self.localcontrol = False
        self.replicatedproperties = ["name", "color", "_controlledunits", "playerid", "level", "localcontrol"]

    def get_info(self):
        d = {}
        for property in self.replicatedproperties:
            d[property] = self.__dict__[property]
        return d

    def set_info(self, info):
        for property in self.replicatedproperties:
            self.__dict__[property] = info[property]


class PlayerData():
    roster = {"2":3}
    desired_maps = ["MapGrasslands", "MapRockValley"]
    sensitivity = 10.5
    properties = ["roster", "desired_maps", "sensitivity"]

    @staticmethod
    def load(path):
        if os.path.isfile(path):
            datadict = {}
            with open(path, 'r') as file:
                try:
                    datadict = json.loads(file.read())
                except json.JSONDecodeError:
                    log(f"Couldn't parse playerdata file '{path}'.", 2)
            for p in PlayerData.properties:
                if p in datadict.keys():
                    setattr(PlayerData, p, datadict[p])
        else:
            log(f"Couldn't open playerdata file '{path}'.", 2)

    @staticmethod
    def save(path):
        datadict = dict()
        for p in PlayerData.properties:
            datadict[p] = vars(PlayerData)[p]
        with open(path, 'w') as file:
            file.write(json.dumps(datadict))