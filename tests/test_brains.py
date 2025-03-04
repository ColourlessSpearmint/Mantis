import pytest
import mantis_logic
import brains

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
        assert self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"
    
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
        assert self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"

    def test_blue_shell_all_same(self):
        self.p1.score_pile = [self.game.Card()]
        self.p2.score_pile = [self.game.Card()]
        self.p3.score_pile = [self.game.Card()]
        self.p4.score_pile = [self.game.Card()]

        info = self.game.get_info(shuffle=True)
        assert self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"

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

class TestMatcherBrain:
    def setup_method(self):
        self.game = mantis_logic.Mantis()
        self.p1 = self.game.Player(self.game, None, "Player 1")
        self.p2 = self.game.Player(self.game, None, "Player 2")
        self.p3 = self.game.Player(self.game, None, "Player 3")
        self.p4 = self.game.Player(self.game, None, "Player 4")
        self.game.start_game()
        self.brain = brains.MatcherBrain()

    def test_matcher_no_matches(self):
        # Test when no player has cards matching the next card's possible colours
        self.game.deck = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p1.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p2.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p3.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p4.tank = [self.game.generate_card(["red", "orange", "yellow"])]

        info = self.game.get_info(shuffle=True)
        assert self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"
    
    def test_matcher_equal_matches(self):
        # Test when all players have exactly one card matching the next card's possible colours
        self.game.deck = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p1.tank = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p2.tank = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p3.tank = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p4.tank = [self.game.generate_card(["blue", "purple", "pink"])]

        info = self.game.get_info(shuffle=True)
        assert self.brain.run(info) == "Player 1" or "Player 2" or "Player 3" or "Player 4"
    
    def test_matcher_one_match(self):
        # Test when only one player has a card matching the next card's possible colours
        self.game.deck = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p1.tank = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p2.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p3.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p4.tank = [self.game.generate_card(["red", "orange", "yellow"])]

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1"

    def test_matcher_two_equal_match(self):
        # Test when two players have exactly one card matching the next card's possible colours
        self.game.deck = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p1.tank = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p2.tank = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p3.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p4.tank = [self.game.generate_card(["red", "orange", "yellow"])]

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 1" or "Player 2"

    def test_matcher_two_unequal_match(self):
        # Test when two players have cards matching the next card's possible colours, but one player has more matching cards
        self.game.deck = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p1.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p2.tank = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p3.tank = [self.game.generate_card(["blue", "purple", "pink"]), self.game.generate_card(["blue", "purple", "pink"])]
        self.p4.tank = [self.game.generate_card(["red", "orange", "yellow"])]

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 3"

    def test_matcher_number_against_quantity(self):
        # Test when two players have cards matching the next card's possible colours, but one player has two single-match cards, and the other player has one double-match card
        self.game.deck = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p1.tank = [self.game.generate_card(["blue", "orange", "red"]), self.game.generate_card(["blue", "orange", "red"])]  # Two single-match
        self.p2.tank = [self.game.generate_card(["blue", "purple", "red"])]  # One double-match
        self.p3.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p4.tank = [self.game.generate_card(["red", "orange", "yellow"])]

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 2"
    
    def test_matcher_bulk_quantity_against_number(self):
        # Test when two players have cards matching the next card's possible colours, but one player has many single-match cards, and the other player has one double-match card
        self.game.deck = [self.game.generate_card(["blue", "purple", "pink"])]
        self.p1.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p2.tank = [self.game.generate_card(["red", "orange", "yellow"])]
        self.p3.tank = [self.game.generate_card(["blue", "orange", "red"]),
                        self.game.generate_card(["blue", "orange", "red"]),
                        self.game.generate_card(["blue", "orange", "red"])]  # Three single-match
        self.p4.tank = [self.game.generate_card(["blue", "purple", "red"])]  # One double-match

        info = self.game.get_info()
        assert self.brain.run(info) == "Player 4"

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