from typing import TYPE_CHECKING
from itblib.abilities.AbilityBase import AbilityBase
from itblib.Enums import PREVIEWS
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
        super().__init__(unit)
        self.id = 0
        self.phase = 4
        self.timinginfo = unit.age
        self.cooldown = 0
        self.remainingcooldown = 0
        self.durationperstep = .5 #seconds
    
    def on_select_ability(self):
        super().on_select_ability()
        if  self.selected:
            self.area_of_effect.clear()
            self.selected_targets.clear()
            self.collect_movement_info()

    def collect_movement_info(self):
        """Gather the tiles we can move to and add them to the displayed AOE."""
        pathwithself = [self._unit.pos] + self.selected_targets
        if len(pathwithself) <= self._unit.moverange:
            pos = pathwithself[-1]
            for neighbor in self._unit.grid.get_ordinal_neighbors(*pos):
                delta = (neighbor[0] - pos[0], neighbor[1] - pos[1])
                coordwithpreviewid = (neighbor, PREVIEWS[delta])
                self.area_of_effect.append(coordwithpreviewid)

    def add_targets(self, targets:"list[tuple[int,int]]"):
        """Handle the user's target selection."""
        super().add_targets(targets)
        for target in targets:
            if len(self.selected_targets) >= self._unit.moverange:
                return
            self.add_to_movement(target)
            if not NetEvents.connector.authority:
                self.collect_movement_info()
        self.on_deselect_ability()
    
    def update_path_display(self):
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
        self.collect_movement_info()

    def add_to_movement(self, target:"tuple[int,int]"):
        """Add a "step" to the path we want to take."""
        pathwithself = [self._unit.pos]
        pathwithself.extend(self.selected_targets)
        if target != pathwithself[-1]:
            self.selected_targets.append(target)
            NetEvents.snd_netabilitytarget(self)
            if not NetEvents.connector.authority:
                self.update_path_display()

    def on_update_cursor(self, newcursorpos:"tuple[int,int]"):
        """Add the new cursor position to the path if we can move there."""
        super().on_update_cursor(newcursorpos)
        if self.selected:
            if len(self.selected_targets) < self._unit.moverange:
                self.add_to_movement(newcursorpos)
            else:
                self.on_deselect_ability()
    
    def activate(self):
        """Trigger effects based on the movement of this unit, and set the timing for animation."""
        super().activate()
        self.timinginfo = self._unit.age
        self._unit.done = False
