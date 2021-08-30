import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from itblib.Grid import Grid
from itblib.gridelements.Units import UnitBase
from itblib.gridelements.Tiles import TileBase

class TestGridMethods(unittest.TestCase):
    def setUp(self):
        self.w, self.h = 3,5
        self.grid = Grid(connector=None, observer=None, width=self.w, height=self.h)

    def test_init(self):
        self.assertEqual(len(self.grid.units), self.w*self.h)
        self.assertEqual(len(self.grid.tiles), self.w*self.h)
        self.assertEqual(len(self.grid.worldeffects), self.w*self.h)
    
    def test_c_to_i(self):
        x,y = 2,3
        self.assertEqual(self.grid.c_to_i((x,y)), self.w*y+x)
    
    def test_add_unit(self):
        pos = (2,3)
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(pos=pos))
        self.assertTrue(self.grid.add_unit(pos=pos, unitid=unitid, ownerid=ownerid))
        self.assertIsInstance(self.grid.get_unit(pos=pos), UnitBase)
  
    def test_add_tile(self):
        pos = (2,3)
        tileid = 2
        self.assertIsNone(self.grid.get_tile(pos=pos))
        self.assertTrue(self.grid.add_tile(pos=pos, tileid=tileid))
        self.assertIsInstance(self.grid.get_tile(pos=pos), TileBase)

if __name__ == "__main__":
    unittest.main()