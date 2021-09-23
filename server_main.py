from itblib.Player import Player
from itblib.Game import Session
import time
import pygame
import random
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
            data = c.receive_server(player.playersocket)
            if data:
                prefix, contents = data
                NetEvents.rcv_event_caller(prefix, contents)
            else:
                break

def get_color(key:int):
    rgb = [random.randrange(0, 200), random.randrange(0, 200), random.randrange(0, 200)]
    rgb[key%3] = 255
    return tuple(rgb)

def manage_players():
    if len(serversession._players) > 1:
        if not serversession.state.startswith("running"):
            print("starting game")
            serversession.start_game()
        return
    for newconnection in c.get_incoming_connections():
        newplayerid = len(serversession._players)+1
        newplayer = Player(newplayerid, newconnection, color=get_color(len(serversession._players)))
        serversession.add_player(newplayer)
        print("added player", newplayer.playerid)
        newplayerid += 1

while True:
    handle_networking_events()
    manage_players()
    dt = clock.tick(FPS)/1000.0
    #dt = int(input()) / 1000.0
    if serversession.state in ["running", "runningPregame"]:
        serversession._grid.tick(dt)
    if serversession.state == "gameOver":
        serversession = Session(c)
        NetEvents.session = serversession
        NetEvents.grid = serversession._grid
        