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
            path_suffixes = Textures.effecttexturemapping[self._effect.id]
            for path_suffix in path_suffixes:
                self._textures.append(pygame.image.load(Textures.texturepath + path_suffix).convert_alpha())
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
