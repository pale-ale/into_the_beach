from typing import Generator
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.gridelements.GridElement import GridElement
from itblib.ui.TextureManager import Textures
from itblib.ui.animations.MultiSprite import MultiSprite

import pygame

class GridElementUI(MultiSprite, ComponentAcceptor):
    """Graphical representation of a GridElement."""
    
    def __init__(self, parentelement:GridElement, global_transform:pygame.Rect, direction:"str|None", framespeed:float=.5):
        texturekey = parentelement.name
        if direction:
            texturekey += direction + "Idle"
        else:
            texturekey += "Default"
        spritesheet = Textures.get_spritesheet(texturekey)
        MultiSprite.__init__(self, spritesheet, global_transform=global_transform, frametime=framespeed, playing=False, looping=False)
        ComponentAcceptor.__init__(self)
        self._parentelement = parentelement
        self.direction = direction
        tfc = TransformComponent()
        tfc.attach_component(self)
    