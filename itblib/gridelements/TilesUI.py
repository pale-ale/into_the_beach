from typing import Generator
import pygame

from itblib.ui.IDisplayable import IDisplayable
from .GridElementUI import GridElementUI
from .Tiles import TileBase

class TileBaseUI(GridElementUI, IDisplayable):
    def __init__(self, tile:TileBase, global_transform:pygame.Rect):
        super().__init__(parentelement=tile, global_transform=global_transform, direction=None)
        self.blits.append((self._textures[self.framenumber], self.global_transform, self.local_transform))
    
    def get_display_name(self) -> str:
        return "Somename"
    
    def get_display_description(self) -> str:
        return "I am an awesome and\n\
                quite long description."


class TileDirtUI(TileBaseUI):
    def get_display_name(self) -> str:
        return "Grass Tile"
    
    def get_display_description(self) -> str:
        return "I am an awesome and\n\
                quite long description."
