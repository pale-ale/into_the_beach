from ..ui.TextureManager import Textures
from .GridElementUI import GridElementUI
from .Tiles import TileBase

class TileBaseUI(GridElementUI):
    def __init__(self, tile:TileBase, width:int=64, height:int=64):
        super().__init__(direction=None, width=width, height=height, parentelement=tile) 

   
