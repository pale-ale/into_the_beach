from typing import TYPE_CHECKING
from itblib.abilities.AbilityBase import AbilityBase
from itblib.Globals.Enums import PREVIEWS
from itblib.net.NetEvents import NetEvents
if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class MovementAbility(AbilityBase):
    """
    Allows units to move around on the map. 
    
    Comes with a movement range and other mechanics, like being able to fly to pass over certain terrain,
    phase through walls and enemies etc.
    """

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 4, cooldown=0)
        self.timinginfo = unit.age
        self.remainingcooldown = 0
        self.durationperstep = .5 #seconds
    
    def on_select_ability(self):
        super().on_select_ability()
        if self.selected:
            self._collect_movement_info()

    def set_targets(self, targets:"list[tuple[int,int]]"):
        super().set_targets(targets)
        if not NetEvents.connector.authority:
            self._collect_movement_info()
    
    def on_update_cursor(self, newcursorpos:"tuple[int,int]"):
        """Add the new cursor position to the path if the unit can move there."""
        super().on_update_cursor(newcursorpos)
        if self.selected:
            if len(self.selected_targets) < self._unit.moverange:
                self._add_to_movement(newcursorpos)
            else:
                self.on_deselect_ability()
    
    def on_trigger(self):
        """Trigger effects based on the movement of this unit, and set the timing for animation."""
        super().on_trigger()
        self.timinginfo = self._unit.age
        self._unit.done = False
  
    def get_valid_targets(self) -> "list[tuple[int,int]]":
        pathwithself = [self._unit.pos] + self.selected_targets
        valid_targets = self._unit.grid.get_ordinal_neighbors(pathwithself[-1]) 
        return valid_targets

    def _collect_movement_info(self):
        """Gather the tiles we can move to and add them to the displayed AOE."""
        pathwithself = [self._unit.pos] + self.selected_targets
        if len(pathwithself) <= self._unit.moverange:
            pos = pathwithself[-1]
            for neighbor in self.get_valid_targets():
                delta = (neighbor[0] - pos[0], neighbor[1] - pos[1])
                coordwithpreviewid = (neighbor, PREVIEWS[delta])
                self.area_of_effect.append(coordwithpreviewid)

    def _update_path_display(self):
        """Display the new path using proximity textures."""
        self.area_of_effect.clear()
        pathwithself = [self._unit.pos]
        pathwithself.extend(self.selected_targets)
        if len(pathwithself) > 1:
            first = (pathwithself[0], PREVIEWS[1])
            last = (pathwithself[-1], PREVIEWS[1])
            for i in range(1, len(pathwithself)-1):
                prev = pathwithself[i-1]
                curr = pathwithself[i]
                next = pathwithself[i+1]
                prevdelta = (curr[0] - prev[0], curr[1] - prev[1])
                nextdelta = (next[0] - curr[0], next[1] - curr[1])
                currentwithpreview = (curr, PREVIEWS[(*nextdelta, *prevdelta)])
                self.area_of_effect.append(currentwithpreview)
            self.area_of_effect.append(first)
            self.area_of_effect.append(last)
        self._collect_movement_info()

    def _add_to_movement(self, target:"tuple[int,int]"):
        """Add a "step" to the path we want to take."""
        pathwithself = [self._unit.pos]
        pathwithself.extend(self.selected_targets)
        if target != pathwithself[-1]:
            new_targets = self.selected_targets + [target]
            self.set_targets(new_targets)
            if not NetEvents.connector.authority:
                self._update_path_display()
