import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

# Game sections
TEST_GRID                = False
TEST_UNIT                = False
TEST_SESSION             = False

# Components
TEST_TRANSFORM_COMPONENT = False

# Networking
TEST_NETWORK             = True


# Game sections
if TEST_GRID:
    from testGrid import TestGridMethods
if TEST_UNIT:
    from testUnit import TestUnitBaseMethods
if TEST_SESSION:
    from testSession import TestSessionMethods


# Components
if TEST_TRANSFORM_COMPONENT:
    from componentTests.testTransformComponent import TestTransformComponentMethods


# Networking
if TEST_NETWORK:
    from networkTests.testNetwork import TestNetworkMethods



if __name__ == "__main__":
    unittest.main()
