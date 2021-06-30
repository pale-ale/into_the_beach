NetEvents = {
    "NetMapTransfer",
    "NetPlayerJoin",
    "NetPlayerLeave",
    "NetUnitSpawn",
    "NetUnitDamage",
    "NetUnitMove"
}

def snd_netmaptransfer(mapjson:str):
    pass

def rcv_netmaptransfer(mapjson:str):
    pass

def snd_netunitmove(unit, connector):
    if connector.authority:
    #connector.sendtoclients(unit.path, unitid)
    else:
    #connector.sendtoserver(unit.path, unitid)

def rcv_netunitmove(unit, connector):
    if server:
        if verified:
            add move
    else:
        add move
        
    