import itblib.gridelements.units.Units as units
import itblib.gridelements.Tiles as tiles
import itblib.gridelements.Effects as effects

class GridElementFactory:
    """
    Useful if you want to spawn the right tile/unit/effect based on name
    """

    @staticmethod 
    def _find_class(name:str, classes):
        """Return a class named 'name' in 'classes' or None if not found"""
        if name in classes.__dict__.keys():
            cls = classes.__dict__[name]
            return cls
        print(f"GridElementFactory: Class '{name}' not found.")
        return None

    @staticmethod
    def find_unit_class(name:str) -> "units.UnitBase|None":
        """Return a class named 'name' in 'itblib.gridelements.units.Units' or None if not found"""
        return GridElementFactory._find_class("Unit" + name, units)

    @staticmethod
    def find_tile_class(name:str) -> "tiles.TileBase|None":
        """Return a class named 'name' in 'itblib.gridelements.Tiles' or None if not found"""
        return GridElementFactory._find_class("Tile" + name, tiles)

    @staticmethod
    def find_effect_class(name:str) -> "effects.EffectBase|None":
        """Return a class named 'name' in 'itblib.gridelements.Effects' or None if not found"""
        return GridElementFactory._find_class("Effect" + name, effects)
