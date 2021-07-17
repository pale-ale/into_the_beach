from .Effects import EffectBase, EffectRiver
from .GridElementUI import GridElementUI
from ..ui.TextureManager import Textures
from itblib.Enums import RIVER

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
    

class EffectRiverUI(EffectBaseUI):
    def __init__(self, effect:EffectRiver, width:int=64, height:int=64):  
        super().__init__(width=width, height=height, effect=effect)
    
    def update(self):
        if self.visible:
            grid = self._parentelement.grid
            pos = self._parentelement.pos
            neighborposs = grid.get_ordinal_neighbors(*pos)
            riverposs = [rpos for rpos in neighborposs if 
                grid.get_effect(*rpos) and 
                type(grid.get_effect(*rpos)).__name__ == "EffectRiver"]
            if len(riverposs) == 0:
                imageid = 4
            elif len(riverposs) == 1:
                imageid = 5
            elif len(riverposs) == 2:
                prev, next = riverposs
                prevdelta = (pos[0] - prev[0], pos[1] - prev[1])
                nextdelta = (next[0] - pos[0], next[1] - pos[1])
                imageid = RIVER[(*nextdelta, *prevdelta)]
            newanimframe = 6*int(self._parentelement.age) % 2 + imageid
            if self.animframe != newanimframe:
                self.image = self._textures[newanimframe]
                self.animframe = newanimframe
                self.needsredraw = True
                return True
        return False

