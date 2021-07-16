from typing import Optional

from .GridElementUI import GridElementUI
from ..ui.TextureManager import Textures
from .Units import UnitBase

class UnitBaseUI(GridElementUI):
    def __init__(self, unit:UnitBase):
        super().__init__(parentelement=unit)
        self.direction = "sw"
    
    def update_unit(self, newunit:Optional[UnitBase]):
        self._parentelement = newunit
        self.visible = bool(newunit)
        if newunit:
            print("test:", newunit.name, newunit.__class__.__name__)
            spritesheet = Textures.get_spritesheet("Unit", newunit.name, "Idle", self.direction)
            self.update_texture_source(spritesheet)
        else:
            self._textures = []
