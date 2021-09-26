import itblib.Globals.Enums as e
import itblib.gridelements.units.Units as units
import itblib.gridelements.Tiles as tiles
import itblib.gridelements.Effects as effects

class GridElementFactory:
    """
    Useful if you want to spawn the right tile/unit/effect based on name
    """
    #classes = [import_module('itblib.gridelements.units.Units.Unit' + s) for s in IDs.TILE_IDS if s]
    #tiles = import_module('itblib.gridelements.units.Units')
    #effects = import_module('itblib.gridelements.units.Units')
    #exit()

    @staticmethod 
    def _find_class(name:str, classes):
        if name in classes.__dict__.keys():
            cls = classes.__dict__[name]
            return cls
        print(f"GridElementFactory: Class '{name}' not found.")
        return None

    @staticmethod
    def find_unit_class(name:str):
        return GridElementFactory._find_class("Unit" + name, units)

    @staticmethod
    def find_tile_class(name:str):
        return GridElementFactory._find_class("Tile" + name, tiles)

    @staticmethod
    def find_effect_class(name:str):
        return GridElementFactory._find_class("Effect" + name, effects)
