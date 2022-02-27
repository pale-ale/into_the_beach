from typing import TYPE_CHECKING

import pygame
from itblib.globals.Colors import BLACK
from itblib.input.Input import InputAcceptor
from itblib.net.NetEvents import NetEvents
from itblib.ui.IGraphics import IGraphics

if TYPE_CHECKING:
    from itblib.SceneManager import SceneManager

class SceneBase(IGraphics, InputAcceptor):
    """
    Scenes are a way to organize several Display-Objects as well as their functioniality,
    essentially allowing for easy grouping.

    Scenes are managed by the SceneManager, 
    which is able to e.g. load() and unload() scenes before and after use, respectively. 
    """

    def __init__(self, scenemanager:"SceneManager") -> None:
        IGraphics.__init__(self)
        InputAcceptor.__init__(self)
        self.scenemanager = scenemanager
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
    
    def on_displayresize(self, newsize:"tuple[int,int]"):
        pass
        
    def update(self, delta_time:float):
        if NetEvents.connector and NetEvents.connector.acc_connection:
            data = NetEvents.connector.receive_client()
            if data:
                prefix, contents = data
                NetEvents.rcv_event_caller(prefix, contents)
    
    def clear(self):
        """Fill the scene with solid black."""
        s = pygame.Surface(self.scenemanager.scene_size)
        s.fill(BLACK)
        self.blits.append((s, s.get_rect(), s.get_rect()))
    
    def load(self):
        """Initialize a scene, load textures, etc."""
        self.clear()

    def unload(self):
        """Perform cleanup tasks."""
    