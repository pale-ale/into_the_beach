from itblib.Vec import Vec
from .GridElementUI import GridElementUI
from itblib.gridelements.units.UnitBase import UnitBase

class UnitBaseUI(GridElementUI):
    def __init__(self, unit:UnitBase):
        super().__init__(parentelement=unit, direction="SW")
        self._parentelement:"UnitBase"
        self.fromscreenpos = None
        self.toscreenpos = None
        self.movementtime = 0.0
        self.speed = 0.0
    
    def set_interp_movement(self, fromscreenpos:"tuple[int,int]", toscreenpos:"tuple[int,int]", speed:float):
        self.fromscreenpos = fromscreenpos
        self.toscreenpos = toscreenpos
        self.speed = speed
        self.movementtime = self._parentelement.age

    def update(self, dt:float):
        super().update(dt)
        if self.fromscreenpos and self.toscreenpos:
            diff = Vec.comp_sub2(self.toscreenpos, self.fromscreenpos)
            timepercent = min((self._parentelement.age - self.movementtime) / self.speed, 1)
            interp_screenpos = Vec.comp_add2(self.fromscreenpos, Vec.scalar_mult2(diff, timepercent))
            self.rect.x, self.rect.y = interp_screenpos
            if timepercent + 0e-4 >= 1:
                self.fromscreenpos = None
                self.toscreenpos = None
                self.movementtime = 0.0
                self.speed = 0.0
