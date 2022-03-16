import json
from typing import TYPE_CHECKING

from itblib.gridelements.Effects import EffectStartingArea
from itblib.Player import Player

if TYPE_CHECKING:
    from itblib.abilities.base_abilities.AbilityBase import AbilityBase
    from itblib.Game import Session
    from itblib.Grid import Grid
    from itblib.net.Connector import Connector
    from itblib.ui.hud.HUD import Hud

class NetEvents():
    grid:"Grid" = None
    session:"Session" = None
    connector:"Connector" = None
    hud:"Hud" = None

    @staticmethod
    def snd_netunitspawn(unitid:int, pos:"tuple[int,int]", ownerid:int):
        """Send a unit spawn event over the network. Server and Client."""
        unitspawntuple = (unitid, pos, ownerid)
        if NetEvents.connector.authority:
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetUnitSpawn", 
                json.dumps(unitspawntuple)
            )
        else:
            NetEvents.connector.send_client("NetUnitSpawn", json.dumps(unitspawntuple))
    
    @staticmethod
    def rcv_netunitspawn(unitspawntuplestr):
        """Called when a unit spawn event was received. Server and Client."""
        unitspawntuple = json.loads(unitspawntuplestr)
        unitid, pos, ownerid = unitspawntuple
        #convert pos from list to tuple
        pos = tuple(pos)
        if NetEvents.connector.authority:
            #check whether this request is fulfillable, if not: return
            if NetEvents.grid.is_space_empty(False, pos):
                effects = NetEvents.grid.get_worldeffects(pos)
                for e in effects:
                    #check if our spawn area reches here
                    if isinstance(e, EffectStartingArea) and e.ownerid == ownerid:
                        NetEvents.snd_netunitspawn(unitid, pos, ownerid)
                        NetEvents.grid.add_unit(pos, unitid, ownerid)
                        return
        else:
            NetEvents.grid.add_unit(pos, unitid, ownerid)
    
    @staticmethod
    def snd_netplayerjoin(targetconnection, player:Player, localcontrol:bool):
        """Send info about a joined player to a client. Server only."""
        d = player.get_info()
        d["localcontrol"] = localcontrol
        NetEvents.connector.send_server_single(targetconnection, "NetPlayerJoin", json.dumps(d))

    @staticmethod
    def rcv_netplayerjoin(playerdata):
        """Called when a player is added to the game. Client only."""
        obj = json.loads(playerdata)
        player = Player(0, None)
        player.set_info(obj)
        NetEvents.session.add_player(player)
        if player.localcontrol:
            NetEvents.hud.playerid = player.playerid

    @staticmethod
    def snd_netphasechange(phasenumber):
        """Send the new phase to every connected client. Server only."""
        NetEvents.connector.send_server_all(
            NetEvents.session._players, 
            "NetPhaseChange", 
            str(phasenumber)
        )
    
    @staticmethod
    def rcv_netphasechange(phasenumber:int):
        """Set the phase to the one sent by the server. Client only."""
        phasenumber = int(phasenumber)
        NetEvents.grid.change_phase(phasenumber)

    @staticmethod
    def snd_netplayerleave(leavingplayerid:int):
        """Send the player leave event.\n
        If client, to the server. If server, to every other client.\n
        Server and Client."""
        if not NetEvents.connector.authority:
            NetEvents.connector.send_client("NetPlayerLeave", str(leavingplayerid))
        else:
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetPlayerLeave",
                str(leavingplayerid))

    @staticmethod
    def rcv_netplayerleave(leavingplayerid:str):
        """Called when a player leave event is received. Remove the player from the session. Server and Client."""
        leavingplayerid = int(leavingplayerid)
        NetEvents.session.remove_player(leavingplayerid)
    
    @staticmethod
    def snd_netabilitytarget(ability:"AbilityBase"):
        """Send a user's targeting preference to the server. Client only."""
        targets = ability.selected_targets
        posnametargetsprimed = (ability._owning_component.owner.pos, type(ability).__name__,  targets, ability.primed)
        posnametargetsprimedjson = json.dumps(posnametargetsprimed)
        if not NetEvents.connector.authority:
            NetEvents.connector.send_client("NetAbilityTarget", posnametargetsprimedjson)
        else:
            pass
            # NetEvents.connector.send_to_clients(
            #     NetEvents.session._players, 
            #     "NetAbilityTarget", 
            #     posnametargetsjson
            # )

    @staticmethod
    def rcv_netabilitytarget(posnametargetsprimedjson):
        """Apply the user's target choice whne received. Server only."""
        obj = json.loads(posnametargetsprimedjson)
        # targets will now be a list[list[int,int]], since tuples dont exist in json
        # for consistency we convert them back to list[tuple[int,int]]
        unitpos, abilityname, targets, primed = obj
        targets = [(x[0],x[1]) for x in targets]
        unit = NetEvents.grid.get_unit(unitpos)
        print("RCV AbilityTarget:", obj)
        if not unit:
            print("NetEvents: Target request '"+posnametargetsprimedjson+"'is unfulfillable, unit not found.")
            return
        ability = [a for a in unit.ability_component._abilities if type(a).__name__ == abilityname][0]
        ability.selected_targets.clear()
        if NetEvents.connector.authority:
            ability.set_targets(targets)
            ability.primed = primed

    @staticmethod
    def snd_netplayerwon(playerid:int):
        """Send a player win event to every connected client. Server only."""
        if NetEvents.connector.authority:
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetPlayerWon",
                str(playerid))

    @staticmethod
    def rcv_netplayerwon(playeridstr:str):
        """Called when a player win event was received. End the game and show who won. Client only."""
        if not NetEvents.connector.authority:
            NetEvents.session.set_state("gameOver")
            NetEvents.hud.player_won(int(playeridstr)) 

    @staticmethod
    def rcv_event_caller(prefix:str, contents:str):
        """Reroute the json data to the correct handler. If no handler was found, exit."""
        if prefix not in RcvNetEventsMap:
            print(f"Bad NetEvent prefix: '{prefix}'")
            exit(1)
        RcvNetEventsMap[prefix](contents)
   
    @staticmethod
    def snd_netsync():
        """Send the game state to every client. Potentially expensive. Server only."""
        if NetEvents.connector.authority:
            data = NetEvents.grid.extract_data()
            datastr = json.dumps(data)
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetSync",
                datastr
            )
    
    @staticmethod
    def rcv_netsync(datastr):
        """Apply received game state from the server. Potentially expensive. Client only."""
        if not NetEvents.connector.authority:
            data = json.loads(datastr)
            NetEvents.grid.insert_data(data)
    
    @staticmethod
    def snd_netsessionstatechange(new_session_state:str):
        """Change the session state of every connected client. Server only."""
        NetEvents.connector.send_server_all(
            NetEvents.session._players,
            "NetSessionStateChange",
            new_session_state
        )

    @staticmethod
    def rcv_netsessionstatechange(new_session_state:str):
        """Set the new session state. Client only."""
        NetEvents.session.set_state(new_session_state)


RcvNetEventsMap = {
    "NetAbilityTarget":NetEvents.rcv_netabilitytarget,
    "NetPhaseChange":NetEvents.rcv_netphasechange,
    "NetPlayerJoin":NetEvents.rcv_netplayerjoin,
    "NetPlayerLeave":NetEvents.rcv_netplayerleave,
    "NetPlayerWon":NetEvents.rcv_netplayerwon,
    "NetUnitSpawn":NetEvents.rcv_netunitspawn,
    "NetSync":NetEvents.rcv_netsync,
    "NetSessionStateChange":NetEvents.rcv_netsessionstatechange
}
    