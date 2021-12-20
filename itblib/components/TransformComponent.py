from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.ComponentBase import ComponentBase
from itblib.Log import log
from itblib.Vec import add


class TransformComponent(ComponentBase):
    def __init__(self):
        super().__init__()
        self.relative_position:tuple[int,int] = (0,0)
        self.children:list[ComponentAcceptor] = []
        self.parent_transform_component:TransformComponent = None
    
    def set_transform_target(self, target:ComponentAcceptor) -> bool:
        """Set target's TransformComponent as this TransformCompnent's point of reference.
        @target: The object with the TransformComponent we want to attach to, i.e. move with.
        @return: Whether the attachment was successful or not."""

        if self.parent_transform_component:
            self.parent_transform_component.children.remove(self)

        other_transform:TransformComponent = target.get_component(TransformComponent)
        if not other_transform:
            log("TransformComponent: Tried to set_transform_target() to non-TransformComponent.", 2)
            return False
        self.parent_transform_component = other_transform
        self.parent_transform_component.children.append(self)
        return True

    def get_position(self) -> tuple[int, int]:
        """Get the global position of the object.
        @return: The global position, calculated by adding every transform parent's local offset"""
        pos = self.relative_position
        if self.parent_transform_component:
            pos:tuple[int,int] = add(pos, self.parent_transform_component.get_position())
        return pos
