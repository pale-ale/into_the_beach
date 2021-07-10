from itblib.net.Connector import Connector
from itblib.Player import Player
from ..Maps import Map
import json

from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from itblib.Game import Session

ENetEvent = {
    "NetMapTransfer",
    "NetPlayerJoin",
    "NetPlayerLeave",
    "NetPhaseChange",
    "NetUnitSpawn",
    "NetUnitDamage",
    "NetUnitMove"
}

StaticObjects = {
    "Grid": None,
    "Session": None,
    "Connector": None,
    "Hud": None,
}

def snd_netmaptransfer(map):
    if StaticObjects["Connector"]:
        if StaticObjects["Connector"].authority:
            for player in StaticObjects["Session"]._players.values():
                StaticObjects["Connector"].send_custom(player.playersocket, "NetMapTransfer", map.export_to_str())

def rcv_netmaptransfer(mapjson:str):
    if not StaticObjects["Connector"].authority:
        newmap = Map()
        newmap.import_from_str(mapjson)
        print("Client: loading map...")
        StaticObjects["Grid"].load_map(newmap)

def snd_netunitspawn(unitid:int, pos:"tuple[int,int]", ownerid:int):
    unitspawntuple = (unitid, pos, ownerid)
    if StaticObjects["Connector"].authority:
        pass
    else:
        StaticObjects["Connector"].send("NetUnitSpawn", json.dumps(unitspawntuple))

def rcv_netunitspawn(unitspawntuplestr):
    unitspawntuple = json.loads(unitspawntuplestr)
    unitid, pos, ownerid = unitspawntuple
    if StaticObjects["Connector"].authority:
        #check whether this request is fulfillable, if not: return
        for player in StaticObjects["Session"]._players.values():
            StaticObjects["Connector"].send_custom(
                player.playersocket, 
                "NetUnitSpawn", 
                unitspawntuplestr
            )
    StaticObjects["Grid"].add_unit(*pos, unitid, ownerid)

def snd_netunitmovepreview(unit):
    path = unit.abilities["MovementAbility"].path
    pos = unit.get_position()
    pospath = (pos, path)
    pospathjson = json.dumps(pospath)
    if StaticObjects["Connector"].authority:
        StaticObjects["Connector"].send_to_clients(
            StaticObjects["Session"]._players, 
            "NetUnitMovePreview", 
            pospathjson
        )
    else:
        StaticObjects["Connector"].send("NetUnitMovePreview", pospathjson)

def rcv_netunitmovepreview(unitandpath):
    obj = json.loads(unitandpath)
    # unit path will now be a list[list[int,int]], since tuples dont exist in json
    unitpos, listpath = obj
    path = [(x[0],x[1]) for x in listpath]
    unit = StaticObjects["Grid"].get_unit(*unitpos)
    c = StaticObjects["Connector"]
    if c.authority:
        #verify move positions
        unit.abilities["MovementAbility"].set_path(path)
        snd_netunitmovepreview(unit)
    else:
        unit.abilities["MovementAbility"].set_path(path)

def snd_netunitmove(fro:"tuple[int,int]", to:"tuple[int,int]"):
    #only the server my send actual unit-moves
    froto = [*fro, *to]
    c = StaticObjects["Connector"]
    frotodata = json.dumps(froto)
    if c.authority:
        c.send_to_clients(
            StaticObjects["Session"]._players,
            "NetUnitMove",
            frotodata
        )

def rcv_netunitmove(movedata):
    #this method is called on clients only
    fromto = json.loads(movedata)
    c = StaticObjects["Connector"]
    StaticObjects["Grid"].move_unit(*fromto)

    #if server:
    #    if verified:
    #        add move
    #else:
    #    add move

def snd_netplayerjoin(targetconnection, player, localcontrol:bool):
    d = player.get_info()
    d["localcontrol"] = localcontrol
    StaticObjects["Connector"].send_custom(targetconnection, "NetPlayerJoin", json.dumps(d))

def rcv_netplayerjoin(playerdata):
    obj = json.loads(playerdata)
    player = Player(0, None)
    player.set_info(obj)
    StaticObjects["Session"]._players[player.playerid] = player
    if player.localcontrol:
        StaticObjects["Hud"].playerid = player.playerid

def snd_netphasechange(phasenumber):
    for player in StaticObjects["Session"]._players.values():
        StaticObjects["Connector"].send_custom(player.playersocket, "NetPhaseChange", str(phasenumber))

def rcv_netphasechange(phasenumber:int):
    phasenumber = int(phasenumber)
    print("got phasechange")
    StaticObjects["Grid"].change_phase(phasenumber)

def snd_netplayerleave(leavingplayer:Player):
    connector = StaticObjects["Connector"]
    connector = cast(Connector, connector)
    if not connector.authority:
        connector.send("NetPlayerLeave", str(leavingplayer.playerid))
    else:
        for player in StaticObjects["Session"]._players.values():
            connector.send_custom(player.playersocket, "NetPlayerLeave", str(player.playerid))

def rcv_netplayerleave(playerid:int):
    print("Bye")
    playerid = int(playerid)
    session = StaticObjects["Session"]
    session.remove_player(playerid)
    exit(0)

RcvNetEventsMap = {
    "NetMapTransfer":rcv_netmaptransfer,
    "NetUnitMovePreview":rcv_netunitmovepreview,
    "NetUnitMove":rcv_netunitmove,
    "NetPlayerJoin":rcv_netplayerjoin,
    "NetPhaseChange":rcv_netphasechange,
    "NetUnitSpawn":rcv_netunitspawn,
    "NetPlayerLeave":rcv_netplayerleave,
}
    
def rcv_event_caller(prefix:str, contents:str):
    if prefix not in RcvNetEventsMap:
        print(f"Bad NetEvent prefix: '{prefix}'")
        exit(1)
    RcvNetEventsMap[prefix](contents)
