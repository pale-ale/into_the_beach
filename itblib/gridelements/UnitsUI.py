from .GridElementUI import GridElementUI
from ..ui.TextureManager import Textures

class UnitBaseUI(GridElementUI):
    def __init__(self, unit):
        super().__init__(parentelement=unit)
        self.direction = "sw"
    
    def update_unit(self, newunit):
        self._parentelement = newunit
        self.visible = bool(newunit)
        if newunit:
            spritesheet = Textures.get_spritesheet("Unit", newunit.name, "Idle", self.direction)
            self.update_texture_source(spritesheet)
        else:
            self._textures = []
