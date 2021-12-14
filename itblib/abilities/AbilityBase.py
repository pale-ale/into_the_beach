from typing import TYPE_CHECKING

from itblib.input.Input import InputAcceptor
from itblib.net.NetEvents import NetEvents
from itblib.Serializable import Serializable

if TYPE_CHECKING:
    from itblib.components.AbilityComponent import AbilityComponent
    from itblib.gridelements.units.UnitBase import UnitBase


class AbilityBase(Serializable, InputAcceptor):
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
        self.phase = phase
        self.cooldown = cooldown
        self.primed = False
        self.selected = False
        self.needstarget = False
        self.trigger_causes_cooldown = True
        self.reduce_cooldown_each_turn = True
        self.area_of_effect:"list[tuple[tuple[int,int],str]]" = []
        self.selected_targets:"list[tuple[int,int]]" = []
        self.remainingcooldown = 0
        self._owning_component.targeting_ability = True
    
    def get_owner(self) -> "UnitBase|None":
        return self._owning_component.owner
    
    def tick(self, dt:float):
        """Made to be overridden."""
        pass

    def on_trigger(self):
        """Called when the ability gets proc'd. Make units take damage, shove them etc."""
        if self.trigger_causes_cooldown:
            self.remainingcooldown = self.cooldown
            self.primed = False
        print("AbilityBase: Triggered", type(self._owning_component.owner).__name__ + "'s", type(self).__name__)
    
    def set_targets(self, targets:"list[tuple[int,int]]"):
        """Set selected_targets to the specified coordinates."""
        self.selected_targets = targets
        print("AbilityBase: Set targets of", type(self).__name__, "to", targets)
    
    def confirm_target(self, target:"tuple[int,int]", primed=True):
        """Called when the players confirms the target(s) with ENTER, 
        passing along the position where the cursor was when ENTER was pressed"""
        self.primed = primed
        NetEvents.snd_netabilitytarget(self)
        print("AbilityBase: Confirmed targets of", type(self).__name__, ":", self.selected_targets)

    def reset(self):
        """Reset the ability to e.g. remove old targeting info."""
        self.selected_targets.clear()
        self.area_of_effect.clear()
        self.primed = False
        self.selected = False

    def on_select_ability(self):
        """Called when a player selects this ability. Use to e.g. show target outlines"""
        self.reset()
        self.selected = True
        print("AbilityBase: Selected", type(self).__name__)
    
    def on_deselect_ability(self):
        """Called when the ability is not selected any longer, e.g. by selecting a different one."""
        self.selected = False
        self.area_of_effect.clear()
        print("AbilityBase: Deselected", type(self).__name__)
    
    def on_parentunit_select(self):
        """Called when the unit has been selected (not as a target)."""
        print("AbilityBase: My parent was selected.")
    
    def on_parentunit_deselect(self):
        """Called when the unit was deselected (not as a target)."""
        print("AbilityBase: My parent was deselected.")
        self.on_deselect_ability()
    
    def on_update_cursor(self, newcursorpos):
        """Called when the player changes the cursor's position while this ability is active."""
        print("AbilityBase: User moved cursor to", newcursorpos)

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
        print("AbilityBase: This unit has died.")
    
    def get_valid_targets(self) -> "list[tuple[int,int]]":
        """Return a list of valid target coordinates."""
        print("AbilityBase: Please override.")
    
    def is_valid_target(self, target:"tuple[int,int]") -> bool:
        """Determine whether a target is valid (e.g. in range) or not."""
        return target in self.get_valid_targets()
    
    def extract_data(self, custom_fields: "dict[str,any]" = ...) -> dict:
        return super().extract_data(custom_fields={"name":type(self).__name__, "selected_targets":self.selected_targets})
