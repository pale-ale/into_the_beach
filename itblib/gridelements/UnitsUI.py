from typing import TYPE_CHECKING, Generator

import pygame
from itblib.components.TransformComponent import TransformComponent
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.gridelements.Effects import EffectBurrowed, StatusEffect
from itblib.net.NetEvents import NetEvents
from itblib.ui.HealthBar import HealthBar
from itblib.ui.TextureManager import Textures
from itblib.ui.hud.OwnerColorRhombus import OwnerColorRhombus
from itblib.ui.IDisplayable import IDisplayable
from itblib.Vec import add, smult, sub

from .GridElementUI import GridElementUI

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class UnitBaseUI(GridElementUI, IDisplayable):
    def __init__(self, unit:"UnitBase", relative_position:tuple[int,int]):
        GridElementUI.__init__(self, parentelement=unit, global_transform=(0,0,*STANDARD_UNIT_SIZE), direction="SW", framespeed=.5)
        self._tfc = self.get_component(TransformComponent)
        if self._tfc:
            self._tfc.relative_position = relative_position
        self._parentelement:"UnitBase"
        self.fromscreenpos = None
        self.toscreenpos = None
        self.movementtime = 0.0
        self.speed = 0.0
        self.looping = True
        self.start()
        self.old_frame = self.framenumber
        self.healthbar = HealthBar(self._parentelement)
        self.healthbar.tfc.set_transform_target(self)
        self.healthbar.tfc.relative_position = (STANDARD_UNIT_SIZE[0]/2,STANDARD_UNIT_SIZE[1]*.8)
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
        if self.old_frame != self.framenumber:
            self.old_frame = self.framenumber
        if self.fromscreenpos and self.toscreenpos:
            diff = sub(self.toscreenpos, self.fromscreenpos)
            timepercent = min((self._parentelement.age - self.movementtime) / self.speed, 1)
            interp_screenpos = add(self.fromscreenpos, smult(timepercent, diff))
            self.global_transform.topleft = interp_screenpos
            self._tfc.relative_position = self.global_transform.center
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
        self.global_transform = pygame.Rect(self._tfc.get_position(), STANDARD_UNIT_SIZE)
        if self.owner_color_rhombus:
            yield from self.owner_color_rhombus.get_blits()
        yield from super().get_blits()
        yield from self.healthbar.get_blits()

    def on_add_statuseffect(effect:StatusEffect):
        pass
    
    def on_remove_statuseffect(effect:StatusEffect):
        pass


class UnitKnightUI(UnitBaseUI):
    def get_display_name(self) -> str:
        return "Knight"


class UnitBurrowerUI(UnitBaseUI):
    def get_display_name(self) -> str:
        return "Burrower"
    
    def on_add_statuseffect(self, effect: "StatusEffect"):
        if isinstance(effect, EffectBurrowed):
            self.set_textures(Textures.get_spritesheet("BurrowerSWBurrowed"))
            self.frametime = .15
   
    def on_remove_statuseffect(self, effect: "StatusEffect"):
        print("oyy")
        if isinstance(effect, EffectBurrowed):
            self.set_textures(Textures.get_spritesheet("BurrowerSWIdle"))
            self.frametime = .5
