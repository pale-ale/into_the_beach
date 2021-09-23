from itblib.SceneManager import SceneManager
from itblib.Maps import Map
from itblib.Player import Player
import json

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.Game import Session
    from itblib.Grid import Grid
    from itblib.abilities.AbilityBase import AbilityBase
    from itblib.net.Connector import Connector
    from itblib.ui.HUD import Hud

class NetEvents():
    grid:"Grid" = None
    session:"Session" = None
    connector:"Connector" = None
    hud:"Hud" = None
    scenemanager:"SceneManager" = None

    @staticmethod
    def snd_netmaptransfer(map:"Map"):
        NetEvents.connector.send_server_all(
            NetEvents.session._players, 
            "NetMapTransfer", 
            map.export_to_str()
        )

    @staticmethod
    def rcv_netmaptransfer(mapjson:str):
        newmap = Map()
        newmap.import_from_str(mapjson)
        print("Client: loading map...")
        NetEvents.grid.load_map(newmap, from_authority=True)

    @staticmethod
    def snd_netunitspawn(unitid:int, pos:"tuple[int,int]", ownerid:int):
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
        unitspawntuple = json.loads(unitspawntuplestr)
        unitid, pos, ownerid = unitspawntuple
        if NetEvents.connector.authority:
            #check whether this request is fulfillable, if not: return
            if NetEvents.grid.is_space_empty(False, pos):
                NetEvents.snd_netunitspawn(unitid, pos, ownerid)
                NetEvents.grid.add_unit(pos, unitid, ownerid)
        else:
            NetEvents.grid.add_unit(pos, unitid, ownerid)
    
    @staticmethod
    def snd_neteffectspawn(effectid:int, pos:"tuple[int,int]"):
        effectspawntuple = (effectid, pos)
        if NetEvents.connector.authority:
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetEffectSpawn", 
                json.dumps(effectspawntuple)
            )
        else:
            NetEvents.connector.send_client("NetEffectSpawn", json.dumps(effectspawntuple))
    
    @staticmethod
    def rcv_neteffectspawn(effectspawntuplestr):
        effectspawntuple = json.loads(effectspawntuplestr)
        effectid, pos = effectspawntuple
        if NetEvents.connector.authority:
            #if valid command:...
            NetEvents.grid.add_worldeffect(pos, effectid, from_authority=False)
        else:
            NetEvents.grid.add_worldeffect(pos, effectid, from_authority=True)

    @staticmethod
    def snd_netunitmove(fro:"tuple[int,int]", to:"tuple[int,int]"):
        #only the server my send actual unit-moves
        c = NetEvents.connector
        if c and c.authority:
            froto = [fro, to]
            frotodata = json.dumps(froto)
            c.send_server_all(
                NetEvents.session._players,
                "NetUnitMove",
                frotodata
            )

    @staticmethod
    def rcv_netunitmove(movedata):
        #this method is called on clients only
        fromto = json.loads(movedata)
        NetEvents.grid.move_unit(*fromto)

    @staticmethod
    def snd_netunithpchange(pos:"tuple[int,int]", new_hp:"int"):
        c = NetEvents.connector
        pos_hp_data = json.dumps([pos, new_hp])
        if c.authority:
            c.send_server_all(
                NetEvents.session._players,
                "NetUnitHpChange",
                pos_hp_data
            )

    @staticmethod
    def rcv_netunithpchange(pos_hp_data):
        pos , new_hp = json.loads(pos_hp_data)
        if not NetEvents.connector.authority:
            NetEvents.grid.get_unit(pos).hitpoints = new_hp

    @staticmethod
    def snd_netplayerjoin(targetconnection, player:Player, localcontrol:bool):
        d = player.get_info()
        d["localcontrol"] = localcontrol
        NetEvents.connector.send_server_single(targetconnection, "NetPlayerJoin", json.dumps(d))

    @staticmethod
    def rcv_netplayerjoin(playerdata):
        obj = json.loads(playerdata)
        player = Player(0, None)
        player.set_info(obj)
        NetEvents.session._players[player.playerid] = player
        if player.localcontrol:
            NetEvents.hud.playerid = player.playerid

    @staticmethod
    def snd_netphasechange(phasenumber):
        NetEvents.connector.send_server_all(
            NetEvents.session._players, 
            "NetPhaseChange", 
            str(phasenumber)
        )
    
    @staticmethod
    def rcv_netphasechange(phasenumber:int):
        phasenumber = int(phasenumber)
        NetEvents.grid.change_phase(phasenumber)

    @staticmethod
    def snd_netplayerleave(leavingplayer:"Player"):
        if not NetEvents.connector.authority:
            NetEvents.connector.send_client("NetPlayerLeave", str(leavingplayer.playerid))
        else:
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetPlayerLeave",
                str(leavingplayer.playerid))

    @staticmethod
    def rcv_netplayerleave(playerid:int):
        print("Bye")
        playerid = int(playerid)
        session = NetEvents.session
        session.remove_player(playerid)
        exit(0)
    
    @staticmethod
    def snd_netabilitytarget(ability:"AbilityBase"):
        targets = ability.selected_targets
        posnametargetsprimed = (ability._unit.pos, type(ability).__name__,  targets, ability.primed)
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
        ability = [a for a in unit.abilities if type(a).__name__ == abilityname][0]
        ability.selected_targets.clear()
        if NetEvents.connector.authority:
            ability.set_targets(primed, targets)

    @staticmethod
    def snd_netplayerwon(playerid:int):
        if NetEvents.connector.authority:
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetPlayerWon",
                str(playerid))

    @staticmethod
    def rcv_netplayerwon(playeridstr:str):
        if not NetEvents.connector.authority:
            NetEvents.session.state = "gameOver"
            NetEvents.hud.player_won(int(playeridstr)) 
            NetEvents.scenemanager.load_scene("MainMenuScene")         

    @staticmethod
    def rcv_event_caller(prefix:str, contents:str):
        if prefix not in RcvNetEventsMap:
            print(f"Bad NetEvent prefix: '{prefix}'")
            exit(1)
        RcvNetEventsMap[prefix](contents)
    
    @staticmethod
    def snd_netunitremove(pos:"tuple[int,int]"):
        if NetEvents.connector.authority:
            NetEvents.connector.send_server_all(
                NetEvents.session._players,
                "NetUnitRemove", 
                json.dumps(pos)
            )
        else:
            NetEvents.connector.send_client("NetUnitRemove", json.dumps(pos))
    
    @staticmethod
    def rcv_netunitremove(unitremoveposstr):
        unitremovetuple = json.loads(unitremoveposstr)
        if NetEvents.connector.authority:
            #check whether this request is fulfillable, if not: return
            if not NetEvents.grid.is_space_empty(False, unitremovetuple):
                NetEvents.snd_netunitremove(unitremovetuple)
                NetEvents.grid.remove_unit(unitremovetuple)
        else:
            NetEvents.grid.remove_unit(unitremovetuple)

    @staticmethod
    def snd_netsync():
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
        if not NetEvents.connector.authority:
            data = json.loads(datastr)
            NetEvents.grid.insert_data(data)


RcvNetEventsMap = {
    "NetAbilityTarget":NetEvents.rcv_netabilitytarget,
    "NetEffectSpawn":NetEvents.rcv_neteffectspawn,
    "NetMapTransfer":NetEvents.rcv_netmaptransfer,
    "NetPhaseChange":NetEvents.rcv_netphasechange,
    "NetPlayerJoin":NetEvents.rcv_netplayerjoin,
    "NetPlayerLeave":NetEvents.rcv_netplayerleave,
    "NetPlayerWon":NetEvents.rcv_netplayerwon,
    "NetUnitHpChange":NetEvents.rcv_netunithpchange,
    "NetUnitMove":NetEvents.rcv_netunitmove,
    "NetUnitSpawn":NetEvents.rcv_netunitspawn,
    "NetUnitRemove":NetEvents.rcv_netunitremove,
    "NetSync":NetEvents.rcv_netsync,
}
    