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
        self._players[player.playerid] = player

    def start_game(self):
        self._grid.load_map(MapGrasslands())
        #NetEvents.snd_netmaptransfer(map)
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
