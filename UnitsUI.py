from typing import Text
import pygame
from GridElementUI import GridElementUI
from Globals import Textures

class UnitBaseUI(GridElementUI):
    def __init__(self, unit):
        super().__init__(parentelement=unit)
        self.direction = "sw"
    
    def update_unit(self, newunit):
        self._parentelement = newunit
        self.visible = bool(newunit)
        if newunit:
            self.update_texture_source(
                Textures.get_spritesheet("Unit", newunit.name, "Idle", self.direction)
            )

    def get_position(self):
        return self._parentelement.get_position()
