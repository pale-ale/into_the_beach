from typing import Text
import pygame
from GridElementUI import GridElementUI
from Globals import Textures

class UnitBaseUI(GridElementUI):
    def __init__(self, unit):
        super().__init__()
        self._unit = unit
        self._textures = dict()
        self.texkey = 0
        self.visible = bool(unit)
        self.direction = 0

    def update(self):
        if self.visible:
            self.image = self._textures[0]
    
    def update_unit(self, newunit):
        self._unit = newunit
        self.visible = bool(newunit)
        if self._unit:
            self._textures = Textures.get_spritesheet(self._unit.name, "Idle", self._unit.orientation)
        self.update()

    def get_position(self):
        return self._unit.get_position()
