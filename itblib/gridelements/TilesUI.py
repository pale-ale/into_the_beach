from itblib.gridelements.GridElementUI import GridElementUI
from itblib.gridelements.Tiles import TileBase
from itblib.ui.IDisplayable import IDisplayable


class TileBaseUI(GridElementUI, IDisplayable):
    def __init__(self, tile:TileBase):
        GridElementUI.__init__(self, parentelement=tile, direction=None)
    
    def get_display_name(self) -> str:
        return "Somename"
    
    def get_display_description(self) -> str:
        return ""


class TileDirtUI(TileBaseUI):
    def get_display_name(self) -> str:
        return "Grass"


class TileRockUI(TileBaseUI):
    def get_display_name(self) -> str:
        return "Wasteland"


class TileWaterUI(TileBaseUI):
    def get_display_name(self) -> str:
        return "Water"

    def get_display_description(self) -> str:
        return "Drowns units that cannot swim"


class TileLavaUI(TileBaseUI):
    def get_display_name(self) -> str:
        return "Lava"
        
    def get_display_description(self) -> str:
        return "Drowns units that cannot swim and sets them on fire"

