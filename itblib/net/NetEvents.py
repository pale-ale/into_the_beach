from ..Maps import Map

ENetEvent = {
    "NetMapTransfer",
    "NetPlayerJoin",
    "NetPlayerLeave",
    "NetUnitSpawn",
    "NetUnitDamage",
    "NetUnitMove"
}

StaticObjects = {
    "Grid": None
}

def snd_netmaptransfer(mapjson:str, connector):
    pass

def rcv_netmaptransfer(mapjson:str, connector):
    if not connector.authority:
        print("Loading Map...")
        newmap = Map()
        newmap.import_from_str(mapjson)
        StaticObjects["Grid"].load_map(newmap)

def snd_netunitmove(unit, connector):
    pass
    #if connector.authority:
    #connector.sendtoclients(unit.path, unitid)
    #else:
    #connector.sendtoserver(unit.path, unitid)

def rcv_netunitmove(unit, connector):
    pass
    #if server:
    #    if verified:
    #        add move
    #else:
    #    add move
        
RcvNetEventsMap = {
    "NetMapTransfer" : rcv_netmaptransfer
}
    
def rcv_event_caller(prefix:str, contents:str, connector):
    if prefix not in RcvNetEventsMap:
        print(f"Bad NetEvent prefix: '{prefix}'")
        exit(1)
    RcvNetEventsMap[prefix](contents, connector)