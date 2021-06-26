class IGridObserver:
    
    def on_add_tile(self, tile):
        pass
    
    def on_add_effect(self, effect):
        pass

    def on_add_unit(self, unit):
        pass

    def on_remove_unit(self, x, y):
        pass

    def on_move_unit(self, x, y, targetx, targety):
        pass

    