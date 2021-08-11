import pygame
import pygame.sprite
import pygame.transform
import pygame.font
import pygame.image
from itblib.ui.TextureManager import Textures
from itblib.Enums import PHASES, PREVIEWS
from itblib.gridelements.UnitsUI import UnitBaseUI
from itblib.ui.GridUI import GridUI
from itblib.Game import Session
from itblib.Vec import Vec
from itblib.gridelements.Units import UnitBase
from itblib.net.NetEvents import NetEvents

class UnitDisplay(pygame.sprite.Sprite):
    """Allows for easier display of a unit on the HUD."""

    def __init__(self):
        super().__init__()
        self.imagepos = (0,0)
        self.titlepos = (64,0)
        self.abilityimagepos = (64,23)
        self.abilityphasepos = (64,44)
        self.defaultimagecolor = (30,0,0,255)
        self.defaulttextboxcolor = (50,50,50,255)
        self.font = pygame.font.SysFont('latinmodernmono', 15)
        self.rect = pygame.Rect(0,0,200,100)
        self.image = pygame.Surface(self.rect.size).convert_alpha()
        self.image.fill((0))
        self.displayunit:UnitBaseUI = None
        self.phasecolors = ((255,255,0,255) ,(75,75,55,255), (50,255,50,255), (255,50,50,255), (255,200,0,255))
        self.set_displayunit(None)
    
    def set_displayunit(self, unit:UnitBaseUI):
        """Set the new unit to display."""
        self.displayunit = unit
        self.image.fill(self.defaultimagecolor, (*self.imagepos,64,64))
        self.image.fill(self.defaulttextboxcolor, (*self.titlepos,128,20))
        self.image.fill(self.defaulttextboxcolor, (*self.abilityimagepos,128,20))
        self.image.fill(self.defaulttextboxcolor, (*self.abilityphasepos,128,20))
        if self.displayunit:
            self.image.blit(
                self.font.render(
                    type(unit._parentelement).__name__, True, (255,255,255,255)
                ), 
                self.titlepos
            )
            self.image.blit(unit.image, Vec.comp_add2(self.imagepos, (0,10)))
            self.display_abilities(unit._parentelement)
    
    def display_abilities(self, unit:UnitBase):
        """Display the abilities of a unit."""
        abilities = unit.abilities
        index = 0
        for ability in abilities:
            if ability.id in Textures.abilitytexturemapping.keys():
                abilityimage = Textures.get_spritesheet(Textures.abilitytexturemapping[ability.id])[0]
                self.image.blit(abilityimage, Vec.comp_add2(self.abilityimagepos, (16*index, 2)), (0,0,16,16))
                if ability.phase >= 0:
                    self.image.fill(self.phasecolors[ability.phase], 
                        (*Vec.comp_add2(self.abilityphasepos, (16*index, 0)), 16, 20)
                    )
            if self.displayunit and unit == self.displayunit._parentelement:
                numberimage = self.font.render(str(index+1), True, (255,255,255,255))
                self.image.blit(numberimage, Vec.comp_add2(self.abilityphasepos, (16*index, 0)))
            index += 1


