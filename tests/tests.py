import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from itblib.Grid import Grid
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.gridelements.Tiles import TileBase
from itblib.scenes.RosterSelectionScene import RosterSelectionScene
from itblib.abilities.BurrowAbility import BurrowAbility
from itblib.gridelements.Effects import EffectBurrowed, EffectBase
from itblib.net.Connector import Connector
from itblib.Player import Player
from itblib.Game import Session, Game
from itblib.net.NetEvents import NetEvents

class TestGridMethods(unittest.TestCase):
    def setUp(self):
        self.w, self.h = 3,5
        connector = Connector(True)
        NetEvents.connector = connector
        self.grid = Grid(connector=connector, observer=None, width=self.w, height=self.h)
    
    def tearDown(self):
        self.grid.units = [None]*len(self.grid.units)
        self.grid.tiles = [None]*len(self.grid.tiles)

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
    
    def test_remove_unit(self):
        pos = (2,3)
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(pos=pos))
        self.assertIsInstance(self.grid.add_unit(pos=pos, unitid=unitid, ownerid=ownerid), UnitBase)
        self.assertTrue(self.grid.remove_unit(pos=pos))
        self.assertIsNone(self.grid.get_unit(pos))

    def test_add_tile(self):
        pos = (2,3)
        tileid = 2
        self.assertIsNone(self.grid.get_tile(pos=pos))
        self.assertTrue(self.grid.add_tile(pos=pos, tileid=tileid))
        self.assertIsInstance(self.grid.get_tile(pos=pos), TileBase)

    def test_remove_tile(self):
        pos = (0,2)
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(pos))
        self.assertTrue(self.grid.add_unit(pos, unitid, ownerid))
        self.assertIsNotNone(self.grid.get_unit(pos))
        self.assertTrue(self.grid.remove_unit(pos))
        self.assertIsNone(self.grid.get_unit(pos))

    def test_add_worldeffect(self):
        pos = (2,3)
        effectids = [2,3]
        self.assertFalse(self.grid.get_worldeffects(pos=pos))
        self.grid.add_worldeffect(
            pos=pos, worldeffectid=effectids[0])
        self.grid.add_worldeffect(
            pos=pos, worldeffectid=effectids[1])
        self.assertIsInstance(self.grid.get_worldeffects(pos=pos)[0], EffectBase)
        self.assertIsInstance(self.grid.get_worldeffects(pos=pos)[1], EffectBase)
    
    def test_remove_worldeffect(self):
        pos = (2,3)
        effectid = 2
        self.assertFalse(self.grid.get_worldeffects(pos=pos))
        effect = self.grid.add_worldeffect(pos=pos, worldeffectid=effectid)
        self.assertTrue(self.grid.remove_worldeffect(effect=effect, pos=pos))
        self.assertEqual(len(self.grid.get_worldeffects(pos)), 0)

    def test_move_unit(self):
        startpos = (0,2)
        endpos = (1,2)
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
        self.assertTrue(self.grid.is_coord_in_bounds([self.w-1,self.h-1]))
        self.assertFalse(self.grid.is_coord_in_bounds([self.w,self.h-1]))
        self.assertFalse(self.grid.is_coord_in_bounds([self.w-1,-1]))

    def test_get_ordinal_neighbors(self):
        pos1 = [1,2]
        pos2 = [0,0]
        ordinals1 = [(1,1),(1,3),(0,2),(2,2)]
        ordinals2 = [(0,1),(1,0)]
        self.assertCountEqual(ordinals1,self.grid.get_neighbors(pos1))
        self.assertCountEqual(ordinals2,self.grid.get_neighbors(pos2))


class TestUnitBaseMethods(unittest.TestCase):
    def setUp(self):
        self.gridw, self.gridh = 3,5
        self.pos = (2,3)
        self.ownerid = 0
        connector = Connector(True)
        NetEvents.connector = connector
        self.grid = Grid(connector=connector, observer=None, width=self.gridw, height=self.gridh)
        self.unit = UnitBase(self.grid, self.pos, self.ownerid)

    # def test_init(self):
    #    self.assertTrue(False)
    
    def test_grid_extract_data(self):
        d = self.grid.extract_data()
        testdict =\
            {
                'width': 3, 
                'height': 5, 
                'phasetime': 0, 
                'tiles': [None]*15, 
                'units': [None]*15, 
                'worldeffects': [[]]*15
            } 
        self.assertEqual(d, testdict)
    
    # def test_grid_insert_data(self):
    #     self.assertTrue(False)
    
    # def test_is_coord_in_bounds(self):
    #     self.assertTrue(False)

    # def test_get_ordinal_neighbors(self):
    #     self.assertTrue(False)

    def test_add_ability(self):
        self.assertTrue(BurrowAbility not in [type(a) for a in self.unit.abilities])
        self.unit.add_ability(BurrowAbility)
        self.assertTrue(BurrowAbility in [type(a) for a in self.unit.abilities])
    
    def test_remove_ability(self):
        self.unit.add_ability(BurrowAbility)
        self.assertTrue(BurrowAbility in [type(a) for a in self.unit.abilities])
        self.unit.remove_ability("BurrowAbility")
        self.assertTrue(BurrowAbility not in [type(a) for a in self.unit.abilities])
    
    def test_add_statuseffect(self):
        statuseffect = EffectBurrowed(self.unit)
        self.assertIsNone(self.unit.get_statuseffect(statuseffect))
        self.unit.add_statuseffect(statuseffect)
        self.assertTrue(statuseffect in self.unit.statuseffects)
    
    def test_remove_statuseffect(self):
        statuseffect = EffectBurrowed(self.unit)
        self.unit.add_statuseffect(statuseffect)
        self.assertTrue(statuseffect in self.unit.statuseffects)
        self.unit.remove_statuseffect("EffectBurrowed")
        self.assertIsNone(self.unit.get_statuseffect(statuseffect))
    
    def test_on_change_hp(self):
        hp = self.unit._hitpoints
        change = 1
        self.unit.change_hp(change, "physical")
        self.assertEqual(hp+1, self.unit._hitpoints)
    
    def test_on_death(self):
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(pos=self.pos))
        self.assertTrue(self.grid.add_unit(pos=self.pos, unitid=unitid, ownerid=ownerid))
        self.assertIsInstance(self.grid.get_unit(self.pos), UnitBase)
        self.unit.on_death()
        self.assertIsNone(self.grid.get_unit(self.pos))

class TestSessionMethods(unittest.TestCase):
    def setUp(self):
        self.connector = Connector(True)
        self.session = Session(self.connector)
        self.player = Player(0, None)

    def test_add_player(self):
        self.session.add_player(self.player)
        self.assertTrue(self.session._players[0].playerid == 0)

    def test_remove_player(self):
        self.session.add_player(self.player)
        self.session.remove_player(0, use_net=False)
        self.assertFalse("0" in self.session._players)

    def test_start_game(self):
        pass

    def test_objective_lost(self):
        pass

#TODO:
#class TestRoster(unittest.TestCase):
#    def test_roster_selection(self):
#        selects = [0,1,2,0]
#        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()