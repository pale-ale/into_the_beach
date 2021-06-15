class Player:
    def __init__(self, id):
        self.name = "Player_1"
        self.color = (0,150,50,255)
        self._controlled_units = []
        self.id = id