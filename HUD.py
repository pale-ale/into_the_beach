from typing import Text
from Tiles import TileForest
import pygame
import pygame.sprite
import pygame.font
from Globals import Textures

class Hud(pygame.sprite.Sprite):
    def __init__(self, width, height, gridui):
        super().__init__()
        self.image = pygame.Surface((width+64, height+64), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.selectedunit = None
        self.gridui = gridui
        self.font = pygame.font.SysFont('universalisadfstd', 22)
        self.selectiontexture = pygame.image.load(Textures.texturepath+Textures.selectionpreviewtexture)
        self.movementtexture = pygame.image.load(Textures.texturepath+Textures.movementpreviewtexture)
        self.targetmovementtexture = pygame.image.load(Textures.texturepath+Textures.targetmovementpreviewtexture)
        self.cursorgridpos = (0,0)
        self.cursorscreenpos = (0,0)
        self.tilefontdisplay = pygame.Surface((100,20))
        self.unitfontdisplay = pygame.Surface((100,20))

    def unitselect(self, position):
        unit = self.gridui.grid.get_unit(*position)
        if unit != self.selectedunit:
            if self.selectedunit:
                self.selectedunit.trigger_hook("OnDeselect")
        if unit:
            self.selectedunit = unit
            unit.trigger_hook("OnSelect")
        self.redraw()
    
    def targetselect(self, position):
        if self.selectedunit:
            self.selectedunit.trigger_hook("TargetSelected", [position])
            self.selectedunit.trigger_hook("OnDeselect")
            self.selectedunit = None
            self.redraw()

    def activate_ability(self, slot:int):
        if self.selectedunit:
            self.selectedunit.trigger_hook("UserAction" + str(slot))
            self.redraw()

    def display_unit(self, pos):
        self.unitfontdisplay.fill((0,0,0,0))
        unitui = self.gridui.uiunits[self.gridui.grid.c_to_i(*pos)]
        if unitui.visible:
            self.unitfontdisplay.blit(self.font.render(type(unitui._unit).__name__, True, (255,255,255,255)), (0,0))
            self.image.blit(unitui.image, (self.gridui.width*.8, self.gridui.height*.1), (0,0,64,64))
            abilities = unitui._unit.abilities.values()
            for ability in abilities:
                if ability.id in Textures.abilitytexturemapping.keys():
                    abilityimage = pygame.image.load(Textures.texturepath+Textures.abilitytexturemapping[ability.id])
                    self.image.blit(abilityimage, (self.gridui.width*.8, self.gridui.height*.1), (0,0,16,16))

                print(ability.id)
        self.image.blit(self.unitfontdisplay, (self.gridui.width*.92, self.gridui.height*.22))
    
    def display_tile(self, pos):
        self.tilefontdisplay.fill((0,0,0,0))
        tile = self.gridui.uitiles[self.gridui.grid.c_to_i(*pos)]
        if tile.visible:
            self.tilefontdisplay.blit(self.font.render(type(tile._tile).__name__, True, (255,255,255,255)), (0,0))
            self.image.blit(tile.image, (self.gridui.width*.8, self.gridui.height*.95), (0,0,64,64))
        self.image.blit(self.tilefontdisplay, (self.gridui.width*.92, self.gridui.height*.87))

    def redraw(self):
        self.image.fill((0,0,0,0))
        if self.selectedunit:
            for ability in self.selectedunit.abilities.values():
                for tilepos in ability.area_of_effect:
                    x,y = self.gridui.transform_grid_screen(*tilepos)
                    self.image.blit(self.movementtexture, (x,y))
        self.image.blit(self.targetmovementtexture if self.selectedunit and 
            (self.cursorgridpos in self.selectedunit.abilities["MovementAbility"].area_of_effect)
            else self.selectiontexture, self.cursorscreenpos)

        self.display_tile(self.cursorgridpos)
        self.display_unit(self.cursorgridpos)

    def update_cursor(self, position):
        self.cursorgridpos = position
        self.cursorscreenpos = self.gridui.transform_grid_screen(*position)
        self.redraw()
