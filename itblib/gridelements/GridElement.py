class GridElement:
    def __init__(self):
        self._pos = [None,None]
        self.age = 0
        self.done = True
        self.name = ""
    
    def tick(self, dt:float):
        self.age += dt

    def get_position(self):
        return self._pos[0], self._pos[1]
    
    def set_position(self, newposition:"tuple[int,int]"):
        self._pos = [c for c in newposition]
