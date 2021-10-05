from .Effects import EffectBase, EffectRiver
from .GridElementUI import GridElementUI
from ..ui.TextureManager import Textures
from itblib.Globals.Enums import RIVER

class EffectBaseUI(GridElementUI):
    def __init__(self, effect:EffectBase, width:int=64, height:int=64, framespeed:float=.5):  
        super().__init__(direction=None, width=width, height=height, parentelement=effect, framespeed=framespeed)
    

class EffectHealUI(EffectBaseUI):
    def __init__(self, effect:EffectBase):  
        super().__init__(effect=effect, framespeed=.1)


class EffectRiverUI(EffectBaseUI):
    def __init__(self, effect:EffectRiver, width:int=64, height:int=64):  
        super().__init__(width=width, height=height, effect=effect)
    
    def update(self):
        if self.visible:
            grid = self._parentelement.grid
            pos = self._parentelement.pos
            neighborposs = grid.get_ordinal_neighbors(pos)
            riverposs = []
            for rpos in neighborposs: 
                for effect in grid.get_worldeffects(rpos):
                    if type(effect).__name__ == "EffectRiver":
                        riverposs.append(rpos)
            if len(riverposs) == 0:
                imageid = 4
            elif len(riverposs) == 1:
                imageid = 5
            elif len(riverposs) == 2:
                prev, next = riverposs
                prevdelta = (pos[0] - prev[0], pos[1] - prev[1])
                nextdelta = (next[0] - pos[0], next[1] - pos[1])
                imageid = RIVER[(*nextdelta, *prevdelta)]
            else:
                print("EffectRiverUI: Weird riverposs:", riverposs)
                return False
            newanimframe = 6*int(self._parentelement.age) % 2 + imageid
            if self.animframe != newanimframe:
                self.image = self._textures[newanimframe]
                self.animframe = newanimframe
                self.needsredraw = True
                return True
        return False

