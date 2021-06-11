import pygame
import pygame.sprite
from Globals import Textures

class Hud(pygame.sprite.Sprite):
    def __init__(self, width, height, gridui):
        super().__init__()
        self.image = pygame.Surface((width+64, height+64), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.selectedunit = None
        self.gridui = gridui
        self.selectiontexture = pygame.image.load(Textures.texturepath+Textures.selectionpreviewtexture)
        self.movementtexture = pygame.image.load(Textures.texturepath+Textures.movementpreviewtexture)
        self.targetmovementtexture = pygame.image.load(Textures.texturepath+Textures.targetmovementpreviewtexture)
        self.cursorgridpos = (0,0)
        self.cursorscreenpos = (0,0)

    def select(self, position):
        unit = self.gridui.grid.get_unit(*position)
        if unit != self.selectedunit:
            if self.selectedunit:
                self.selectedunit.trigger_hook("OnDeselect")
        if unit:
            self.selectedunit = unit
            unit.trigger_hook("OnSelect")
        self.redraw()
    
    def redraw(self):
        self.image.fill((0,0,0,0))
        if self.selectedunit:
            for movementoption in self.selectedunit.abilities["MovementAbility"].movementinfo:
                x,y = self.gridui.transform_grid_screen(*movementoption)
                self.image.blit(self.movementtexture, (x,y))

        if self.selectedunit:
            print(self.selectedunit.name, self.cursorgridpos)
        self.image.blit(self.targetmovementtexture if self.selectedunit and 
            (self.cursorgridpos in self.selectedunit.abilities["MovementAbility"].movementinfo)
            else self.selectiontexture, self.cursorscreenpos)

    def update_cursor(self, position):
        self.cursorgridpos = position
        self.cursorscreenpos = self.gridui.transform_grid_screen(*position)
        self.redraw()