from .Effects import EffectBase
from .GridElementUI import GridElementUI
from ..ui.TextureManager import Textures

class EffectBaseUI(GridElementUI):
    def __init__(self, effect:EffectBase, width:int=64, height:int=64):  
        super().__init__(width=width, height=height, parentelement=effect)

    def update_effect(self, neweffect:EffectBase):
        self._parentelement = neweffect
        self.visible = bool(neweffect)
        if neweffect:
            self.update_texture_source(
                Textures.get_spritesheet("Effect", neweffect.name, "Default")
            )
    
    def get_position(self):
        return self._parentelement.get_position()
