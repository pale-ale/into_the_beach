from Effects import EffectBase
from Globals import Textures
from GridElementUI import GridElementUI

import pygame.sprite
import pygame.rect
import pygame.image

class EffectBaseUI(GridElementUI):
    def __init__(self, effect:EffectBase, width:int=64, height:int=64):  
        super().__init__()
        self.visible = bool(effect)
        self._effect = effect  
        self._textures = []   

    def update_texture_source(self):
        self._textures.clear()
        if self._effect:
            self._textures = Textures.get_tile_effect_spritesheet(False, self._effect.name, "Default")
        self.needsredraw = True

    def update_effect(self, neweffect):
        self._effect = neweffect
        self.update_texture_source()
    
    def update(self):
        if self.visible:
            newimage = self._textures[int(self._effect.age % len(self._textures))]
            if self.image != newimage:
                self.image = newimage
                self.needsredraw = True
    
    def get_position(self):
        return self._effect.get_position()
