from math import pi
import unittest

import itblib.Vec as Vec
from itblib.globals.Enums import NORTH, EAST

class TestVecMethods(unittest.TestCase):
    def almostEqual2(self, a,b):
        self.assertAlmostEqual(a[0],b[0])
        self.assertAlmostEqual(a[1],b[1])

    def test_deg_to_coord(self):
        self.assertEqual(Vec.deg_to_coord(0), (1,0))
        self.almostEqual2(Vec.deg_to_coord(2*pi), (1,0))
        self.almostEqual2(Vec.deg_to_coord(pi), (-1,0))
        self.almostEqual2(Vec.deg_to_coord(pi/2), (0,1))

    def test_is_between(self):
        r = ( 1, 0)
        l = (-1, 0)
        u = ( 0, 1)
        d = ( 0,-1)
        self.assertTrue(Vec.vector_between(u,r,(1,1)))
        self.assertTrue(Vec.vector_between(r,u,(1,1)))
    
    def test_transform_vector(self):
        v_right    = (1,0)
        v_right_up = (1,1)
        m = (EAST, NORTH)
        self.assertEqual(Vec.transform_vector(m,v_right   ), (-1,1))
        self.assertEqual(Vec.transform_vector(m,v_right_up), (-2,0))
