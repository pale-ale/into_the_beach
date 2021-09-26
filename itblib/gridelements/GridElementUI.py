from itblib.gridelements.GridElement import GridElement
from itblib.ui.TextureManager import Textures
import pygame.sprite
import pygame

class GridElementUI(pygame.sprite.Sprite):
    """Graphical representation of a GridElement."""
    
    def __init__(self, parentelement:GridElement, direction:"str|None", width:int=64, height:int=64, framespeed:float=.5):
        assert isinstance(parentelement, GridElement), "GridElementUIs must now have an associated parent."
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.visible = True
        self.needsredraw = True
        self._textures = []
        self.animframe = -1
        self.framespeed = framespeed
        self.frametime = 0
        self._parentelement = parentelement
        self.direction = direction

        texturekey = parentelement.name
        if self.direction:
            texturekey += self.direction + "Idle"
        else:
            texturekey += "Default"
        spritesheet = Textures.get_spritesheet(texturekey)
        if spritesheet:
            self.update_texture_source(spritesheet)


    def update_texture_source(self, source:"list[pygame.Surface]"):
        """Set a new spritesheet as this UIElements' texture soure."""
        assert len(source) > 0, self._parentelement.name + " has not received a texture"
        self._textures = source
        self.needsredraw = True
        self.animframe = -1
        self.frametime = 0

    def update(self):
        """Update animations etc. to a new frame"""
        if self.visible and len(self._textures) > 0:
            if self._parentelement.age > self.frametime + self.framespeed:
                newanimframe = (self.animframe+1) % len(self._textures)
                self.image = self._textures[newanimframe]
                self.animframe+=1
                self.frametime = self._parentelement.age
                self.needsredraw = True
                return True
        return False
