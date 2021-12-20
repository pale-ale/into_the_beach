import abc
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.components.ComponentAcceptor import ComponentAcceptor

from itblib.Log import log

class ComponentBase(abc.ABC):
    """Components allow for simple and reusable grouping of bahaviours.
    If you want an object to move, give it a TransformComponent etc."""
    def __int__(self):
        self.owner:ComponentAcceptor = None

    def attach_component(self, target:"ComponentAcceptor"):
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
            log("Tried to dettach component which was already detached.", 2)
            return
        self.owner.components.remove(self)
        self.on_detach_component()
        self.owner = None

    def on_attach_component(self, target:"ComponentAcceptor"):
        """Setup method for convenience"""
        pass
    
    def on_detach_component(self):
        """Teardown method for convenience"""
        pass
    
    def on_initialize_component(self):
        """Setup method for convenience"""
        pass
    
    def on_destroy_component(self):
        """Teardown method for convenience"""
        pass
