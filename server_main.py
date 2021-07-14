from itblib.Player import Player
from itblib.Game import Session
import time
import pygame
from itblib.net.Connector import Connector
from itblib.net.NetEvents import NetEvents

FPS = 10

clock = pygame.time.Clock()
c = Connector(True)
c.server_init()

serversession = Session(c)
NetEvents.session = serversession
NetEvents.connector = c
NetEvents.grid = serversession._grid

def handle_networking_events():
    for player in serversession._players.values():
        while True:
            data = c.receive_custom(player.playersocket)
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
        newplayerid = len(serversession._players)+1
        newplayer = Player(newplayerid, newconnection)
        serversession.add_player(newplayer)
        print("added player", newplayer.playerid)
        newplayerid += 1

while True:
    handle_networking_events()
    manage_players()
    dt = clock.tick(FPS)/1000.0
    #dt = int(input()) / 1000.0
    serversession._grid.tick(dt)
