import pygame
from pygame.sprite import Sprite

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.SceneManager import SceneManager

class SceneBase(Sprite):
    """
    Scenes are a way to organize several Display-Objects as well as their functioniality,
    essentially allowing for easy grouping.

    Scenes are managed by the SceneManager, 
    which is able to e.g. load() and unload() scenes before and after use, respectively. 
    """

    def __init__(self, scenemanager:"SceneManager",  width:int, height:int, *groups) -> None:
        super().__init__(*groups)
        self.desired_size = (width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.scenemanager = scenemanager
    
    def on_keyevent(self, keyevent):
        """Forwards keystrokes to the scene, allowing for easy navigation."""
        pass

    def on_displayresize(self, newsize:"tuple[int,int]"):
        self.image = pygame.Surface(newsize)
        self.desired_size = newsize
        
    def tick(self, dt:float):
        pass

    def load(self):
        """Initialize a scene, load textures, etc."""
        pass

    def unload(self):
        """Perform cleanup tasks like removing hooks."""
        pass
      