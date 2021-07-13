from itblib.scenes.SceneBase import SceneBase

class SceneManager():
    """Manages the Scenes."""
    def __init__(self) -> None:
        self.scenes:"dict[str, SceneBase]" = {}
        self.activescene:"SceneBase" = None
    
    def load_scene(self, key:str):
        if key in self.scenes.keys():
            if self.activescene:
                self.activescene.unload()
            scene = self.scenes[key]
            self.activescene = scene
            self.activescene.load()
    
    def add_scene(self, key:str, scene:"SceneBase"):
        self.scenes[key] = scene

