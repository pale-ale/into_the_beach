from itblib.net.Connector import Connector
from itblib.Player import Player
from itblib.Maps import MapGrasslands, MapIceAge, MapRockValley
from itblib.Grid import Grid
from itblib.net.NetEvents import NetEvents 

class Session:
    """
    Sessions keep track of who participates in a game as well as the state of a game.
    It is also used to manage the map for easy access.
    """

    def __init__(self, connector:Connector):
        self.connector = connector
        self._players:"dict[int,Player]" = {}
        self._grid = Grid(connector)
        self.state = "needsPlayers"
    
    def add_player(self, player:Player):
        """Add a player to the sesion."""
        if self.connector:
            for playerid in self._players.keys():
                if self._players[playerid].playersocket:
                    NetEvents.snd_netplayerjoin(self._players[playerid].playersocket, player, False)
            for playerid in self._players.keys():
                if player.playersocket:
                    NetEvents.snd_netplayerjoin(player.playersocket, self._players[playerid], False)
            if player.playersocket:
                NetEvents.snd_netplayerjoin(player.playersocket, player, True)
        self._players[player.playerid] = player
    
    def remove_player(self, playerid:int, use_net=True):
        """Remove all players with matching playerid from the session."""
        player = self._players[playerid]
        if self.connector and self.connector.authority and use_net:
            for playerid in self._players.keys():
                NetEvents.snd_netplayerleave(player)
            # for playerid in self._players.keys():
            #     NetEvents.snd_netplayerjoin(player.playersocket, self._players[playerid], False)
            # NetEvents.snd_netplayerjoin(player.playersocket, player, True)
        self._players.pop(playerid)

    def start_game(self):
        """Begin the Unit Placement Phase, after which the normal turn cycle ensues."""
        self._grid.load_map(MapGrasslands(), from_authority=True)
        #self._grid.load_map(MapIceAge(), from_authority=True)
        #self._grid.load_map(MapRockValley(), from_authority=True)
        #game mode specific
        NetEvents.snd_netmaptransfer(MapGrasslands())
        #NetEvents.snd_netmaptransfer(MapIceAge())
        #NetEvents.snd_netmaptransfer(MapRockValley())
        NetEvents.snd_netphasechange(0)
        p1, p2 = self._players.values()
        self._grid.add_unit((2,1), 4, p1.playerid)
        NetEvents.snd_netunitspawn(4, (2,1), p1.playerid)
        self._grid.add_unit((7,8), 4, p2.playerid)
        NetEvents.snd_netunitspawn(4, (7,8), p2.playerid)
        self._grid.add_unit((2,2), 5, p2.playerid)
        NetEvents.snd_netunitspawn(5, (2,2), p1.playerid)
        self._grid.add_unit((7,7), 6, p2.playerid)
        NetEvents.snd_netunitspawn(6, (7,7), p2.playerid)
        self.state = "runningPregame"
    
    def objective_lost(self, playerid:int):
        opponent = [p for p in self._players.keys() if p != playerid][0]
        if NetEvents.connector.authority:
            NetEvents.snd_netplayerwon(opponent)
            NetEvents.session.state = "gameOver"


class Game:
    """
    Currently unused
    """
    
    def __init__(self):
        self._sessions = []
    
    def get_sessions(self):
        return self._sessions
    
    def create_session(self):
        newsession = Session(None)
        self._sessions.append(newsession)
        return newsession
