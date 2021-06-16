import pygame.sprite
from Globals import Textures
import pygame

class GridElementUI(pygame.sprite.Sprite):
    def __init__(self, width:int=64, height:int=64, parentelement=None):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((150,80,80))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.visible = bool(parentelement)
        self.needsredraw = True
        self._textures = []
        self.animframe = -1
        self._parentelement = None

    def update_texture_source(self, source:"list[pygame.Surface]"):
        assert len(source) > 0, self._parentelement.name + " has not received a texture"
        self._textures = source
        self.update_image()
        self.needsredraw = True

    def update_image(self):
        if self.visible:
            newanimframe = int(self._parentelement.age % len(self._textures))
            if self.animframe != newanimframe:
                self.image = self._textures[newanimframe]
                self.animframe = newanimframe
                self.needsredraw = True
                return True
        return False