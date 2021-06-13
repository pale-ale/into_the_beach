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

    def update_texture_source(self):
        self._textures = []
        if self._unit:
            for suffix in Textures.unittexturemapping[self._unit.id]:
                path = Textures.texturepath + suffix
                self._textures.append(pygame.image.load(path).convert_alpha())
            self.update()
        
    def update(self):
        if self.visible:
            self.image = self._textures[self.direction]
    
    def update_unit(self, newunit):
        self._unit = newunit
        self.visible = bool(newunit)
        self.update_texture_source()

    def get_position(self):
        return self._unit.get_position()
