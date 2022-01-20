from pygame import Rect
import pygame.sprite
import pygame.font
import pygame.surface

import pygame

from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent

class TextBox(pygame.sprite.Sprite, ComponentAcceptor):
    """Since alpha=0 in text renders is currently broken, use (0,0,0,0) as color to be removed."""
    def __init__(self, 
                text:str = "AaBbCcDdEeFfGg;:_ÖÄ@ILil",
                bgcolor:"tuple[int,int,int,int]" = (0,0,0,255), 
                textcolor:"tuple[int,int,int,int]" = (255,255,255,255),
                fontsize:int = 20,
                pos:"tuple[int,int]" = (0,0),
                *groups: pygame.sprite.AbstractGroup) -> None:
        ComponentAcceptor.__init__(self)
        font = pygame.font.SysFont('firamono', fontsize)
        self.image = font.render(text, True, textcolor, bgcolor).copy().convert_alpha()
        self.image.set_colorkey((0,0,0,0))
        self.rect = Rect(*pos, *self.image.get_size())
        tfc = TransformComponent()
        tfc.attach_component(self)
        pygame.sprite.Sprite.__init__(self, *groups)
