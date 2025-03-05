import brains
import mantis_logic


class TestRandomBrain:
    def setup_method(self):
        self.game = mantis_logic.Mantis()
        self.p1 = self.game.Player(self.game, None, "Player 1")
        self.p2 = self.game.Player(self.game, None, "Player 2")
        self.p3 = self.game.Player(self.game, None, "Player 3")
        self.p4 = self.game.Player(self.game, None, "Player 4")
        self.game.start_game()
        self.brain = brains.RandomBrain()

    def test_random(self):
        info = self.game.get_info()
        assert (
            self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"
        )


class TestScorerBrain:
    def setup_method(self):
        self.game = mantis_logic.Mantis()
        self.p1 = self.game.Player(self.game, None, "Player 1")
        self.p2 = self.game.Player(self.game, None, "Player 2")
        self.p3 = self.game.Player(self.game, None, "Player 3")
        self.p4 = self.game.Player(self.game, None, "Player 4")
        self.game.start_game()
        self.brain = brains.ScorerBrain()

    def test_scorer(self):
        self.game.turns = 0
        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1"

        self.game.turns = 1
        info = self.game.get_info()
        assert self.brain.run(info) == "Player 2"

        self.game.turns = 3
        info = self.game.get_info()
        assert self.brain.run(info) == "Player 4"

        self.game.turns = 4
        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1"


class TestBlueShellBrain:
    def setup_method(self):
        self.game = mantis_logic.Mantis()
        self.p1 = self.game.Player(self.game, None, "Player 1")
        self.p2 = self.game.Player(self.game, None, "Player 2")
        self.p3 = self.game.Player(self.game, None, "Player 3")
        self.p4 = self.game.Player(self.game, None, "Player 4")
        self.game.start_game()
        self.brain = brains.BlueShellBrain()

    def test_blue_shell_all_zero(self):
        self.p1.score_pile = []
        self.p2.score_pile = []
        self.p3.score_pile = []
        self.p4.score_pile = []

        info = self.game.get_info(shuffle=False)
        assert self.brain.run(info) == "Player 4"

        info = self.game.get_info(shuffle=True)
        assert (
            self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"
        )

    def test_blue_shell_all_same(self):
        self.p1.score_pile = [self.game.Card()]
        self.p2.score_pile = [self.game.Card()]
        self.p3.score_pile = [self.game.Card()]
        self.p4.score_pile = [self.game.Card()]

        info = self.game.get_info(shuffle=True)
        assert (
            self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"
        )

    def test_blue_shell_one_winner(self):
        self.p1.score_pile = [self.game.Card()]
        self.p2.score_pile = []
        self.p3.score_pile = []
        self.p4.score_pile = []

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1"

    def test_blue_shell_two_player_tie(self):
        self.p1.score_pile = [self.game.Card()]
        self.p2.score_pile = [self.game.Card()]
        self.p3.score_pile = []
        self.p4.score_pile = []

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1" or "Player 2"


class TestQuantityBrain:
    def setup_method(self):
        self.game = mantis_logic.Mantis()
        self.p1 = self.game.Player(self.game, None, "Player 1")
        self.p2 = self.game.Player(self.game, None, "Player 2")
        self.p3 = self.game.Player(self.game, None, "Player 3")
        self.p4 = self.game.Player(self.game, None, "Player 4")
        self.game.start_game()
        self.brain = brains.QuantityBrain()

    def test_quantity_all_empty(self):
        self.p1.tank = []
        self.p2.tank = []
        self.p3.tank = []
        self.p4.tank = []
        info = self.game.get_info(shuffle=True)
        assert self.brain.run(info) in ["Player 1", "Player 2", "Player 3", "Player 4"]

    def test_quantity_one_winner(self):
        self.p1.tank = [self.game.Card(), self.game.Card()]
        self.p2.tank = []
        self.p3.tank = []
        self.p4.tank = []

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1"

    def test_quantity_two_player_tie(self):
        self.p1.tank = [self.game.Card(), self.game.Card()]
        self.p2.tank = [self.game.Card(), self.game.Card()]
        self.p3.tank = []
        self.p4.tank = []

        info = self.game.get_info()
        assert self.brain.run(info) in ["Player 1", "Player 2"]

    def test_quantity_different_quantities(self):
        self.p1.tank = [self.game.Card(), self.game.Card(), self.game.Card()]
        self.p2.tank = [self.game.Card(), self.game.Card()]
        self.p3.tank = [self.game.Card()]
        self.p4.tank = []

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1"
