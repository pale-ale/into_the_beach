from ..Maps import Map
import json

ENetEvent = {
    "NetMapTransfer",
    "NetPlayerJoin",
    "NetPlayerLeave",
    "NetUnitSpawn",
    "NetUnitDamage",
    "NetUnitMove"
}

StaticObjects = {
    "Grid": None,
    "Session": None,
    "Connector": None
}

def snd_netmaptransfer(map):
    if StaticObjects["Connector"].authority:
        print("Sending map to players")
        for player in StaticObjects["Session"]._players:
            StaticObjects["Connector"].send_custom(player.playersocket, "NetMapTransfer", map.export_to_str())

def rcv_netmaptransfer(mapjson:str):
    if not StaticObjects["Connector"].authority:
        print("Loading Map...")
        newmap = Map()
        newmap.import_from_str(mapjson)
        StaticObjects["Grid"].load_map(newmap)

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
    print("jsonstr:", unitandpath)
    obj = json.loads(unitandpath)
    unitpos, path = obj
    print("unitpos:", *unitpos)
    unit = StaticObjects["Grid"].get_unit(*unitpos)
    print("Moving unit:", unit.name)
    #if server:
    #    if verified:
    #        add move
    #else:
    #    add move
        
RcvNetEventsMap = {
    "NetMapTransfer" : rcv_netmaptransfer,
    "NetUnitMove" : rcv_netunitmove,
}
    
def rcv_event_caller(prefix:str, contents:str):
    if prefix not in RcvNetEventsMap:
        print(f"Bad NetEvent prefix: '{prefix}'")
        exit(1)
    RcvNetEventsMap[prefix](contents)
