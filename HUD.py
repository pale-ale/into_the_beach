import pygame
import pygame.sprite
from Globals import Textures

class Hud(pygame.sprite.Sprite):
    def __init__(self, width, height, gridui):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.gridui = gridui
        self.selectiontexture = pygame.image.load(Textures.texturepath+Textures.selectionpreviewtexture)
        self.movementtexture = pygame.image.load(Textures.texturepath+Textures.movementpreviewtexture)

    def select(self, position):
        unit = self.gridui.grid.get_unit(*position)
        if unit:
            x,y = self.gridui.transform_grid_screen(*position)
            screenpos = (x+self.rect.width/2, y)
            self.image.fill((0,0,0,0))
            self.image.blit(self.movementtexture, screenpos)

    def update_cursor(self, position):
        x,y = self.gridui.transform_grid_screen(*position)
        screenpos = (x+self.rect.width/2, y)
        self.image.fill((0,0,0,0))
        self.image.blit(self.selectiontexture, screenpos)