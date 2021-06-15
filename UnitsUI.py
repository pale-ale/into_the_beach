from typing import Text
import pygame
from GridElementUI import GridElementUI
from Globals import Textures

class UnitBaseUI(GridElementUI):
    def __init__(self, unit):
        super().__init__(parentelement=unit)
        self.direction = "sw"
        self.darkfilter = pygame.Surface((64,64), pygame.SRCALPHA)
        self.filterstate = False
    
    def update_unit(self, newunit):
        self._parentelement = newunit
        self.visible = bool(newunit)
        if newunit:
            self.update_texture_source(
                Textures.get_spritesheet("Unit", newunit.name, "Idle", self.direction)
            )

    def get_position(self):
        return self._parentelement.get_position()

    def update_image(self):
        if self.visible:
            super().update_image(not self._parentelement.myturn)
      