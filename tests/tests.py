import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

# Game sections
TEST_GRID = True
TEST_UNIT = True
TEST_SESSION = True

# Components
TEST_TRANSFORM_COMPONENT = True

if TEST_GRID:
    from testGrid import TestGridMethods
if TEST_UNIT:
    from testUnit import TestUnitBaseMethods
if TEST_SESSION:
    from testSession import TestSessionMethods

if TEST_TRANSFORM_COMPONENT:
    from componentTests.testTransformComponent import TestTransformComponentMethods


if __name__ == "__main__":
    unittest.main()
