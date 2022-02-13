from itblib.gridelements.GridElementUI import GridElementUI
from itblib.gridelements.Tiles import TileBase
from itblib.ui.IDisplayable import IDisplayable


class TileBaseUI(GridElementUI, IDisplayable):
    def __init__(self, tile:TileBase):
        GridElementUI.__init__(self, parentelement=tile, direction=None)
    
    def get_display_name(self) -> str:
        return "Somename"
    
    def get_display_description(self) -> str:
        return "No special tile effects"


class TileDirtUI(TileBaseUI):
    def get_display_name(self) -> str:
        return "Grass Tile"
