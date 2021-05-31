import pygame.sprite
import pygame.rect
import pygame.image

from Effects import EffectBase
from Globals import Textures

class EffectBaseUI(pygame.sprite.Sprite):
    def __init__(self, effect:EffectBase, width:int=64, height:int=64):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.visible = bool(effect)
        self._effect = effect  
        self._textures = []         

    def update_texture_source(self):
        self._textures.clear()
        if self._effect:
            path_suffixes = Textures.effectmapping[self._effect.id]
            for path_suffix in path_suffixes:
                self._textures.append(pygame.image.load(Textures.texturepath + path_suffix))

    def update_effect(self, neweffect):
        self._effect = neweffect
        self.update_texture_source()
    
    def update(self):
        if self.visible:
            self.image = self._textures[int(self._effect.age % len(self._textures))]
    
    def get_position(self):
        return self._effect.get_position()