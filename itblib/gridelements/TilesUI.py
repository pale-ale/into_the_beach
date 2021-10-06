from ..ui.TextureManager import Textures
from .GridElementUI import GridElementUI
from .Tiles import TileBase

class TileBaseUI(GridElementUI):
    def __init__(self, tile:TileBase, width:int=64, height:int=96):
        super().__init__(parentelement=tile, direction=None, width=width, height=height) 
