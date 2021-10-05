import pygame
import pygame.sprite
import pygame.transform
import pygame.font
import pygame.image
from itblib.ui.TextureManager import Textures
from itblib.Globals.Enums import PHASES, PREVIEWS
from itblib.gridelements.UnitsUI import UnitBaseUI
from itblib.gridelements.TilesUI import TileBaseUI
from itblib.gridelements.EffectsUI import EffectBaseUI
from itblib.ui.GridUI import GridUI
from itblib.Game import Session
from itblib.Vec import Vec
from itblib.gridelements.units.UnitBase import UnitBase
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
        self.rect = pygame.Rect(0,0,200,116)
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
            self.display_statuseffects(unit._parentelement)
    
    def update(self):
        self.image.fill(self.defaultimagecolor, (*self.imagepos,64,64))
        if self.displayunit:
            self.image.blit(self.displayunit.image, Vec.comp_add2(self.imagepos, (0,10)))
    
    def display_statuseffects(self, unit:UnitBase):
        self.image.fill((0), (0,100,200,16))
        for i in range(len(unit.statuseffects)):
            texkey = unit.statuseffects[i].name+"Icon"
            spritesheet = Textures.get_spritesheet(texkey)
            if spritesheet:
                self.image.blit(spritesheet[0], (i,100))
            else:
                print(f"HUD: Texture {texkey} not found.")
                self.image.fill((255,0,255), (i,100,32,32))

    def display_abilities(self, unit:UnitBase):
        """Display the abilities of a unit."""
        abilities = unit.abilities
        index = 0
        for ability in abilities:
            if type(ability).__name__ in Textures.abilitytexturemapping.values():
                abilityimage = Textures.get_spritesheet(type(ability).__name__)[0]
                self.image.blit(abilityimage, Vec.comp_add2(self.abilityimagepos, (16*index, 2)), (0,0,16,16))
                if ability.phase >= 0:
                    if ability.remainingcooldown > 0:
                        self.image.fill((100,100,100,255), 
                            (*Vec.comp_add2(self.abilityphasepos, (16*index, 0)), 16, 20)
                        )
                    else:
                        self.image.fill(self.phasecolors[ability.phase], 
                            (*Vec.comp_add2(self.abilityphasepos, (16*index, 0)), 16, 20)
                        )
            else:
                print(f"HUD: Texture {type(ability).__name__} not found.")
            if self.displayunit and unit == self.displayunit._parentelement:
                numberimage = self.font.render(str(index+1), True, (255,255,255,255))
                self.image.blit(numberimage, Vec.comp_add2(self.abilityphasepos, (16*index, 0)))
            index += 1


class TileDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagepos = (0,0)
        self.titlepos = (64,0)
        self.defaultimagecolor = (30,0,0,255)
        self.defaulttextboxcolor = (50,50,50,255)
        self.font = pygame.font.SysFont('latinmodernmono', 15)
        self.rect = pygame.Rect(0,0,200,100)
        self.image = pygame.Surface(self.rect.size).convert_alpha()
        self.image.fill((0))
        self.displaytile:TileBaseUI = None
        self.displayeffects:"list[EffectBaseUI]" = None
        self.set_displaytile_effects(None, None)

    def set_displaytile_effects(self, tile:TileBaseUI, effects:"list[EffectBaseUI]"):
        """Set the new tile and effects to display."""
        self.displaytile = tile
        self.displayeffects = effects
        
    def update(self):
        self.image.fill(self.defaultimagecolor, (*self.imagepos,64,64))
        self.image.fill(self.defaulttextboxcolor, (*self.titlepos,128,20))
        if self.displaytile:
            self.image.blit(
                self.font.render(
                    type(self.displaytile._parentelement).__name__, True, (255,255,255,255)
                ), 
                self.titlepos
            )
            self.image.blit(self.displaytile.image, self.imagepos)
        if self.displayeffects:
            for e in self.displayeffects:
                self.image.blit(e.image, self.imagepos)


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
        self.displayscale = 2
        self.scaledpreviewtextures = {}
        for value in PREVIEWS.values():
            newtex = pygame.Surface(Vec.scalar_mult2((64,96), 2)).convert_alpha()
            pygame.transform.scale(
                Textures.get_spritesheet(value)[0],
                newtex.get_size(),
                newtex
            )
            self.scaledpreviewtextures[value] = newtex
        self.unitdisplay = UnitDisplay()
        self.tiledisplay = TileDisplay()
        self.unitdisplayanchor = (.85,0)
        self.tiledisplayanchor = (.85,.85)
        self.unitdisplay.rect.topleft = Vec.comp_mult2(self.unitdisplayanchor, self.rect.size) 
        self.tiledisplay.rect.topleft = Vec.comp_mult2(self.tiledisplayanchor, self.rect.size) 
        self.hudsprites = pygame.sprite.Group(self.unitdisplay, self.tiledisplay)
        # other info
        self.timerdisplay = pygame.Surface((96,20)).convert_alpha()
        
        self.playerid = playerid
        self.session = session
        self.backgrounds = []
        self.background = pygame.Surface((0,0)).convert_alpha()
        for bgname in Textures.backgroundtexturemapping.values():
            s = pygame.Surface((width, height))
            pygame.transform.scale(Textures.get_spritesheet(bgname)[0], s.get_size(), s)
            self.backgrounds.append(s)
    
    def transform_grid_true(self, pos:"tuple[int,int]"):
        """Transform incorporates pannening and scale"""
        unscaled = self.gridui.transform_grid_screen(pos)
        scaled = Vec.scalar_mult2(unscaled, self.displayscale)
        return Vec.comp_add2(self.gridui.pan, scaled)
    
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
    
    def targetconfirm(self, position:"tuple[int,int]"):
        """Forward the position of the selected target to the selected unit's hooks or spawn a unit."""
        if self.gridui.grid.phase == 0 and \
        len(self.session._players[self.playerid]._initialunitids) > 0 and\
        self.gridui.grid.is_space_empty(False, position):
            id = self.session._players[self.playerid]._initialunitids.pop(0)
            self.gridui.grid.request_add_unit(position, id, self.playerid)
        elif self.selectedunitui:
            self.selectedunitui._parentelement.on_confirm_target(position)
        self.redraw()

    def activate_ability(self, slot:int):
        """Activate the ability with the according number, and deselect all others."""
        if self.selectedunitui and self.selectedunitui._parentelement and self.gridui.grid.phase == 1:
            self.selectedunitui._parentelement.on_deselect()
            self.selectedunitui._parentelement.on_activate_ability(slot-1)
            self.redraw()

    def display_healthbar(self, unit:UnitBase):
        """Display the health bar on top of a unit."""
        #x,y = self.transform_grid_screen_scaled(Vec.comp_add2(unit.pos, [32,0]))
        maxbarwidth = 100
        hitpoints = unit._hitpoints
        slotwidth = (maxbarwidth - hitpoints -1) / max(1, hitpoints)
        barwidth = min(maxbarwidth, 10*max(1, hitpoints))
        #self.image.fill((0,0,255,255), (50, 50, barwidth, 20))
        for hp in range(hitpoints):
            self.image.fill(
                (50,255,50),
                (
                    51 + slotwidth*hp + hp, 
                    51,
                    slotwidth,
                    18
                )
            )

    def draw_unit_ability_previews(self, unit:UnitBase):
        """Draw previews of a unit, e.g. movement and targeting info."""
        for ability in unit.abilities:
            for previewinfo in ability.area_of_effect:
                pos, previewid = previewinfo
                screenpos = self.transform_grid_true(pos)
                self.image.blit(self.scaledpreviewtextures[previewid], screenpos)
    
    def player_won(self, playerid:int):
        if self.playerid == playerid:
            print("\nI Won!\n")
        else:
            print("\nI Lost!\n")
        self.gridui.grid.units.clear()        
        self.gridui.grid.tiles.clear()        
        self.gridui.grid.worldeffects.clear()
        self.gridui.grid.uniteffects.clear()
        self.gridui.reload_from_grid()

    def redraw(self):
        """Update the internal image, so that no residual blits are seen."""
        self.background = self.backgrounds[self.gridui.grid.phase]
        self.image.fill((0,0,0,0))
        if self.selectedunitui and self.selectedunitui._parentelement:
            self.draw_unit_ability_previews(self.selectedunitui._parentelement)
        self.hudsprites.update()
        self.hudsprites.draw(self.image)
        maxphasetime = PHASES[self.gridui.grid.phase][1]
        currentphasetime = self.gridui.grid.phasetime
        self.timerdisplay = self.font.render(str(round(maxphasetime-currentphasetime, 1)), True, (255,255,255,255))
        self.image.blit(self.scaledpreviewtextures["SelectionPreview"], self.cursorscreenpos)
        self.image.blit(self.timerdisplay, (10,10))
        unit = self.gridui.grid.get_unit(self.cursorgridpos)
        self.image.fill((0,0,0,255), (50, 50, 100, 20))
        if unit:
            self.display_healthbar(unit)

    def update_cursor(self, position:"tuple[int,int]"):
        """Forward the new cursor position to a unit's according hooks"""
        self.tiledisplay.set_displaytile_effects(
            self.gridui.get_tileui(position),
            self.gridui.get_tile_effectsui(position)
        )
        self.unitdisplay.set_displayunit(self.gridui.get_unitui(position))
        self.cursorgridpos = position
        self.cursorscreenpos = self.transform_grid_true(position)
        if self.selectedunitui and self.selectedunitui._parentelement:
            self.selectedunitui._parentelement.on_update_cursor(position)
        self.redraw()
    