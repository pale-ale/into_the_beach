from typing import Type, TypeVar

from itblib.abilities.baseAbilities.AbilityBase import AbilityBase
from itblib.components.ComponentBase import ComponentBase
from itblib.Log import log
from itblib.Serializable import Serializable

T = TypeVar('T', bound=AbilityBase)

class AbilityComponent(ComponentBase, Serializable):
    """
    Adds ability behaviour to a ComponentAcceptor. Contains the Abilities and various hooks to trigger for them."""
    def __init__(self, abilities: "list[Type[AbilityBase]]" = []) -> None:
        ComponentBase.__init__(self)
        Serializable.__init__(self, ["_abilities"])
        self._abilities: "list[AbilityBase]" = [
            ability(self) for ability in abilities]
        self.targeting_ability = False
    
    def extract_data(self, custom_fields: "dict[str,any]" = ...) -> dict:
        customabilities = [x.extract_data() for x in self._abilities]
        return Serializable.extract_data(self, custom_fields={"_abilities":customabilities})
    
    def insert_data(self, data):
        Serializable.insert_data(self, data, exclude=["_abilities"])
        for abilitydata in data["_abilities"]:
            for ability in self._abilities:
                if type(ability).__name__ == abilitydata["name"]:
                    abilitydata["selected_targets"] = [(x,y) for x,y in abilitydata["selected_targets"]]
                    ability.insert_data(abilitydata, exclude=["name"])

    def add_ability(self, ability_class: "Type[T]") -> "T|None":
        """Add an ability to this unit. Will spawn and initialize the required class."""
        for ability in self._abilities:
            if ability is ability_class:
                print(ability_class.__name__, "-class already exists")
                exit(1)
        ability = ability_class(self)
        self._abilities.append(ability)
        return ability

    def remove_ability(self, ability_class: "Type[AbilityBase]") -> None:
        """Remove an ability by class"""
        for ability in self._abilities[:]:
            if type(ability) == ability_class:
                log(f"Removed ability: {ability}", 0)
                self._abilities.remove(ability)

    def get_ability(self, ability_class: "Type[AbilityBase]") -> "AbilityBase|None":
        """Return the first ability of type ability_class, or None if none exists."""
        for ability in self._abilities:
            if type(ability) == ability_class:
                return ability
    
    def on_activate_ability(self, slot:int):
        """Called when the user wishes to use an ability by pressing one of the assigned slot numbers."""
        if slot >= 0 and slot < len(self._abilities):
            ability = self._abilities[slot]
            if ability.remainingcooldown == 0:
                ability.on_select_ability()

    def on_update_abilities_phases(self, newphase: int):
        """Called when a phase change occured."""
        for ability in self._abilities:
            ability.on_update_phase(newphase)

    def on_update_cursor(self, newcursorpos: "tuple[int,int]"):
        """Called when the user moves the cursor."""
        for ability in self._abilities:
            ability.on_update_cursor(newcursorpos)

    def on_select(self):
        """Called when this unit is selected."""
        for ability in self._abilities:
            ability.on_parentunit_select()
    
    def on_deselect(self):
        """Called when this unit is deselected."""
        for ability in self._abilities:
            ability.on_parentunit_deselect()

    def on_confirm_target(self, target:"tuple[int,int]"):
        """Called when the user hits enter, passes on the cursor position where the event occured."""
        for ability in self._abilities:
            if ability.selected:
                ability.confirm_target(target)
                return

    def get_selected_ability(self):
        """Return the ability that is currently selected."""
        for ability in self._abilities:
            if ability.selected:
                return ability
