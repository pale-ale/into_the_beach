from typing import Generator

import pygame
import pygame.font
import pygame.image
import pygame.sprite
import pygame.transform
from itblib.Game import Session
from itblib.globals.Colors import BLACK, PHASECOLORS
from itblib.globals.Constants import HUD
from itblib.globals.Enums import PHASES
from itblib.gridelements.UnitsUI import UnitBaseUI
from itblib.input.Input import InputAcceptor
from itblib.net.NetEvents import NetEvents
from itblib.ui.animations.PlayerVersus import PlayerVersusAnimation
from itblib.ui.GridUI import GridUI
from itblib.ui.hud.TileDisplay import TileDisplay
from itblib.ui.hud.UnitDisplay import UnitDisplay
from itblib.ui.PerfSprite import PerfSprite
from itblib.ui.TextureManager import Textures
from itblib.Vec import add
from itblib.ui.hud.AbilityPreviewDisplay import AbilityPreviewDisplay

class Hud(PerfSprite, InputAcceptor):
    """The HUD is used to display most information, like HP, abilities, etc."""

    def __init__(self, size:"tuple[int,int]", gridui:GridUI, playerid:int, session:Session):
        PerfSprite.__init__(self)
        InputAcceptor.__init__(self)
        self.defaultimagecolor = (30,0,0,255)
        self.defaulttextboxcolor = (50,50,50,255)
        self.playerversusanimation:"PlayerVersusAnimation|None" = None
        self.rect = pygame.Rect(0,0,*size)
        self.selected_unitui:UnitBaseUI = None
        self.gridui = gridui
        self.gridui.phase_change_callback = lambda newphase: self.update_phase(newphase)
        self.font = pygame.font.SysFont('firamono', 22)
        self.cursorgridpos = (0,0)
        self.cursorscreenpos = (0,0)
        self.displayscale = 2
        self.unitdisplay = UnitDisplay()
        self.tiledisplay = TileDisplay()
        self.ability_preview_display = AbilityPreviewDisplay(gridui)
        self.unitdisplay.rect.topleft = (self.rect.width - HUD.ELEM_WIDTH, 0) 
        self.tiledisplay.rect.topleft = (0, 0)
        # other info
        self.playerid = playerid
        self.session = session
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        self.owner_blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        self.cursor_blit = None
    
    def update_phase(self, newphase:int):
        if newphase == 1:
            self.selected_unitui = None
            self.unitdisplay.set_displayunit(self.gridui.get_unitui(self.cursorgridpos))
    
    def handle_key_event(self, event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.targetconfirm(self.cursorgridpos)
                return True
            if event.key == pygame.K_SPACE:
                self.select_unit(self.gridui.get_unitui(self.cursorgridpos))
                return True
            if event.key == pygame.K_ESCAPE:
                if self.selected_unitui:
                    if self.selected_unitui._parentelement.ability_component.targeting_ability:
                        self.selected_unitui._parentelement.ability_component.on_deselect()
                        self.selected_unitui._parentelement.ability_component.on_select()
                    else:
                        self.select_unit(None)
                    return True
                else:
                    NetEvents.snd_netplayerleave(self.playerid)
                    return True
        return False      
    
    def select_unit(self, unitui:"UnitBaseUI|None"):
        """Mark a unit as selected, displaying it's stats in greater detail and allowing ability use."""
        if unitui != self.selected_unitui:
            if self.selected_unitui and self.selected_unitui._parentelement:
                self.selected_unitui._parentelement.ability_component.on_deselect()
        if unitui and unitui._parentelement:
            if unitui._parentelement.ownerid == self.playerid:
                self.selected_unitui = unitui
                unitui._parentelement.ability_component.on_select()
            else:
                print("not my unit")
        else:
            self.selected_unitui = None
    
    def targetconfirm(self, position:"tuple[int,int]"):
        """Forward the position of the selected target to the selected unit's hooks or spawn a unit."""
        if self.gridui.grid.phase == 0 and \
        len(self.session._players[self.playerid]._initialunitids) > 0 and\
        self.gridui.grid.is_space_empty(False, position):
            id = self.session._players[self.playerid]._initialunitids.pop(0)
            self.gridui.grid.request_add_unit(position, id, self.playerid)
        elif self.selected_unitui:
            self.selected_unitui._parentelement.ability_component.on_confirm_target(position)
            self.unitdisplay.set_displayunit(self.selected_unitui)

    def activate_ability(self, slot:int):
        """Activate the ability with the according number, and deselect all others."""
        if self.selected_unitui and self.selected_unitui._parentelement and self.gridui.grid.phase == 1:
            self.selected_unitui._parentelement.ability_component.on_deselect()
            self.selected_unitui._parentelement.ability_component.on_activate_ability(slot-1)
            self.unitdisplay.set_displayunit(self.selected_unitui)
    
    def get_unit_ability_preview_blits(self):
        """Retrieve ability previews blits of a unit, e.g. movement and targeting info."""
        for unit in self.gridui.grid.units:
            if unit:
                self.ability_preview_display.unit = unit
                yield from self.ability_preview_display.get_blits()
    
    def get_phase_timer_blit(self):
        maxphasetime = PHASES[self.gridui.grid.phase][1]
        currentphasetime = self.gridui.grid.phasetime
        s = self.font.render(str(round(max(0.0,maxphasetime-currentphasetime), 1)).zfill(4), True, (255,255,255,255), (255,50,50,255)).convert()
        c = self.session._players[self.playerid].color if self.playerid in self.session._players else (50,50,50,255)
        pygame.draw.line(s, c, (0,0), (s.get_width(),0), 1)
        pygame.draw.line(s, BLACK, (0,1), (s.get_width(), 1), 2)
        pygame.draw.line(s, BLACK, (0,s.get_height()-3), (s.get_width(),s.get_height()-3), 2)
        pygame.draw.line(s, PHASECOLORS[self.gridui.grid.phase], (0,s.get_height()-1), (s.get_width(),s.get_height()-1), 1)
        yield (s, pygame.Rect((self.rect.width - s.get_width())/2, 10, *s.get_size()), pygame.Rect(0,0,*s.get_size()))
    
    # def player_won(self, playerid:int):
    #     if self.playerid == playerid:
    #         print("\nI Won!\n")
    #     else:
    #         print("\nI Lost!\n")

    def _update_display_unit_if_necessary(self):
        gu = self.gridui.get_unitui(self.cursorgridpos)
        du = self.unitdisplay.displayunit
        if gu is not du:
            self.unitdisplay.set_displayunit(gu)

    def update_cursor(self, position:"tuple[int,int]"):
        """Forward the new cursor position to a unit's according hooks"""
        self.tiledisplay.set_displaytile_effects(
            self.gridui.get_tileui(position),
            self.gridui.get_tile_effectsui(position)
        )
        self.unitdisplay.set_displayunit(self.gridui.get_unitui(position))
        self.cursorgridpos = position
        self.cursorscreenpos = self.gridui.transform_grid_screen(position)
        if self.cursor_blit:
            self.blits.remove(self.cursor_blit)
        self.cursor_blit = (Textures.textures["SelectionPreview"][0], pygame.Rect(*self.cursorscreenpos,64,64), pygame.Rect(0,0,64,64))
        self.blits.append(self.cursor_blit)
        if self.selected_unitui and self.selected_unitui._parentelement:
            self.selected_unitui._parentelement.ability_component.on_update_cursor(position)
    
    def on_start_game(self):
        p1, p2 = self.session._players.values()
        self.playerversusanimation = PlayerVersusAnimation(p1, p2, *self.rect.size)
        self.playerversusanimation.start()
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits
        if self.playerversusanimation.playing:
            yield from self.playerversusanimation.get_blits()
        else:
            yield from self.get_phase_timer_blit()
            yield from self.tiledisplay.get_blits()
            yield from self.unitdisplay.get_blits()
        yield from self.get_unit_ability_preview_blits()

    def update(self, delta_time: float) -> None:
        if self.playerversusanimation:
            if self.playerversusanimation.animtime <= 3:
                self.playerversusanimation.update(delta_time)
            else:
                self.playerversusanimation.stop()
        self._update_display_unit_if_necessary()
        self.tiledisplay.update(delta_time)
        self.unitdisplay.update(delta_time)
