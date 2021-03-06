"""Contains the base class of the ability system's abilities."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from itblib.Vec import IVector2
from itblib.abilities.ui_abilities import AbilityBaseUI

from itblib.input.Input import InputAcceptor
from itblib.Log import log
from itblib.net.NetEvents import NetEvents
from itblib.Serializable import Serializable

if TYPE_CHECKING:
    from itblib.components import AbilityComponent
    from itblib.gridelements.units.UnitBase import UnitBase


class AbilityBase(Serializable, InputAcceptor, ABC):
    """
    The base class for all the other abilities.
    Abilities are used to provide unique actions to units.
    They usually come with an active phase during which they can proc,
    a cost, cooldowns and other mechanics.
    """

    def __init__(self, owning_component:"AbilityComponent", phase:int, cooldown=1):
        Serializable.__init__(self, ["name", "selected_targets", "primed", "remainingcooldown"])
        InputAcceptor.__init__(self)
        self._owning_component = owning_component
        self.observer:"AbilityBaseUI|None" = None
        self.phase = phase
        self.cooldown = cooldown
        self.primed = False
        self.selected = False
        self.needstarget = False
        self.trigger_causes_cooldown = True
        self.reduce_cooldown_each_turn = True
        self.area_of_effect:"list[tuple[IVector2,str]]" = []
        self.selected_targets:"list[IVector2]" = []
        self.remainingcooldown = 0

    def get_owner(self) -> "UnitBase|None":
        """Returns the ComponentAcceptor associated with this abilty's AbilityComponent."""
        return self._owning_component.owner if self._owning_component else None

    def tick(self, delta_time:float):
        """Override to be executed every tick."""

    def on_trigger(self):
        """Called when the ability gets proc'd. Make units take damage, shove them etc."""
        if self.trigger_causes_cooldown:
            self.remainingcooldown = self.cooldown
            self.primed = False
        log(f"AbilityBase: Triggered {type(self.get_owner()).__name__}'s {type(self).__name__}", 0)
        if self.observer: 
            self.observer.on_trigger()

    def set_targets(self, targets:"list[IVector2]"):
        """Set selected_targets to the specified coordinates."""
        self.selected_targets = targets
        log(f"AbilityBase: Set targets of {type(self).__name__} to {targets}", 0)

    def confirm_target(self, target: IVector2, primed=True):
        """Called when the players confirms the target(s) with ENTER,
        passing along the position where the cursor was when ENTER was pressed"""
        assert isinstance(target, IVector2)
        self.primed = primed
        NetEvents.snd_netabilitytarget(self)
        log(f"AbilityBase: Confirmed targets of {type(self).__name__}: {self.selected_targets}", 0)

    def reset(self):
        """Reset the ability to e.g. remove old targeting info."""
        self.selected_targets.clear()
        self.area_of_effect.clear()
        self.primed = False
        self.selected = False

    def reset_to_targets(self):
        """Remove the ability's previews, keeping the selected targets"""
        self.area_of_effect = list(filter(lambda e: e[0] in self.selected_targets, self.area_of_effect))
        for e in self.area_of_effect:
            assert isinstance(e, tuple)

    def on_select_ability(self):
        """Called when a player selects this ability. Use to e.g. show target outlines"""
        self.reset()
        if self._owning_component:
            self._owning_component.targeting_ability = True
        self.selected = True
        log(f"AbilityBase: Selected {type(self).__name__}", 0)

    def on_deselect_ability(self):
        """Called when the ability is not selected any longer, e.g. by selecting a different one."""
        self.selected = False
        self.reset_to_targets()
        log(f"AbilityBase: Deselected {type(self).__name__}", 0)

    def on_parentunit_select(self):
        """Called when the unit has been selected (not as a target)."""
        log("AbilityBase: My parent was selected.", 0)

    def on_parentunit_deselect(self):
        """Called when the unit was deselected (not as a target)."""
        log("AbilityBase: My parent was deselected.", 0)
        self.on_deselect_ability()

    def on_update_cursor(self, newcursorpos):
        """Called when the player changes the cursor's position while this ability is active."""
        log(f"AbilityBase: User moved cursor to {newcursorpos}", 0)

    def on_update_phase(self, newphase:int):
        """Called when a phase change occured. Not necessarily a new turn."""
        if newphase == 1:
            self.reset()
            if self.reduce_cooldown_each_turn:
                self.remainingcooldown = max(self.remainingcooldown-1, 0)
        if self.phase == newphase and self.primed:
            self.on_trigger()

    def on_death(self):
        """Called when this ability's unit dies."""
        log("AbilityBase: This unit has died.", 0)

    @abstractmethod
    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        """Return a set of valid target coordinates."""

    def _is_valid_target(self, target:"tuple[int,int]") -> bool:
        """Determine whether a target is valid (e.g. in range) or not."""
        return target in self._get_valid_targets()

    def extract_data(self, custom_fields: "dict[str,any]" = ...) -> dict:
        custom_fields = {"name":type(self).__name__, "selected_targets":[v.c for v in self.selected_targets]}
        return super().extract_data(custom_fields=custom_fields)
