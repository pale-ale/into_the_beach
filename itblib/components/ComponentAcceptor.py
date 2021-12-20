import abc
from typing import Union

from itblib.components.ComponentBase import ComponentBase
from itblib.Log import log

class ComponentAcceptor(abc.ABC):
    """Allows adding Components to an Object to change its behaviour."""
    def __init__(self) -> None:
        self.components:list[ComponentBase] = []

    def get_component(self, componentType:type[ComponentBase]) -> Union[ComponentBase,None]:
        """Return a Component of type componentType, or None if no such component exists."""
        for component in self.components:
            if type(component) == componentType:
                return component
        return None
