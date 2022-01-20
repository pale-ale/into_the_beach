import unittest

from itblib.Game import Session
from itblib.Player import Player

class TestSessionMethods(unittest.TestCase):
    def setUp(self):
        self.session = Session(None)
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
