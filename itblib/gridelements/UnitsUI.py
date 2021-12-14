from typing import TYPE_CHECKING, Generator

import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.net.NetEvents import NetEvents
from itblib.ui.HealthBar import HealthBar
from itblib.ui.hud.OwnerColorRhombus import OwnerColorRhombus
from itblib.ui.IDisplayable import IDisplayable
from itblib.Vec import add, scalar_mult, sub

from .GridElementUI import GridElementUI

if TYPE_CHECKING:
    from itblib.ui.GridUI import GridUI

class UnitBaseUI(GridElementUI, IDisplayable):
    def __init__(self, unit:UnitBase, global_transform:pygame.Rect):
        GridElementUI.__init__(self, parentelement=unit, global_transform=global_transform, direction="SW", framespeed=.5)
        self._tfc = self.get_component(TransformComponent)
        if self._tfc:
            self._tfc.relative_position = global_transform.center
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
        self.healthbar.tfc.relative_position = (0,15)
        self.owner_color_rhombus = OwnerColorRhombus(NetEvents.session._players[self._parentelement.ownerid].color)
        self.owner_color_rhombus.attach_to_unit(self)
    
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
            interp_screenpos = add(self.fromscreenpos, scalar_mult(timepercent, diff))
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
        yield from self.owner_color_rhombus.get_blits()
        yield from super().get_blits()
        yield from self.healthbar.get_blits()


class UnitKnightUI(UnitBaseUI):
    def get_display_name(self) -> str:
        return "Knight"
    