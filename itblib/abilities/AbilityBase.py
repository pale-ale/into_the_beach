from itblib.gridelements.UnitsUI import UnitBaseUI
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class AbilityBase:
    """
    The base class for all the other abilities.
    Abilities are used to provide unique actions to units.
    They usually come with an active phase during which they are proc'd,
    a cost, cooldowns and other mechanics.
    """

    def __init__(self, unit:"UnitBase"):
        self._unit = unit
        self.needstarget = False
        self.area_of_effect:"list[tuple[tuple[int,int],int]]" = []
        self.selected_targets:"list[tuple[int,int]]" = []
        self.selected = False
        self.id = -1
        self.cooldown = 1
        self.remainingcooldown = 0
        self.phase = -1
    
    def tick(self, dt:float):
        """Made to be overridden."""
        pass
    
    def activate(self):
        """Called when an ability gets proc'd."""
        print("Activated", type(self._unit).__name__ + "'s", type(self).__name__)
        self.remainingcooldown = self.cooldown
    
    def add_targets(self, targets):
        """Add target coordinates to selected_targets."""
        if self.selected:
            print("Targets chosen for " + type(self).__name__ + ":", targets)

    def on_select_ability(self):
        """Called when a player wants to use this ability."""
        if not self.selected and self.remainingcooldown == 0:
            self.selected = True
            print("Selected", type(self).__name__)
    
    def on_deselect_ability(self):
        """Called when the ability is not selected any longer, e.g. by selecting a different one."""
        if self.selected:
            self.selected = False
            self.area_of_effect.clear()
            print("Deselected", type(self).__name__)
    
    def on_parentunit_select(self):
        """Called when the unit has been selected (not as a target)."""
        print("My parent was selected.")
    
    def on_parentunit_deselect(self):
        """Called when the unit was deselected (not as a target)."""
        print("My parent was deselected.")
        self.on_deselect_ability()
    
    def on_update_cursor(self, newcursorpos):
        """Called when the player changes the cursor's position while this ability is active."""
        if self.selected:
            print("User moved cursor to", newcursorpos)

    def on_update_phase(self, newphase:int):
        """Called when a phase change occured. Not necessarily a new phase."""
        if newphase == self.phase:
            if self.remainingcooldown == 0:
                self.activate()
            else:
                self.remainingcooldown -= 1
    
    def on_death(self):
        """Called when this ability's unit dies."""
        print("This unit has died.")
