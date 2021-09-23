from itblib.net.NetEvents import NetEvents
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class AbilityBase:
    """
    The base class for all the other abilities.
    Abilities are used to provide unique actions to units.
    They usually come with an active phase during which they can proc,
    a cost, cooldowns and other mechanics.
    """

    def __init__(self, unit:"UnitBase", id:int, phase:int, cooldown=1):
        self._unit = unit
        self.id = id
        self.phase = phase
        self.cooldown = cooldown
        self.primed = False
        self.selected = False
        self.needstarget = False
        self.trigger_causes_cooldown = True
        self.reduce_cooldown_each_turn = True
        self.area_of_effect:"list[tuple[tuple[int,int],int]]" = []
        self.selected_targets:"list[tuple[int,int]]" = []
        self.remainingcooldown = 0
    
    def tick(self, dt:float):
        """Made to be overridden."""
        pass

    def on_trigger(self):
        """Called when the ability gets proc'd. Make units take damage, shove them etc."""
        if self.trigger_causes_cooldown:
            self.remainingcooldown = self.cooldown
            self.primed = False
        print("AbilityBase: Triggered", type(self._unit).__name__ + "'s", type(self).__name__)
    
    def set_targets(self, primed:bool, targets:"list[tuple[int,int]]"):
        """Set selected_targets to the specified coordinates. Replicated."""
        self.selected_targets = targets
        self.primed = primed
        NetEvents.snd_netabilitytarget(self)
        print("AbilityBase: Set targets of", type(self).__name__, "to", targets)

    def on_select_ability(self):
        """Called when a player selects this ability. Use to e.g. show target outlines"""
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
        if self.phase == newphase and self.primed:
            self._unit.done = False
            self.on_trigger()
        elif self.reduce_cooldown_each_turn:
            self.remainingcooldown = max(self.remainingcooldown-1, 0)
    
    def on_death(self):
        """Called when this ability's unit dies."""
        print("AbilityBase: This unit has died.")
