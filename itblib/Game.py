from .Maps import Map, MapGrasslands
from .Grid import Grid
import json 

class Session:
    def __init__(self, connector):
        self.connector = connector
        self._players = []
        self._grid = Grid()
        self.state = "needsPlayers"
    
    def add_player(self, player):
        self._players.append(player)

    def start_game(self):
        with open("itblib/maps/sea_map.json","r") as f:
            contents = f.read()
        map = Map()
        map.import_from_str(contents)
        for player in self._players:
            self.connector.send_custom(player.playersocket, "MapTransfer", contents)
        self._grid.load_map(map)
        self.state = "running"
    

class Game:
    def __init__(self):
        self._sessions = []
    
    def get_sessions(self):
        return self._sessions
    
    def create_session(self):
        newsession = Session()
        self._sessions.append(newsession)
        return newsession
