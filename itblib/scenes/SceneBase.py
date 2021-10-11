import pygame

from itblib.net.NetEvents import NetEvents

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.SceneManager import SceneManager

class SceneBase(pygame.sprite.Sprite):
    """
    Scenes are a way to organize several Display-Objects as well as their functioniality,
    essentially allowing for easy grouping.

    Scenes are managed by the SceneManager, 
    which is able to e.g. load() and unload() scenes before and after use, respectively. 
    """

    def __init__(self, scenemanager:"SceneManager",  width:int, height:int) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.scenemanager = scenemanager
    
    def on_keyevent(self, keyevent):
        """Forwards keystrokes to the scene, allowing for easy navigation."""
        pass

    def on_displayresize(self, newsize:"tuple[int,int]"):
        pass #self.image = pygame.Surface(newsize)
        
    def update(self, dt:float):
        if NetEvents.connector and NetEvents.connector.acc_connection:
            data = NetEvents.connector.receive_client()
            if data:
                prefix, contents = data
                NetEvents.rcv_event_caller(prefix, contents)

    def load(self):
        """Initialize a scene, load textures, etc."""
        pass

    def unload(self):
        """Perform cleanup tasks like removing hooks."""
        pass
      