from typing import Optional
from itblib.gridelements.GridElement import GridElement
from itblib.ui.TextureManager import Textures
import pygame.sprite
import pygame

class GridElementUI(pygame.sprite.Sprite):
    """Graphical representation of a GridElement."""
    
    def __init__(self, width:int=64, height:int=64, parentelement:Optional[GridElement]=None):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.visible = bool(parentelement)
        self.needsredraw = True
        self._textures = []
        self.animframe = -1
        self._parentelement = parentelement

    def update_texture_source(self, source:"list[pygame.Surface]"):
        """Set a new spritesheet as this UIElements' texture soure."""
        assert len(source) > 0, self._parentelement.name + " has not received a texture"
        self._textures = source
        self.update()
        self.needsredraw = True
        self.animframe = -1

    def update(self):
        """Update animations etc. to a new frame"""
        if self.visible:
            newanimframe = int(self._parentelement.age) % len(self._textures)
            if self.animframe != newanimframe:
                self.image = self._textures[newanimframe]
                self.animframe = newanimframe
                self.needsredraw = True
                return True
        return False
