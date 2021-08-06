from typing import TYPE_CHECKING
from .GridElementUI import GridElementUI
from .Units import UnitBase
if TYPE_CHECKING:
    from itblib.ui.GridUI import GridUI

class UnitBaseUI(GridElementUI):
    def __init__(self, unit:UnitBase):
        super().__init__(parentelement=unit, direction="SW")
        self._parentelement:"UnitBase"

    def update(self):
        super().update()
        if self._parentelement.grid.phase == 4:
            mov = self._parentelement.get_movement_ability()
            gridui:GridUI = self._parentelement.grid.observer
            if mov:
                dt = (self._parentelement.age - mov.timinginfo)*2
                waypoint = int(dt)
                if len(mov.selected_targets) > waypoint+1:
                    s = gridui.transform_grid_screen(mov.selected_targets[waypoint])
                    s = (s[0], s[1] + gridui.unitdrawoffset)
                    e = gridui.transform_grid_screen(mov.selected_targets[waypoint+1])
                    e = (e[0], e[1] + gridui.unitdrawoffset)
                    dist = (e[0] - s[0], e[1] - s[1])
                    interp_screenpos = (s[0] + int(dist[0]*(dt%1)), s[1] + int(dist[1]*(dt%1)))
                    self.rect.x, self.rect.y = interp_screenpos
