import itblib.gridelements.UnitsUI as units
import itblib.gridelements.TilesUI as tiles
import itblib.gridelements.ui_effect as effects

class GridElementUIFactory:
    """
    Useful if you want to spawn the right uitile/uiunit/uieffect based on name
    """

    @staticmethod
    def _find_class(name:str, classes):
        """Return a class named 'name' in 'classes' or the base class if not found (if base not found either, return None)"""
        if name in classes.__dict__.keys():
            cls = classes.__dict__[name]
            return cls
        #print(f"GridElementUIFactory: Class '{name}' not found.")
        for name in classes.__dict__.keys():
            if name.endswith("BaseUI"):
                return classes.__dict__[name]
        return None

    @staticmethod
    def find_unit_class(name:str) -> "units.UnitBaseUI|None":
        """Return a class named 'name' in 'itblib.gridelements.units.Units' or None if not found"""
        return GridElementUIFactory._find_class(name, units)

    @staticmethod
    def find_tile_class(name:str) -> "tiles.TileBaseUI|None":
        """Return a class named 'name' in 'itblib.gridelements.Tiles' or None if not found"""
        return GridElementUIFactory._find_class(name, tiles)

    @staticmethod
    def find_effect_class(name:str) -> "effects.EffectBaseUI|None":
        """Return a class named 'name' in 'itblib.gridelements.Effects' or None if not found"""
        return GridElementUIFactory._find_class(name, effects)