class Hud(pygame.sprite.Sprite):
    """The HUD is used to display most information, like HP, abilities, etc."""

    def __init__(self, width:int, height:int, gridui:GridUI, playerid:int, session:Session):
        super().__init__()
        #default colors
        self.defaultimagecolor = (30,0,0,255)
        self.defaulttextboxcolor = (50,50,50,255)

        self.image = pygame.Surface((width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.selectedunitui:UnitBaseUI = None
        self.gridui = gridui
        self.font = pygame.font.SysFont('latinmodernmono', 15)
        self.cursorgridpos = (0,0)
        self.cursorscreenpos = (0,0)

        self.unitdisplay = UnitDisplay()
        self.unitdisplayanchor = (.75,0)
        self.unitdisplay.rect.topleft = Vec.comp_mult2(self.unitdisplayanchor, self.gridui.rect.size) 
        self.hudsprites = pygame.sprite.Group(self.unitdisplay)
        # tile display
        self.tilefontdisplay = pygame.Surface((100,20)).convert_alpha()
        self.tileimagedisplay = pygame.Surface((64,64)).convert_alpha()
        self.tileimagedisplayanchor = (.75,.8)
        self.tilefontdisplayanchor = (.85,.8)
        # other info
        self.timerdisplay = pygame.Surface((96,20)).convert_alpha()
        self.hitpoint = pygame.Surface((16,16)).convert_alpha()
        self.hitpoint.fill((0,200,0,255))
        self.hitpointdisplay = pygame.Surface((20,20)).convert_alpha()
        self.hitpointdisplay.fill((0,0,0,255))
        
        self.playerid = playerid
        self.session = session
        self.backgrounds = []
        self.background = pygame.Surface((0,0)).convert_alpha()
        for bgname in Textures.backgroundtexturemapping.values():
            self.backgrounds.append(Textures.get_spritesheet(bgname)[0])
        
    
    def escape_pressed(self):
        """Tell the server that the player wants to leave."""
        NetEvents.snd_netplayerleave(self.session._players[self.playerid])

    def unitselect(self, position:"tuple[int,int]"):
        """Mark a unit as selected, displaying it's stats in greater detail and allowing ability use."""
        unitui = self.gridui.get_unitui(position)
        if unitui != self.selectedunitui:
            if self.selectedunitui and self.selectedunitui._parentelement:
                self.selectedunitui._parentelement.on_deselect()
        if unitui and unitui._parentelement:
            if unitui._parentelement.ownerid == self.playerid:
                self.selectedunitui = unitui
                unitui._parentelement.on_select()
            else:
                print(self.playerid, unitui._parentelement.ownerid)
        else:
            self.selectedunitui = None
        self.redraw()
    
    def targetselect(self, position:"tuple[int,int]"):
        """Forward the position of the selected target to the selected unit's hooks or spawn a unit."""
        if self.gridui.grid.phase == 0 and \
        len(self.session._players[self.playerid]._initialunitids) > 0 and\
        self.gridui.grid.is_space_empty(False, position):
            id = self.session._players[self.playerid]._initialunitids.pop(0)
            self.gridui.grid.request_add_unit(*position, id, self.playerid)
        elif self.selectedunitui:
            self.selectedunitui._parentelement.on_targets_chosen([position])
        self.redraw()

    def activate_ability(self, slot:int):
        """Activate the ability with the according number, and deselect all others."""
        if self.selectedunitui and self.selectedunitui._parentelement:
            self.selectedunitui._parentelement.on_deselect()
            self.selectedunitui._parentelement.on_activate_ability(slot-1)
            self.redraw()

    def display_unit(self, pos:"tuple[int,int]"):
        """Display the portrait, stats and other info of a unit."""
        unitui = self.gridui.uiunits[self.gridui.grid.c_to_i(pos)]
        self.unitdisplay.set_displayunit(unitui)
        if not unitui and self.selectedunitui:
            unitui = self.selectedunitui
            #self.display_healthbar(unitui._parentelement)
        self.hudsprites.draw(self.image)
        
    def display_healthbar(self, unit:UnitBase):
        """Display the health bar on top of a unit."""
        x,y = self.gridui.transform_grid_screen(unit.pos)
        barwidth = 32
        hitpoints = unit.hitpoints
        slotwidth = min(10, max(4, barwidth/max(1,hitpoints)))
        for hp in range(hitpoints):
            self.image.blit(self.hitpointdisplay,
                (x+32+slotwidth*hp-slotwidth/2*hitpoints,y-16),
                (0,0,slotwidth+2,8))
            self.image.blit(self.hitpoint, 
                (x+33+slotwidth*hp-slotwidth/2*hitpoints,y-15), 
                (0,0,slotwidth,6))
    
    def display_effects(self, pos:"tuple[int,int]"):
        """Display the effect the cursor is on."""
        effects = self.gridui.uieffects[self.gridui.grid.c_to_i(pos)]
        for effect in effects:
            if effect.visible:
                self.image.blit(effect.image, (self.gridui.width*.75, self.gridui.height*.75), (0,0,64,64))

    def display_tile(self, pos:"tuple[int,int]"):
        """Display the tile the cursor is on."""
        self.tilefontdisplay.fill(self.defaulttextboxcolor)
        self.tileimagedisplay.fill(self.defaultimagecolor)
        tile = self.gridui.uitiles[self.gridui.grid.c_to_i(pos)]
        effect = self.gridui.uieffects[self.gridui.grid.c_to_i(pos)]
        if tile and tile.visible:
            self.tilefontdisplay.blit(
                self.font.render(type(tile._parentelement).__name__, 
                True, 
                (255,255,255,255)), 
                (0,0)
            )
            self.tileimagedisplay.blit(tile.image, (0,0))
        self.image.blit(self.tileimagedisplay, Vec.comp_mult2(self.tileimagedisplayanchor, self.rect.size))
        self.image.blit(self.tilefontdisplay, Vec.comp_mult2(self.tilefontdisplayanchor, self.rect.size))

    def draw_unit_ability_previews(self, unit:UnitBase):
        """Draw previews of a unit, e.g. movement and targeting info."""
        for ability in unit.abilities:
            for previewinfo in ability.area_of_effect:
                pos, previewid = previewinfo
                screenpos = self.gridui.transform_grid_screen(pos)
                self.image.blit(Textures.get_spritesheet(previewid)[0], screenpos)
    
    def player_won(self, playerid:int):
        if self.playerid == playerid:
            print("\nI Won!\n")
        else:
            print("\nI Lost!\n")
    
    def redraw(self):
        """Update the internal image, so that no residual blits are seen."""
        self.background = self.backgrounds[self.gridui.grid.phase]
        self.image.fill((0,0,0,0))
        if self.selectedunitui and self.selectedunitui._parentelement:
            self.draw_unit_ability_previews(self.selectedunitui._parentelement)
        maxphasetime = PHASES[self.gridui.grid.phase][1]
        currentphasetime = self.gridui.grid.phasetime
        self.timerdisplay = self.font.render(str(round(maxphasetime-currentphasetime, 1)), True, (255,255,255,255))
        self.image.blit(Textures.get_spritesheet(PREVIEWS[0])[0], self.cursorscreenpos)
        self.image.blit(self.timerdisplay, (10,10))

        self.display_tile(self.cursorgridpos)
        self.display_effects(self.cursorgridpos)
        self.display_unit(self.cursorgridpos)

    def update_cursor(self, position:"tuple[int,int]"):
        """Forward the new cursor position to a unit's according hooks"""
        self.cursorgridpos = position
        self.cursorscreenpos = self.gridui.transform_grid_screen(position)
        if self.selectedunitui and self.selectedunitui._parentelement:
            self.selectedunitui._parentelement.on_update_cursor(position)
        self.redraw()
    