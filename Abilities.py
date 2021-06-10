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

    def collect_movement_info(self):
        self.movementinfo = set(self._unit.grid.get_ordinal_neighbors(*self._unit.get_position()))
