"""
Status Effects are bound to a unit or a tile, usually affecting them each turn.
"""

from typing import TYPE_CHECKING
from itblib.Serializable import Serializable
from itblib.ui.IDisplayable import IDisplayable
from itblib.globals.Enums import PHASES

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class StatusEffectBase(Serializable, IDisplayable):
    """The base class for any StatusEffect"""
    def __init__(self, target:"UnitBase", name:str, trigger_phase:int, duration:int):
        super().__init__(["name"])
        self.target = target
        self.name = name
        self.trigger_phase = trigger_phase
        self.duration = duration

    def on_update_phase(self, newphase:int):
        """Triggers when the phase changes, reducing remaining duration by 1"""
        if newphase == self.trigger_phase:
            self.on_proc()
            if self.duration is not None:
                self.duration = max(0, self.duration-1)

    def on_spawn(self):
        """Triggers when the status effect is created and attached"""

    def on_proc(self):
        """
        Triggers when the status effect is proc'd, i.e. define what the ability does every turn here
        """

    def on_purge(self):
        "Triggers when the effect is removed from a unit"

    def get_display_name(self) -> str:
        return self.name


class StatusEffectBleeding(StatusEffectBase):
    """Deals 1 damage each turn."""
    def __init__(self, target: "UnitBase"):
        super().__init__(target, name="Bleeding", trigger_phase=PHASES.BATTLEPHASE, duration=3)

    def on_proc(self):
        self.target.change_hp(-1, "physical")

    def get_display_description(self) -> str:
        return "Will deal 1 damage every battle phase."


class StatusEffectBurrowed(StatusEffectBase):
    """Prevents movement."""
    def __init__(self, target: "UnitBase"):
        super().__init__(target, name="Burrowed", trigger_phase=-1, duration=-1)
        self.original_shove = target.on_receive_shove
        self.original_moverange = target.get_movement_ability().moverange
        target.get_movement_ability().moverange = 0
        target.on_receive_shove = self.disabled_shove

    def disabled_shove(self, pos):
        "Placeholder method to disable the unit's standard shove method"

    def on_purge(self):
        self.target.on_receive_shove = self.original_shove
        self.target.get_movement_ability().moverange = self.original_moverange

    def get_display_description(self) -> str:
        return "Burrowed entities cannot be pushed."


class StatusEffectDreadfulNoise(StatusEffectBase):
    """Reduces a unit's physical damage to 0 for 2 turns."""
    def __init__(self, target: "UnitBase"):
        super().__init__(target, name="DreadfulNoise", trigger_phase=-1, duration=2)
        self.removed_attack = 0

    def on_spawn(self):
        self.removed_attack = self.target.baseattack["physical"]
        self.target.baseattack["physical"] -= self.removed_attack

    def on_purge(self):
        self.target.baseattack["physical"] += self.removed_attack

    def get_display_description(self) -> str:
        return "Causes a unit to cower in fear, taking more damage from attacks."
