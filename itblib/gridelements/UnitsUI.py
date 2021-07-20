from typing import Optional

from .GridElementUI import GridElementUI
from ..ui.TextureManager import Textures
from .Units import UnitBase

class UnitBaseUI(GridElementUI):
    def __init__(self, unit:UnitBase):
        super().__init__(parentelement=unit)
        self._parentelement:"UnitBase"
        self.direction = "SW"
        
