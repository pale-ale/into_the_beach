from itblib.abilities.base_abilities.cone_ability_base import \
    ConeAbilityBase
from itblib.gridelements.status_effect import StatusEffectDreadfulNoise


class DreadfulNoiseAbility(ConeAbilityBase):
    """A cone-targeted ability, weakening opponents and friendlies alike."""

    #pylint: disable=missing-function-docstring
    def apply_to_target(self, target: "tuple[int,int]"):
        owner = self.get_owner()
        targetunit = owner.grid.get_unit(target)
        if targetunit and targetunit != owner:
            dreadfulnoiseeffect = StatusEffectDreadfulNoise(targetunit)
            targetunit.add_status_effect(dreadfulnoiseeffect)
