import abc
from typing import Union

from itblib.components.ComponentBase import ComponentBase
from itblib.Log import log

class ComponentAcceptor(abc.ABC):
    def __init__(self) -> None:
        self.components:list[ComponentBase] = []

    def get_component(self, componentType:type[ComponentBase]) -> Union[ComponentBase,None]:
        for component in self.components:
            if type(component) == componentType:
                return component
        return None
