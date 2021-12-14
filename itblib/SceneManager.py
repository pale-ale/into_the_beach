from itblib.scenes.SceneBase import SceneBase

class SceneManager:
    """Manages the Scenes."""
    def __init__(self, scene_size:"tuple[int,int]") -> None:
        self.scenes:"dict[str, SceneBase]" = {}
        self._activescene:"SceneBase" = None
        self.scene_size:"tuple[int,int]" = scene_size
    
    def load_scene(self, key:str):
        if key in self.scenes.keys():
            if self._activescene:
                self._activescene.unload()
            scene = self.scenes[key]
            self._activescene = scene
            print(f"SceneManager: Loading scene '{type(scene).__name__}'")
            self._activescene.load()
        else:
            print("SceneManager: Unknown scene '" + key + "'")
    
    def add_scene(self, key:str, scene:"SceneBase"):
        self.scenes[key] = scene

    def update(self, dt):
        if self._activescene:
            self._activescene.update(dt)
