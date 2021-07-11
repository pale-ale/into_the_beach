from itblib.net.Connector import Connector
from itblib.Player import Player
from itblib.Maps import MapGrasslands
from itblib.Grid import Grid
from itblib.net.NetEvents import NetEvents 

class Session:
    def __init__(self, connector:Connector):
        self.connector = connector
        self._players:"dict[int,Player]" = {}
        self._grid = Grid(connector)
        self.state = "needsPlayers"
    
    def add_player(self, player:Player):
        if self.connector:
            for playerid in self._players.keys():
                NetEvents.snd_netplayerjoin(self._players[playerid].playersocket, player, False)
            for playerid in self._players.keys():
                NetEvents.snd_netplayerjoin(player.playersocket, self._players[playerid], False)
            NetEvents.snd_netplayerjoin(player.playersocket, player, True)
        self._players[player.playerid] = player
    
    def remove_player(self, playerid:int):
        player = self._players[playerid]
        if self.connector and self.connector.authority:
            for playerid in self._players.keys():
                NetEvents.snd_netplayerleave(player)
            # for playerid in self._players.keys():
            #     NetEvents.snd_netplayerjoin(player.playersocket, self._players[playerid], False)
            # NetEvents.snd_netplayerjoin(player.playersocket, player, True)
        self._players.pop(playerid)

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
