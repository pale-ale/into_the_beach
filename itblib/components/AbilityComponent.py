from typing import TYPE_CHECKING, Type
from itblib.Serializable import Serializable
from itblib.components.ComponentBase import ComponentBase

if TYPE_CHECKING:
    from itblib.abilities.AbilityBase import AbilityBase


class AbilityComponent(ComponentBase, Serializable):
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

    def add_ability(self, ability_class: "AbilityBase") -> None:
        """Add an ability to this unit. Will spawn and initialize the required class."""
        for ability in self._abilities:
            if ability is ability_class:
                print(ability_class.__name__, "-class already exists")
                exit(1)
        self._abilities.append(ability_class(self))

    def remove_ability(self, ability_class: "Type[AbilityBase]") -> None:
        """Remove an ability by class"""
        for ability in self._abilities[:]:
            if type(ability) == ability_class:
                print("Removed ability:", ability)
                self._abilities.remove(ability)

    def get_ability(self, ability_class: "Type[AbilityBase]") -> "AbilityBase":
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