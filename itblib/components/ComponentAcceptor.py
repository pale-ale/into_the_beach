import abc
from typing import Type, TypeVar

from itblib.components.ComponentBase import ComponentBase

T = TypeVar('T', bound=ComponentBase)

class ComponentAcceptor(abc.ABC):
    """Allows adding Components to an Object to change its behaviour."""
    def __init__(self) -> None:
        self.components:list[ComponentBase] = []

    def get_component(self, componentType:Type[T]) -> "T|None":
        """Return a Component of type componentType, or None if no such component exists."""
        for component in self.components:
            if type(component) == componentType:
                return component
        return None
