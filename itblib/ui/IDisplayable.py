from abc import ABC, abstractmethod


class IDisplayable(ABC):
    @abstractmethod
    def get_display_name(self) -> str:
        pass

    @abstractmethod
    def get_display_description(self) -> str:
        pass
