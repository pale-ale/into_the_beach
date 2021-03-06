from itblib.Log import log
from itblib.Vec import IVector2
from itblib.net.Connector import Connector
from itblib.Player import Player
from itblib.Maps import MapGrasslands, MapIceAge, MapRockValley
from itblib.Grid import Grid
from itblib.net.NetEvents import NetEvents 
import random

class Session:
    """
    Sessions keep track of who participates in a game as well as the state of a game.
    It is also used to manage the map for easy access.
    """

    def __init__(self, connector:Connector, observer=None):
        self.connector = connector
        self._players:"dict[int,Player]" = {}
        self._grid = Grid(connector) if connector and connector.authority else NetEvents.grid
        self._state = "needsPlayers"
        self._observer = observer
        self._map_options = [MapGrasslands, MapIceAge, MapRockValley]
    
    def set_state(self, new_state:str) -> None:
        """Update the state to a new one."""
        if new_state not in ["needsPlayers", "running", "runningPregame", "gameOver"]:
            print(f"Session: Unknown state: '{new_state}'")
        self._state = new_state
        if NetEvents.connector.authority:
            NetEvents.snd_netsessionstatechange(new_state)
        if self._observer:
            self._observer.update_data()
    
    def add_player(self, player:Player):
        """Add a player to the sesion."""
        if self.connector and self.connector.authority:
            for playerid in self._players.keys():
                if self._players[playerid].playersocket:
                    NetEvents.snd_netplayerjoin(self._players[playerid].playersocket, player, False)
            for playerid in self._players.keys():
                if player.playersocket:
                    NetEvents.snd_netplayerjoin(player.playersocket, self._players[playerid], False)
            if player.playersocket:
                NetEvents.snd_netplayerjoin(player.playersocket, player, True)
        self._players[player.playerid] = player
        if self._observer:
            self._observer.update_data()
    
    def remove_player(self, playerid:int, use_net=True):
        """Remove all players with matching playerid from the session."""
        log(f"Session: Removing player {playerid}", 0)
        if self.connector and self.connector.authority and use_net:
            NetEvents.snd_netplayerleave(playerid)
            if len(self._players) -1 < 2:
                self.set_state("gameOver")
        self._players.pop(playerid)
        if self._observer:
            self._observer.update_data()

    def start_game(self):
        """Begin the Unit Placement Phase, after which the normal turn cycle ensues."""
        #TODO: get the overlap of maps selected by both players
        map_intersection = {MapGrasslands}
        self._grid.load_map(random.choice(list(map_intersection))())
        p1, p2 = self._players.values()
        self._grid.add_unit(IVector2(2,1), 4, p1.playerid)
        self._grid.add_unit(IVector2(2,2), 5, p1.playerid)
        self._grid.add_unit(IVector2(7,8), 4, p2.playerid)
        self._grid.add_unit(IVector2(7,7), 6, p2.playerid)
        NetEvents.snd_netsessionstatechange("runningPregame")
        self._grid.change_phase(0)
        NetEvents.snd_netphasechange(0)
        NetEvents.snd_netsync()
        self.set_state("runningPregame")
    
    def objective_lost(self, playerid:int):
        opponent = [p for p in self._players.keys() if p != playerid][0]
        if NetEvents.connector.authority:
            NetEvents.snd_netplayerwon(opponent)
            NetEvents.session.set_state("gameOver")
    
    def get_player(self, playerid:int):
        return self._players.get(playerid, None)


# class Game:
#     """
#     Currently unused
#     """
    
#     def __init__(self):
#         self._sessions = []
    
#     def get_sessions(self):
#         return self._sessions
    
#     def create_session(self):
#         newsession = Session(None)
#         self._sessions.append(newsession)
#         return newsession
