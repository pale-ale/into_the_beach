from itblib.scenes.SceneBase import SceneBase
import sys

class SceneManager:
    """Manages the Scenes."""
    def __init__(self) -> None:
        self.scenes:"dict[str, SceneBase]" = {}
        self._activescene:"SceneBase" = None
    
    def load_scene(self, key:str):
        if key in self.scenes.keys():
            if self._activescene:
                self._activescene.unload()
            scene = self.scenes[key]
            self._activescene = scene
            self._activescene.load()
            print(f"SceneManager: Loading scene '{type(scene).__name__}'")
        else:
            print("SceneManager: Unknown scene '" + key + "'")
    
    def add_scene(self, key:str, scene:"SceneBase"):
        self.scenes[key] = scene

    def update(self, dt):
        if self._activescene:
            self._activescene.update(dt)
