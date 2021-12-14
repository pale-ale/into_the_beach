from abc import ABC
from typing import Callable, Optional

class DamageReceiver(ABC):
    def __init__(self, max_hp:int, current_hp:int):
        self._max_hitpoints = max_hp
        self._hitpoints = current_hp
        self.resistances = {"physical": 0, "magical": 0, "collision": 0}
        self._hp_update_callback:Optional[Callable[[int],None]] = None
    
    def change_hp(self, delta_hp:int, hp_change_type:str):
        """Change hp by amount. Influenced by resistances etc.."""
        true_delta = min(delta_hp, self._max_hitpoints)
        if true_delta < 0:
            true_delta = min(0, true_delta + self.resistances[hp_change_type])
        self.set_hp(self._hitpoints + true_delta)

    def set_hp(self, hp:int):
        self._hitpoints = hp
        if self._hp_update_callback:
            self._hp_update_callback(self._hitpoints)
        if self._hitpoints <= 0:
            self.on_death()
    
    def set_hp_update_callback(self, callback:Optional[Callable[[int],None]]):
        self._hp_update_callback = callback
        callback(self._hitpoints)

    def on_death():
        pass