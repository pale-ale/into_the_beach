"""Contains the ObjectiveAbility class."""

from typing import TYPE_CHECKING

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.net.NetEvents import NetEvents

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class ObjectiveAbility(AbilityBase):
    """This ability makes a unit an "Objective", meaning the player loses if it dies."""
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 0, 0)

    def on_death(self):
        super().on_death()
        NetEvents.session.objective_lost(self.get_owner().ownerid)

    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        return set()
