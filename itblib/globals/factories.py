"""Contains various facotries that can be used globally."""

import itblib.gridelements.world_effects as effects
import itblib.gridelements.Tiles as tiles
import itblib.gridelements.units.units as units

import itblib.gridelements.ui_effect as ui_effects
import itblib.gridelements.TilesUI as ui_tiles
import itblib.gridelements.UnitsUI as ui_units

from itblib.Log import log

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
        log(f"GridElementUIFactory: Class '{name}' not found. Trying to use fallback.", 1)
        for name in classes.__dict__.keys():
            if name.endswith("BaseUI"):
                return classes.__dict__[name]
        return None

    @staticmethod
    def find_unit_class(name:str) -> "ui_units.UnitBaseUI|None":
        """Return a class named 'name' in 'itblib.gridelements.units.UnitsUI' or None if not found"""
        return GridElementUIFactory._find_class(name, ui_units)

    @staticmethod
    def find_tile_class(name:str) -> "ui_tiles.TileBaseUI|None":
        """Return a class named 'name' in 'itblib.gridelements.TilesUI' or None if not found"""
        return GridElementUIFactory._find_class(name, ui_tiles)

    @staticmethod
    def find_effect_class(name:str) -> "ui_effects.EffectBaseUI|None":
        """Return a class named 'name' in 'itblib.gridelements.EffectsUI' or None if not found"""
        return GridElementUIFactory._find_class(name, ui_effects)
