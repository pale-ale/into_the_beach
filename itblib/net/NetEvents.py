from itblib.Player import Player
from ..Maps import Map
import json

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
    print(unitspawntuple)
    if StaticObjects["Connector"].authority:
        pass#StaticObjects["Connector"].sendtoclients(unit.path, unitid)
    else:

        StaticObjects["Connector"].send("NetUnitSpawn", json.dumps(unitspawntuple))

def rcv_netunitspawn(unitspawntuplestr):
    unitspawntuple = json.loads(unitspawntuplestr)
    unitid, pos, ownerid = unitspawntuple
    if StaticObjects["Connector"].authority:
        #check whether this request is fulfillable, if not: return
        print("spawning:", unitspawntuple)
        for player in StaticObjects["Session"]._players.values():
            StaticObjects["Connector"].send_custom(player.playersocket, "NetUnitSpawn", unitspawntuplestr)
    StaticObjects["Grid"].add_unit(*pos, unitid)

def snd_netunitmove(unit):
    path = [x[0] for x in unit.abilities["MovementAbility"].selected_targets]
    pos = unit.get_position()
    pospath = (pos, path)
    pospathjson = json.dumps(pospath)
    if StaticObjects["Connector"].authority:
        pass#StaticObjects["Connector"].sendtoclients(unit.path, unitid)
    else:
        StaticObjects["Connector"].send("NetUnitMove", pospathjson)

def rcv_netunitmove(unitandpath):
    obj = json.loads(unitandpath)
    unitpos, path = obj
    unit = StaticObjects["Grid"].get_unit(*unitpos)
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

def snd_netphasechange(phasenumber):
    for player in StaticObjects["Session"]._players.values():
        StaticObjects["Connector"].send_custom(player.playersocket, "NetPhaseChange", str(phasenumber))

def rcv_netphasechange(phasenumber:int):
    phasenumber = int(phasenumber)
    print("got phasechange")
    StaticObjects["Grid"].change_phase(phasenumber)
        
RcvNetEventsMap = {
    "NetMapTransfer" : rcv_netmaptransfer,
    "NetUnitMove" : rcv_netunitmove,
    "NetPlayerJoin" : rcv_netplayerjoin,
    "NetPhaseChange" : rcv_netphasechange,
    "NetUnitSpawn" : rcv_netunitspawn,
}
    
def rcv_event_caller(prefix:str, contents:str):
    if prefix not in RcvNetEventsMap:
        print(f"Bad NetEvent prefix: '{prefix}'")
        exit(1)
    RcvNetEventsMap[prefix](contents)
