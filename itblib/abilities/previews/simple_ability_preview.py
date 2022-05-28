"""Contains the SimeAbilityPreview class."""

from typing import TYPE_CHECKING
from itblib.Vec import IVector2

from itblib.abilities.previews.abilitiy_preview_base import AbilityPreviewBase

if TYPE_CHECKING:
    from typing import Callable, Generator
    from pygame import Surface, Rect


class SimpleAbilityPreview(AbilityPreviewBase):
    """Creates previews for a unit based on it's abilities and their targets."""

    def get_blit_func(self, transform_func:"Callable[[IVector2], IVector2]") -> "Generator[tuple[Surface, Rect, Rect]]":
        """@transform_func: turns grid coordinates into screen coordinates"""
        yield from self._get_simple_preview_gen(transform_func=transform_func)
