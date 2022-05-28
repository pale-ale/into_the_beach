from abc import ABC
from typing import TYPE_CHECKING, TypeVar

from itblib.Vec import IVector2

from itblib.Log import log
from itblib.Serializable import Serializable

if TYPE_CHECKING:
    from typing import Type
    from itblib.abilities.base_abilities.ability_base import AbilityBase


class ComponentBase(ABC):
    """Components allow for simple and reusable grouping of bahaviours.
    If you want an object to move, give it a TransformComponent etc."""
    def __init__(self):
        self.owner: "ComponentAcceptor|None" = None

    def attach_component(self, target: "ComponentAcceptor"):
        """Add the Component to a ComponentAcceptor."""
        if not target:
            log("Tried to attach component to None.", 2)
            return
        self.on_attach_component(target=target)
        self.owner = target
        self.owner.components.append(self)

    def detach_component(self):
        """Remove the Component from a CompnentAcceptor."""
        if not self.owner:
            log("Tried to detach component which was already detached.", 2)
            return
        self.owner.components.remove(self)
        self.on_detach_component()
        self.owner = None

    def on_attach_component(self, target: "ComponentAcceptor"):
        """Setup method for convenience"""

    def on_detach_component(self):
        """Teardown method for convenience"""

    def on_initialize_component(self):
        """Setup method for convenience"""

    def on_destroy_component(self):
        """Teardown method for convenience"""


C = TypeVar('C', bound="ComponentBase")


class ComponentAcceptor(ABC):
    """Allows adding Components to an Object to change its behaviour."""
    def __init__(self) -> None:
        self.components: list[ComponentBase] = []

    def get_component(self, component_type: "Type[C]") -> "C|None":
        """Return a Component of type componentType, or None if no such component exists."""
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None


A = TypeVar('A', bound="AbilityBase")


class AbilityComponent(ComponentBase, Serializable):
    """
    Adds ability behaviour to a ComponentAcceptor.
    Contains the Abilities and various hooks to trigger for them.
    """
    def __init__(self, abilities: "list[Type[AbilityBase]]") -> None:
        ComponentBase.__init__(self)
        Serializable.__init__(self, ["_abilities"])
        self._abilities: "list[AbilityBase]" = [
            ability(self) for ability in abilities]
        self.targeting_ability = False

    def extract_data(self, custom_fields: "dict[str,any]" = None) -> dict:
        customabilities = [x.extract_data() for x in self._abilities]
        return Serializable.extract_data(self, custom_fields={"_abilities": customabilities})

    def insert_data(self, data):
        Serializable.insert_data(self, data, exclude=["_abilities"])
        for abilitydata in data["_abilities"]:
            for ability in self._abilities:
                if type(ability).__name__ == abilitydata["name"]:
                    abilitydata["selected_targets"] = [IVector2(x, y) for x, y in abilitydata["selected_targets"]]
                    ability.insert_data(abilitydata, exclude=["name"])

    def add_ability(self, ability_class: "Type[A]") -> "A|None":
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
            if isinstance(ability, ability_class):
                log(f"Removed ability: {ability}", 0)
                self._abilities.remove(ability)

    def get_ability(self, ability_class: "Type[AbilityBase]") -> "AbilityBase|None":
        """Return the first ability of type ability_class, or None if none exists."""
        for ability in self._abilities:
            if isinstance(ability, ability_class):
                return ability
        return None

    def on_activate_ability(self, slot: int):
        """
        Called when the user wishes to use an ability by pressing one of the assigned slot numbers.
        """
        if 0 <= slot < len(self._abilities):
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

    def on_confirm_target(self, target: "tuple[int,int]"):
        """
        Called when the user hits enter, passes on the cursor position where the event occured.
        """
        for ability in self._abilities:
            if ability.selected:
                ability.confirm_target(target)
                return

    def get_selected_ability(self):
        """Return the ability that is currently selected."""
        for ability in self._abilities:
            if ability.selected:
                return ability
        return None


class TransformComponent(ComponentBase):
    """
    TransformComponents can be used to position objects in the world.
    Their transform target can be set to a different TransformComponent
    to calculate the relative vs. global position, i.e. "moving with
    the TransformComponent it is attached to".
    """
    def __init__(self):
        super().__init__()
        self._relative_position: IVector2 = IVector2(0, 0)
        self.children: list[ComponentAcceptor] = []
        self.parent_transform_component: TransformComponent = None

    @property
    def relative_position(self):
        return self._relative_position

    @relative_position.setter
    def relative_position(self, relative_position: IVector2):
        assert isinstance(relative_position, IVector2)
        self._relative_position = relative_position

    def set_transform_target(self, target: ComponentAcceptor) -> bool:
        """
        Set target's TransformComponent as this TransformCompnent's point of reference.
        @target: The object with the TransformComponent we want to attach to, i.e. move with.
        @return: Whether the attachment was successful or not.
        """
        if self.parent_transform_component:
            self.parent_transform_component.children.remove(self)

        other_tfc: TransformComponent = target.get_component(TransformComponent)
        if not other_tfc:
            log("TransformComponent: Tried to set_transform_target() to non-TransformComponent.", 2)
            return False
        self.parent_transform_component = other_tfc
        self.parent_transform_component.children.append(self)
        return True

    def get_position(self) -> IVector2:
        """
        Get the global position of the object.
        @return: The global position, calculated by adding every transform parent's local offset
        """
        assert isinstance(self.relative_position, IVector2)
        pos = self.relative_position
        if self.parent_transform_component:
            pos = pos + self.parent_transform_component.get_position()
        return pos
