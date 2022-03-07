import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

TEST_ALL = True

# Game sections
TEST_GRID                = False
TEST_UNIT                = False
TEST_SESSION             = False

# Components
TEST_TRANSFORM_COMPONENT = False

# Networking
TEST_NETWORK             = True

# Scenes
TEST_SCENES              = True


# Game sections
if TEST_ALL or TEST_GRID:
    from testGrid import TestGridMethods
if TEST_ALL or TEST_UNIT:
    from testUnit import TestUnitBaseMethods
if TEST_ALL or TEST_SESSION:
    from testSession import TestSessionMethods


# Components
if TEST_ALL or TEST_TRANSFORM_COMPONENT:
    from componentTests.testTransformComponent import TestTransformComponentMethods


# Networking
if TEST_ALL or TEST_NETWORK:
    from networkTests.testNetwork import TestNetworkMethods
    from networkTests.testJoinGame import TestJoinGameMethods

# Scenes
if TEST_ALL or TEST_SCENES:
    from testScenes import TestScenes

if TEST_ALL:
    from testVec import TestVecMethods


if __name__ == "__main__":
    unittest.main()
