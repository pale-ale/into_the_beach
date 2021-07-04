from itblib.Player import Player
from itblib.Game import Session
import time
import pygame
from itblib.net.Connector import Connector
from itblib.net import NetEvents

FPS = 10

clock = pygame.time.Clock()
c = Connector(True)
c.server_init()

serversession = Session(c)
NetEvents.StaticObjects["Session"] = serversession
NetEvents.StaticObjects["Connector"] = c
NetEvents.StaticObjects["Grid"] = serversession._grid

def handle_networking_events():
    while True:
            data = c.receive()
            if data:
                prefix, contents = data
                NetEvents.rcv_event_caller(prefix, contents)
            else:
                break

def manage_players():
    if len(serversession._players) > 0:
        if not serversession.state.startswith("running"):
            print("starting game")
            serversession.start_game()
        return
    print("awaiting new connections...")
    for newconnection in c.get_incoming_connections():
        newplayerid = len(serversession._players)
        newplayer = Player(newplayerid, newconnection)
        serversession.add_player(newplayer)
        print("added player", newplayer.playerid)
        newplayerid += 1

while True:
    handle_networking_events()
    manage_players()
    dt = clock.tick(FPS)/1000.0
    serversession._grid.tick(dt)
