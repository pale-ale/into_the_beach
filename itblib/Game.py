from .Maps import MapGrasslands
from .Grid import Grid

class Session:
    def __init__(self):
        self._players = []
        self._grid = Grid()
        self.state = "awaitingStart"
    
    def add_player(self, player):
        self._players.append(player)

    def start_game(self):
        self._grid.load_map(MapGrasslands())
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
