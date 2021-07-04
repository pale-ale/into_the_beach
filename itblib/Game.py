from .Maps import Map, MapGrasslands
from .Grid import Grid
from .net import NetEvents 
import json

class Session:
    def __init__(self, connector):
        self.connector = connector
        self._players = {}
        self._grid = Grid()
        self.state = "needsPlayers"
    
    def add_player(self, player):
        if self.connector:
            for playerid in self._players.keys():
                NetEvents.snd_netplayerjoin(self._players[playerid].playersocket, player, False)
            for playerid in self._players.keys():
                NetEvents.snd_netplayerjoin(player.playersocket, self._players[playerid], False)
            NetEvents.snd_netplayerjoin(player.playersocket, player, True)
        self._players[player.playerid] = player

    def start_game(self):
        self._grid.load_map(MapGrasslands())
        NetEvents.snd_netmaptransfer(MapGrasslands())
        self.state = "running_pregame"
    

class Game:
    def __init__(self):
        self._sessions = []
    
    def get_sessions(self):
        return self._sessions
    
    def create_session(self):
        newsession = Session(None)
        self._sessions.append(newsession)
        return newsession
