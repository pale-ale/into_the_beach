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
        r = (10, 0)
        l = (10, 1)
        t_1 = (10, .5)
        f_1 = (-10,-.5)
        f_2 = (10,1.1)
        f_3 = (1,10)
        self.assertTrue(Vec.vector_between(r,l,t_1))
        self.assertFalse(Vec.vector_between(l,r,f_1))
        self.assertFalse(Vec.vector_between(l,r,f_2))
        self.assertFalse(Vec.vector_between(l,r,f_3))
    
    def test_transform_vector(self):
        v_right    = (1,0)
        v_right_up = (1,1)
        m = (EAST, NORTH)
        self.assertEqual(Vec.transform_vector(m,v_right   ), (-1,1))
        self.assertEqual(Vec.transform_vector(m,v_right_up), (-2,0))
