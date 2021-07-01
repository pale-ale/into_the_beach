from itblib.Player import Player
from itblib.Game import Session
import time
from itblib.net.Connector import Connector

c = Connector(True)
c.server_init()

serversession = Session(c)
nextfreeplayerid = 0

while True:
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

