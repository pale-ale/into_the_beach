from itblib.Player import Player
from itblib.Game import Session
import time
from itblib.net.Connector import Connector
from itblib.net import NetEvents

c = Connector(True)
c.server_init()

serversession = Session(c)
NetEvents.StaticObjects["Session"] = serversession
NetEvents.StaticObjects["Connector"] = c
NetEvents.StaticObjects["Grid"] = serversession._grid
nextfreeplayerid = 0

while True:
    while True:
        data = c.receive()
        if data:
            prefix, contents = data
            NetEvents.rcv_event_caller(prefix, contents)
        else:
            break
    time.sleep(2)
    if len(serversession._players) > 0:
        if serversession.state != "running":
            print("starting game")
            serversession.start_game()
        continue
    print("awaiting new connections...")
    for newconnection in c.get_incoming_connections():
        newplayer = Player(nextfreeplayerid, newconnection)
        serversession.add_player(newplayer)
        print("added player", newplayer.id)
        nextfreeplayerid += 1

