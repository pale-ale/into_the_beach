from typing import TYPE_CHECKING
from itblib.Vec import IVector2

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.globals.Constants import DIRECTIONS, FLAGS, PREVIEWS
from itblib.net.NetEvents import NetEvents

if TYPE_CHECKING:
    from itblib.components import AbilityComponent

class MovementAbility(AbilityBase):
    """
    Allows units to move around on the map.

    Comes with a movement range and other mechanics,
    like being able to fly to pass over certain terrain,
    phase through walls and enemies etc.
    """

    def __init__(self, owning_component:"AbilityComponent"):
        super().__init__(owning_component=owning_component, phase=4, cooldown=0)
        self.moverange = 5
        self.remainingcooldown = 0
        self.durationperstep = .5 #seconds
        self.can_move = True
        self.can_be_moved = True
        self.movement_flags = FLAGS.MOVEMENT_DEFAULT

    def on_select_ability(self):
        super().on_select_ability()
        if self.selected:
            self._collect_movement_info()

    def set_targets(self, targets:"list[IVector2]"):
        super().set_targets(targets)
        if not NetEvents.connector.authority:
            self._collect_movement_info()

    def on_update_cursor(self, newcursorpos:"tuple[int,int]"):
        """Add the new cursor position to the path if the unit can move there."""
        super().on_update_cursor(newcursorpos)
        if self.selected:
            if len(self.selected_targets) < self.moverange and self._is_valid_target(newcursorpos):
                self._add_to_movement(newcursorpos)
            else:
                self.area_of_effect.clear()
                self.on_deselect_ability()

    def on_trigger(self):
        """Trigger effects based on the movement of this unit, and set the timing for animation."""
        super().on_trigger()
        self.get_owner().done = False

    def _can_move_at(self, pos:"tuple[int,int]") -> bool:
        tile = self.get_owner().grid.get_tile(pos)
        return tile and (tile.get_movement_requirements() & self.movement_flags)

    def _get_valid_targets(self):
        owner = self.get_owner()
        valid_targets = []
        if owner:
            pathwithself = [owner.position] + self.selected_targets
            test_targets = owner.grid.get_neighbors(pathwithself[-1])
            valid_targets = [t_pos for t_pos in test_targets if self._can_move_at(t_pos)]
        return valid_targets

    def _collect_movement_info(self):
        """Gather the tiles we can move to and add them to the displayed AOE."""
        owner = self.get_owner()
        pathwithself = [owner.position] + self.selected_targets
        if len(pathwithself) <= self.moverange:
            pos = pathwithself[-1]
            for neighbor in self._get_valid_targets():
                delta = neighbor - pos
                coordwithpreviewid = (neighbor, PREVIEWS[delta.c])
                self.area_of_effect.append(coordwithpreviewid)

    def _update_path_display(self):
        """Display the new path using proximity textures."""
        owner = self.get_owner()
        self.area_of_effect.clear()
        pathwithself = [owner.position]
        pathwithself.extend(self.selected_targets)
        if len(pathwithself) > 1:
            first = (pathwithself[0], PREVIEWS[1])
            last = (pathwithself[-1], PREVIEWS[1])
            for i in range(1, len(pathwithself)-1):
                prev_pos = pathwithself[i-1]
                curr_pos = pathwithself[i]
                next_pos = pathwithself[i+1]
                prevdelta = curr_pos - prev_pos
                nextdelta = next_pos - curr_pos
                currentwithpreview = (curr_pos, PREVIEWS[(nextdelta.c, prevdelta.c)])
                self.area_of_effect.append(currentwithpreview)
            self.area_of_effect.append(first)
            self.area_of_effect.append(last)
        self._collect_movement_info()

    def _add_to_movement(self, target:IVector2):
        """Add a "step" to the path we want to take."""
        assert isinstance(target, IVector2)
        owner = self.get_owner()
        pathwithself = [owner.position]
        pathwithself.extend(self.selected_targets)
        if target.c != pathwithself[-1]:
            new_targets = self.selected_targets + [target]
            self.set_targets(new_targets)
            if not NetEvents.connector.authority:
                self._update_path_display()

    def confirm_target(self, target: "tuple[int,int]", primed=True):
        super().confirm_target(target, primed=primed)
        self.on_deselect_ability()

    #pylint: disable=missing-function-docstring,attribute-defined-outside-init
    def on_deselect_ability(self):
        self.selected = False
        if self.primed:
            cardinals = {DIRECTIONS.NORTHEAST, DIRECTIONS.SOUTHEAST, 
                         DIRECTIONS.NORTHWEST, DIRECTIONS.SOUTHWEST}
            valid_preview_lambda = lambda p: not p[1] in {PREVIEWS[c] for c in cardinals}
            self.area_of_effect = list(filter(valid_preview_lambda, self.area_of_effect))
        else:
            self.reset()
