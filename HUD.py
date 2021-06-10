import pygame
import pygame.sprite
from Globals import Textures

class Hud(pygame.sprite.Sprite):
    def __init__(self, width, height, gridui):
        super().__init__()
        self.image = pygame.Surface((width+64, height+64), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.gridui = gridui
        self.selectiontexture = pygame.image.load(Textures.texturepath+Textures.selectionpreviewtexture)
        self.movementtexture = pygame.image.load(Textures.texturepath+Textures.movementpreviewtexture)

    def select(self, position):
        unit = self.gridui.grid.get_unit(*position)
        if unit:
            print("Hooks triggered by OnSelect:", unit.trigger_hook("OnSelect"))
            self.image.fill((0,0,0,0))
            for movementoption in unit.abilities["MovementAbility"].movementinfo:
                x,y = self.gridui.transform_grid_screen(*movementoption)
                self.image.blit(self.movementtexture, (x,y))

    def update_cursor(self, position):
        x,y = self.gridui.transform_grid_screen(*position)
        self.image.fill((0,0,0,0))
        self.image.blit(self.selectiontexture, (x,y))