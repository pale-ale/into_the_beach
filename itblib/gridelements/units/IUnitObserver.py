from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from itblib.gridelements.StatusEffects import StatusEffect


class IUnitObserver(ABC):
    """Objects implementing this interface will receive updates from units they register with."""
    @abstractmethod
    def on_add_status_effect(self, added_effect:"StatusEffect"):
        """Called when a status effect has been added."""
    
    @abstractmethod
    def on_remove_status_effect(self, removed_effect:"StatusEffect"):
        """Called when a status effect has been removed."""
    
    @abstractmethod
    def on_update_position(self, new_pos:tuple[int,int]):
        """Called when a unit moves; not guaranteed to be a different tile."""
