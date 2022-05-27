import unittest
from itblib.Grid import Grid
from itblib.Vec import IVector2
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.gridelements.Tiles import TileBase
from itblib.gridelements.world_effects import WorldEffectBase


class TestGridMethods(unittest.TestCase):
    def setUp(self):
        self.w, self.h = 3, 5
        self.grid = Grid(connector=None, observer=None, width=self.w, height=self.h)
        self.pos = IVector2(2, 3)

    def tearDown(self):
        self.grid.units = [None]*len(self.grid.units)
        self.grid.tiles = [None]*len(self.grid.tiles)

    def test_init(self):
        self.assertEqual(len(self.grid.units), self.w*self.h)
        self.assertEqual(len(self.grid.tiles), self.w*self.h)
        self.assertEqual(len(self.grid.worldeffects), self.w*self.h)

    def test_c_to_i(self):
        x, y = self.pos
        self.assertEqual(self.grid.c_to_i(self.pos), self.w*y+x)

    def test_add_unit(self):
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(pos=self.pos))
        self.assertTrue(self.grid.add_unit(pos=self.pos, unitid=unitid, ownerid=ownerid))
        self.assertIsInstance(self.grid.get_unit(pos=self.pos), UnitBase)

    def test_remove_unit(self):
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(pos=self.pos))
        self.assertIsInstance(self.grid.add_unit(pos=self.pos, unitid=unitid, ownerid=ownerid), UnitBase)
        self.assertTrue(self.grid.remove_unit(pos=self.pos))
        self.assertIsNone(self.grid.get_unit(self.pos))

    def test_add_tile(self):
        tileid = 2
        self.assertIsNone(self.grid.get_tile(pos=self.pos))
        print(type(self.pos))
        self.assertTrue(self.grid.add_tile(pos=self.pos, tileid=tileid))
        self.assertIsInstance(self.grid.get_tile(pos=self.pos), TileBase)

    def test_remove_tile(self):
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(self.pos))
        self.assertTrue(self.grid.add_unit(self.pos, unitid, ownerid))
        self.assertIsNotNone(self.grid.get_unit(self.pos))
        self.assertTrue(self.grid.remove_unit(self.pos))
        self.assertIsNone(self.grid.get_unit(self.pos))

    def test_add_worldeffect(self):
        effectids = [2,3]
        self.assertFalse(self.grid.get_worldeffects(pos=self.pos))
        self.grid.add_worldeffect(
            pos=self.pos, worldeffectid=effectids[0])
        self.grid.add_worldeffect(
            pos=self.pos, worldeffectid=effectids[1])
        self.assertIsInstance(self.grid.get_worldeffects(pos=self.pos)[0], WorldEffectBase)
        self.assertIsInstance(self.grid.get_worldeffects(pos=self.pos)[1], WorldEffectBase)
    
    def test_remove_worldeffect(self):
        effectid = 2
        self.assertFalse(self.grid.get_worldeffects(pos=self.pos))
        effect = self.grid.add_worldeffect(pos=self.pos, worldeffectid=effectid)
        self.assertTrue(self.grid.remove_worldeffect(effect=effect, pos=self.pos))
        self.assertEqual(len(self.grid.get_worldeffects(self.pos)), 0)

    def test_move_unit(self):
        startpos = IVector2(0, 2)
        endpos = IVector2(1, 2)
        unitid = 2
        tileid = 1
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(startpos))
        self.assertIsNone(self.grid.get_unit(endpos))
        self.assertTrue(self.grid.add_unit(startpos, unitid, ownerid))
        self.assertIsNotNone(self.grid.get_unit(startpos))
        self.assertIsNone(self.grid.get_unit(endpos))
        # unit should fall from the grid in this case, so nothing should have changed
        self.assertFalse(self.grid.move_unit(startpos, endpos))
        self.assertIsNotNone(self.grid.get_unit(startpos))
        self.assertIsNone(self.grid.get_unit(endpos))
        # adding the tile allows us to move the unit
        self.grid.add_tile(endpos, tileid)
        self.assertTrue(self.grid.move_unit(startpos, endpos))
        self.assertIsNone(self.grid.get_unit(startpos))
        self.assertIsNotNone(self.grid.get_unit(endpos))

    def test_is_coord_in_bounds(self):
        self.assertTrue(
            self.grid.is_coord_in_bounds(IVector2(self.w-1, self.h-1)))
        self.assertFalse(
            self.grid.is_coord_in_bounds(IVector2(self.w, self.h-1)))
        self.assertFalse(
            self.grid.is_coord_in_bounds(IVector2(self.w-1, -1)))

    def test_get_ordinal_neighbors(self):
        pos1 = IVector2(1, 2)
        pos2 = IVector2(0, 0)
        ordinals1 = [(1, 1), (1, 3), (0, 2), (2, 2)]
        ordinals2 = [(0, 1), (1, 0)]
        self.assertCountEqual(ordinals1, [(x,y) for x,y in self.grid.get_neighbors(pos1)])
        self.assertCountEqual(ordinals2, [(x,y) for x,y in self.grid.get_neighbors(pos2)])
