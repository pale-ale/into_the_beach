from typing import TYPE_CHECKING, Generator

import pygame
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.gridelements.StatusEffects import (StatusEffect,
                                               StatusEffectBurrowed)
from itblib.gridelements.units.IUnitObserver import IUnitObserver
from itblib.net.NetEvents import NetEvents
from itblib.ui.widgets.game_widget import HealthBar, OwnerColorRhombus
from itblib.ui.IDisplayable import IDisplayable
from itblib.ui.TextureManager import Textures
from itblib.Vec import add, smult, sub

from .GridElementUI import GridElementUI

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class UnitBaseUI(GridElementUI, IDisplayable, IUnitObserver):
    def __init__(self, unit:"UnitBase", direction="SW", framespeed=.5):
        GridElementUI.__init__(self, parentelement=unit, direction=direction, framespeed=framespeed)
        self._parentelement:"UnitBase"
        self.fromscreenpos = None
        self.toscreenpos = None
        self.movementtime = 0.0
        self.speed = 0.0
        self.old_frame = self.framenumber
        self.healthbar = HealthBar(self._parentelement)
        self.healthbar.parent = self
        barwidth = self.healthbar.get_size()[0]
        offset = ((STANDARD_UNIT_SIZE[0]-barwidth)/2,STANDARD_UNIT_SIZE[1]*.7)
        self.healthbar.position = offset
        self.owner_color_rhombus = None
        if NetEvents.session:
            self.owner_color_rhombus = OwnerColorRhombus(NetEvents.session._players[self._parentelement.ownerid].color)
            self.owner_color_rhombus.attach_to_unit(self)
        self._parentelement.observer = self
    
    def set_interp_movement(self, fromscreenpos:"tuple[int,int]", toscreenpos:"tuple[int,int]", speed:float):
        self.fromscreenpos = fromscreenpos
        self.toscreenpos = toscreenpos
        self.speed = speed
        self.movementtime = self._parentelement.age

    def update(self, delta_time:float):
        super().update(delta_time)
        if self.fromscreenpos and self.toscreenpos:
            diff = sub(self.toscreenpos, self.fromscreenpos)
            timepercent = min((self._parentelement.age - self.movementtime) / self.speed, 1)
            interp_screenpos = add(self.fromscreenpos, smult(timepercent, diff))
            self.tfc.relative_position = interp_screenpos
            if timepercent + 0e-4 >= 1:
                self.fromscreenpos = None
                self.toscreenpos = None
                self.movementtime = 0.0
                self.speed = 0.0
    
    def get_display_name(self) -> str:
        return "UnitBaseUI"
    
    def get_display_description(self) -> str:
        return "Another long description ------ weee------"
  
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        if self.owner_color_rhombus:
            yield from self.owner_color_rhombus.get_blits()
        yield from GridElementUI.get_blits(self)
        yield from self.healthbar.get_blits()
    
    def on_add_status_effect(self, added_effect: "StatusEffect"):
        pass

    def on_remove_status_effect(self, removed_effect: "StatusEffect"):
        pass

    def on_update_position(self, new_pos: tuple[int, int]):
        pass


class UnitKnightUI(UnitBaseUI):
    def __init__(self, unit: "UnitBase"):
        super().__init__(unit, framespeed=.1)

    def get_display_name(self) -> str:
        return "Knight"


class UnitBurrowerUI(UnitBaseUI):
    def get_display_name(self) -> str:
        return "Burrower"
    
    def on_add_status_effect(self, added_effect: "StatusEffect"):
        if isinstance(added_effect, StatusEffectBurrowed):
            self.set_textures(Textures.get_spritesheet("BurrowerSWBurrowed"))
            self.frametime = .15
   
    def on_remove_status_effect(self, removed_effect: "StatusEffect"):
        if isinstance(removed_effect, StatusEffectBurrowed):
            self.set_textures(Textures.get_spritesheet("BurrowerSWIdle"))
            self.frametime = .5


class UnitChipmonkUI(UnitBaseUI):
    def get_display_name(self) -> str:
        return "Chipmonk"
