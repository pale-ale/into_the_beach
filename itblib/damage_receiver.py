"""Introduces healthpoint related behaviour"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

class DamageReceiver:
    """Adds methods which modify and retrieve healthpoints"""
    def __init__(self, max_hp:int, current_hp:int):
        self._max_hitpoints = max_hp
        self._hitpoints = current_hp
        self.resistances = {"physical": 0, "magical": 0, "collision": 0}

    @property
    def hitpoints(self):
        """The amount of damage a unit can take before dying."""
        return self._hitpoints

    @hitpoints.setter
    def hitpoints(self, new_hitpoints:int):
        """Set hp to a certain amount."""
        self._hitpoints = new_hitpoints
        if self._hp_update_callback:
            self._hp_update_callback(self._hitpoints)
        if self._hitpoints <= 0:
            self.on_death()

    @property
    def hp_update_callback(self):
        """A function to be called when the hp amount changes."""
        return self._hp_update_callback

    @hp_update_callback.setter
    def hp_update_callback(self, callback:"Callable[[int],None]|None"):
        """Set the callback used when a hp change occurs. Calls the callback once."""
        self._hp_update_callback = callback
        callback(self._hitpoints)

    def change_hp(self, delta_hp:int, hp_change_type:str):
        """Change hp by amount. Influenced by resistances etc.."""
        true_delta = min(delta_hp, self._max_hitpoints)
        if true_delta < 0:
            true_delta = min(0, true_delta + self.resistances[hp_change_type])
        self.hitpoints = self._hitpoints + true_delta

    def on_death(self):
        """Called when this unit dies."""
