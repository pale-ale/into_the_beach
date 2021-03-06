import unittest

from itblib.Grid import Grid
from itblib.Vec import IVector2
from itblib.gridelements.status_effect import StatusEffectBleeding
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.abilities.burrow_ability import BurrowAbility

class TestUnitBaseMethods(unittest.TestCase):
    def setUp(self):
        self.gridw, self.gridh = 3, 5
        self.pos = IVector2(2, 3)
        self.ownerid = 0
        self.grid = Grid(
            connector=None,
            observer=None,
            width=self.gridw,
            height=self.gridh
            )
        self.unit = UnitBase(self.grid, self.pos, self.ownerid)

    def test_grid_extract_data(self):
        d = self.grid.extract_data()
        testdict =\
            {
                'size': (3,5),
                'phasetime': 0,
                'tiles': [None]*15,
                'units': [None]*15,
                'worldeffects': [[]]*15
            } 
        self.assertCountEqual(d, testdict)

    def test_add_and_remove_ability(self):
        self.assertIsNone(self.unit.ability_component.get_ability(BurrowAbility))
        self.unit.ability_component.add_ability(BurrowAbility)
        self.assertIsInstance(self.unit.ability_component.get_ability(BurrowAbility), BurrowAbility)
        self.unit.ability_component.remove_ability(BurrowAbility)
        self.assertIsNone(self.unit.ability_component.get_ability(BurrowAbility))

    def test_add_remove_statuseffect(self):
        self.assertTrue(self.unit)
        statuseffect = StatusEffectBleeding(self.unit)
        self.assertIsNone(self.unit.get_statuseffect(statuseffect))
        self.unit.add_status_effect(statuseffect)
        self.assertTrue(statuseffect in self.unit.statuseffects)
        self.unit.remove_statuseffect("EffectBurrowed")
        self.assertIsNone(self.unit.get_statuseffect(statuseffect))

    def test_on_change_hp(self):
        hp = self.unit.hitpoints
        change = 1
        self.unit.change_hp(change, "physical")
        self.assertEqual(hp+1, self.unit.hitpoints)

    def test_on_death(self):
        unitid = 2
        ownerid = 0
        self.assertIsNone(self.grid.get_unit(pos=self.pos))
        self.assertTrue(self.grid.add_unit(pos=self.pos, unitid=unitid, ownerid=ownerid))
        self.assertIsInstance(self.grid.get_unit(self.pos), UnitBase)
        self.unit.on_death()
        self.assertIsNone(self.grid.get_unit(self.pos))
