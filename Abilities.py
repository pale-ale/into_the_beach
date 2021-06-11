class AbilityBase:
    def __init__(self, unit):
        self._unit = unit
        self.register_hooks()

    def register_hooks(self):
        pass


class MovementAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        #contains all the tilepositions the bound unit could move to
        self.movementinfo = set()
    
    def register_hooks(self):
        self._unit.register_hook("OnSelect", self.collect_movement_info)
        self._unit.register_hook("OnDeselect", lambda: self.movementinfo.clear())

    def collect_movement_info(self):            
        self.movementinfo = set()
        newtiles = {self._unit.get_position()}
        tmpnewtiles = set()
        rangefromstart = 0
        while rangefromstart <= self._unit.moverange:
            self.movementinfo = self.movementinfo.union(newtiles)
            while len(newtiles) > 0:
                newtilepos = newtiles.pop()
                self.movementinfo.add(newtilepos)
                for neighborpos in self._unit.grid.get_ordinal_neighbors(*newtilepos):
                    if neighborpos not in self.movementinfo:
                        tmpnewtiles.add(neighborpos)
            newtiles = tmpnewtiles.copy()
            tmpnewtiles.clear()
            rangefromstart += 1
            

