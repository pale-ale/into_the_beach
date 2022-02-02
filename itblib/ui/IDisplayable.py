from abc import ABC, abstractmethod


class IDisplayable(ABC):
    """Objects implementing this interface have a name and description method."""
    @abstractmethod
    def get_display_name(self) -> str:
        pass

    @abstractmethod
    def get_display_description(self) -> str:
        pass
