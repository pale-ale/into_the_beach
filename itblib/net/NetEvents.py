from itblib.Maps import Map
from itblib.Player import Player
import json

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.Game import Session
    from itblib.Grid import Grid
    from itblib.gridelements.Units import UnitBase
    from itblib.net.Connector import Connector
    from itblib.ui.HUD import Hud

ENetEvent = {
    "NetMapTransfer",
    "NetPlayerJoin",
    "NetPlayerLeave",
    "NetPhaseChange",
    "NetUnitSpawn",
    "NetUnitDamage",
    "NetUnitMove"
}

class NetEvents():
    grid:"Grid" = None
    session:"Session" = None
    connector:"Connector" = None
    hud:"Hud" = None

    @staticmethod
    def snd_netmaptransfer(map:"Map"):
        NetEvents.connector.send_to_clients(
            NetEvents.session._players, 
            "NetMapTransfer", 
            map.export_to_str()
        )

    @staticmethod
    def rcv_netmaptransfer(mapjson:str):
        newmap = Map()
        newmap.import_from_str(mapjson)
        print("Client: loading map...")
        NetEvents.grid.load_map(newmap)

    @staticmethod
    def snd_netunitspawn(unitid:int, pos:"tuple[int,int]", ownerid:int):
        unitspawntuple = (unitid, pos, ownerid)
        if NetEvents.connector.authority:
            NetEvents.connector.send_to_clients(
                NetEvents.session._players,
                "NetUnitSpawn", 
                json.dumps(unitspawntuple)
            )
        else:
            NetEvents.connector.send("NetUnitSpawn", json.dumps(unitspawntuple))

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
    def snd_netunitmovepreview(unit:"UnitBase"):
        path = unit.abilities["MovementAbility"].path
        pospath = (unit.pos, path)
        pospathjson = json.dumps(pospath)
        if NetEvents.connector.authority:
            NetEvents.connector.send_to_clients(
                NetEvents.session._players, 
                "NetUnitMovePreview", 
                pospathjson
            )
        else:
            NetEvents.connector.send("NetUnitMovePreview", pospathjson)

    @staticmethod
    def rcv_netunitmovepreview(unitandpath):
        obj = json.loads(unitandpath)
        # unit path will now be a list[list[int,int]], since tuples dont exist in json
        unitpos, listpath = obj
        path = [(x[0],x[1]) for x in listpath]
        unit = NetEvents.grid.get_unit(unitpos)
        c = NetEvents.connector
        if c.authority:
            #verify move positions
            unit.abilities["MovementAbility"].set_path(path)
            NetEvents.snd_netunitmovepreview(unit)
        else:
            unit.abilities["MovementAbility"].set_path(path)

    @staticmethod
    def snd_netunitmove(fro:"tuple[int,int]", to:"tuple[int,int]"):
        #only the server my send actual unit-moves
        froto = [fro, to]
        c = NetEvents.connector
        frotodata = json.dumps(froto)
        if c.authority:
            c.send_to_clients(
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
    def snd_netplayerjoin(targetconnection, player, localcontrol:bool):
        d = player.get_info()
        d["localcontrol"] = localcontrol
        NetEvents.connector.send_custom(targetconnection, "NetPlayerJoin", json.dumps(d))

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
        for player in NetEvents.session._players.values():
            NetEvents.connector.send_custom(player.playersocket, "NetPhaseChange", str(phasenumber))
    
    @staticmethod
    def rcv_netphasechange(phasenumber:int):
        phasenumber = int(phasenumber)
        print("got phasechange")
        NetEvents.grid.change_phase(phasenumber)

    @staticmethod
    def snd_netplayerleave(leavingplayer:"Player"):
        if not NetEvents.connector.authority:
            NetEvents.connector.send("NetPlayerLeave", str(leavingplayer.playerid))
        else:
            NetEvents.connector.send_to_clients(
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
    def rcv_event_caller(prefix:str, contents:str):
        if prefix not in RcvNetEventsMap:
            print(f"Bad NetEvent prefix: '{prefix}'")
            exit(1)
        RcvNetEventsMap[prefix](contents)

RcvNetEventsMap = {
    "NetMapTransfer":NetEvents.rcv_netmaptransfer,
    "NetUnitMovePreview":NetEvents.rcv_netunitmovepreview,
    "NetUnitMove":NetEvents.rcv_netunitmove,
    "NetPlayerJoin":NetEvents.rcv_netplayerjoin,
    "NetPhaseChange":NetEvents.rcv_netphasechange,
    "NetUnitSpawn":NetEvents.rcv_netunitspawn,
    "NetPlayerLeave":NetEvents.rcv_netplayerleave,
}
    
