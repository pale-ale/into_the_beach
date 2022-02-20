from itblib.abilities.baseAbilities.AbilityBase import AbilityBase


class TargetAbilityBase(AbilityBase):
    """Base class for any simple targeted ability, allowing for easy creation of such abilities."""

    def on_select_ability(self):
        super().on_select_ability()
    
    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        owner = self.get_owner()
        if owner:
            return owner.grid.get_neighbors(owner.pos)
        return set()
    
    def apply_to_target(self, target:"tuple[int,int]"):
        """Convenient override to act on each selected target."""
        pass

    def on_trigger(self):
        super().on_trigger()
        [self.apply_to_target(target) for target in self.selected_targets]

    def set_targets(self, targets:"list[tuple[int,int]]"):
        super().set_targets(targets)
        self.area_of_effect.clear()
        self.on_deselect_ability()
