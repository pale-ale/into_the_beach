from typing import TYPE_CHECKING

from itblib.abilities.previews.AbilityPreviewBase import AbilityPreviewBase

if TYPE_CHECKING:
    from typing import Callable, Generator

    import pygame


class SimpleAbilityPreview(AbilityPreviewBase):
    """Creates previews for a unit based on it's abilities and their targets."""

    def get_blit_func(self, transform_func:"Callable[[tuple[int,int]], tuple[int,int]]") -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        """@transform_func: turns grid coordinates into screen coordinates"""
        yield from self._get_simple_preview_gen(transform_func=transform_func)

    def update(self, delta_time: float) -> None:
        pass
