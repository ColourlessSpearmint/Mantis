import pytest
import mantis_logic
import brains

TIMES_TO_CHECK = 100


class SampleCards:
    def __init__(self):
        game = mantis_logic.Mantis()
        self.red_card = game.generate_card(
            ["red", "orange", "pink"], random_colour=False
        )
        self.green_card = game.generate_card(
            ["green", "red", "blue"], random_colour=False
        )
        self.blue_card = game.generate_card(
            ["blue", "orange", "yellow"], random_colour=False
        )


def test_convert_colour_index_to_name():
    assert mantis_logic.convert_colour_index_to_name(1) == "red"
    assert mantis_logic.convert_colour_index_to_name(2) == "orange"
    assert mantis_logic.convert_colour_index_to_name(3) == "yellow"
    assert mantis_logic.convert_colour_index_to_name(4) == "green"
    assert mantis_logic.convert_colour_index_to_name(5) == "blue"
    assert mantis_logic.convert_colour_index_to_name(6) == "purple"
    assert mantis_logic.convert_colour_index_to_name(7) == "pink"


def test_convert_colour_list_to_names():
    assert mantis_logic.convert_colour_list_to_names([1, 2, 3]) == [
        "red",
        "orange",
        "yellow",
    ]
    assert mantis_logic.convert_colour_list_to_names([4, 5, 6]) == [
        "green",
        "blue",
        "purple",
    ]
    assert mantis_logic.convert_colour_list_to_names([3, 5, 7]) == [
        "yellow",
        "blue",
        "pink",
    ]


def test_validate_colour():
    assert mantis_logic.validate_colour("red") is True
    assert mantis_logic.validate_colour("orange") is True
    assert mantis_logic.validate_colour("yellow") is True
    assert mantis_logic.validate_colour("green") is True
    assert mantis_logic.validate_colour("blue") is True
    assert mantis_logic.validate_colour("purple") is True
    assert mantis_logic.validate_colour("pink") is True

    assert mantis_logic.validate_colour("1") is False


def test_random_card_generation():
    game = mantis_logic.Mantis()
    for _ in range(100):
        card = game.Card()
        assert card.colour in card.possible_colours


def test_manual_card_generation():
    game = mantis_logic.Mantis()

    card1 = game.generate_card(["blue", "purple", "pink"], random_colour=False)
    assert card1.possible_colours == ["blue", "purple", "pink"]
    assert card1.colour == "blue"

    card2 = game.generate_card(["green", "red", "yellow"], random_colour=False)
    assert card2.possible_colours == ["green", "red", "yellow"]
    assert card2.colour == "green"

    card3 = game.generate_card(["orange", "yellow", "purple"], random_colour=True)
    assert card3.possible_colours == ["orange", "yellow", "purple"]
    assert card3.colour in card3.possible_colours

    times_not_shuffled = 0
    for _ in range(TIMES_TO_CHECK):
        card4 = game.generate_card(["pink", "red", "green"], random_colour=True)
        assert card4.possible_colours == ["pink", "red", "green"]
        assert card4.colour in card4.possible_colours
        if card4.colour == card4.possible_colours[0]:
            times_not_shuffled += 1
    # We need to make sure that the list isn't unshuffled EVERY time.
    assert times_not_shuffled < TIMES_TO_CHECK


def test_is_valid_name():
    game = mantis_logic.Mantis()

    assert game.is_valid_new_name("score") is False
    assert game.is_valid_new_name("steal") is False
    assert game.is_valid_new_name("brain") is False
    assert game.is_valid_new_name("mantis") is False
    assert game.is_valid_new_name("SCORE") is False
    assert game.is_valid_new_name("STEAL") is False
    assert game.is_valid_new_name("BRAIN") is False
    assert game.is_valid_new_name("MANTIS") is False

    assert game.is_valid_new_name("Player 1") is True
    game.Player(game, None, "Player 1")
    assert game.is_valid_new_name("Player 1") is False
    assert game.is_valid_new_name("player 1") is False

    assert game.is_valid_new_name("Player 2") is True
    game.Player(game, None, "Player 2")
    assert game.is_valid_new_name("Player 1") is False
    assert game.is_valid_new_name("Player 2") is False



def test_score_action():
    game = mantis_logic.Mantis()
    sample_cards = SampleCards()
    assert len(game.deck) == 0

    p1 = game.Player(game, None, "Player 1")

    assert p1.tank == []
    assert p1.score_pile == []

    game.deck = [sample_cards.red_card, sample_cards.green_card]

    p1.tank = [sample_cards.red_card]

    assert game.deck[-1].colour == "green"
    assert game.deck[-2].colour == "red"
    assert p1.tank[0].colour == "red"

    # Unsuccessfully score, adding the unmatched green card to tank
    p1.score_action()
    assert p1.score_pile == []
    assert p1.get_self_tank_colours() == ["red", "green"]

    # Successfully score, transferring both red cards to score pile
    p1.score_action()
    assert len(p1.score_pile) == 2
    assert p1.score_pile[0].colour == "red"
    assert p1.score_pile[1].colour == "red"
    assert p1.get_self_tank_colours() == ["green"]


def test_steal_action():
    game = mantis_logic.Mantis()
    sample_cards = SampleCards()
    assert len(game.deck) == 0

    p1 = game.Player(game, None, "Player 1")
    p2 = game.Player(game, None, "Player 2")

    assert p1.tank == []
    assert p1.score_pile == []
    assert p2.tank == []
    assert p2.score_pile == []

    game.deck = [sample_cards.red_card, sample_cards.green_card]

    p1.tank = [sample_cards.green_card]
    p2.tank = [sample_cards.red_card]

    # Unsuccessfully steal, giving the drawn green card to p2's tank
    p1.steal_action(p2)
    assert p1.get_self_tank_colours() == ["green"]
    assert p2.get_self_tank_colours() == ["red", "green"]
    assert p1.score_pile == []
    assert p2.score_pile == []

    # Successfully steal, moving p2's red cards to p1's tank
    p1.steal_action(p2)
    assert p1.get_self_tank_colours() == ["green", "red", "red"]
    assert p2.get_self_tank_colours() == ["green"]
    assert p1.score_pile == []
    assert p2.score_pile == []


def test_get_info():
    game = mantis_logic.Mantis()
    sample_cards = SampleCards()
    p1 = game.Player(game, None, "Player 1")
    p2 = game.Player(game, None, "Player 2")

    game.deck = [sample_cards.blue_card]
    p1.tank = [sample_cards.green_card, sample_cards.green_card]
    p2.tank = [sample_cards.red_card, sample_cards.red_card]
    p2.score_pile = [sample_cards.green_card]

    info = game.get_info(shuffle=False)

    assert info.player_names == ["Player 1", "Player 2"]
    assert info.tank_colours["Player 1"] == ["green", "green"]
    assert info.tank_colours["Player 2"] == ["red", "red"]
    assert info.next_card_possible_colours == ["blue", "orange", "yellow"]
    assert info.scores["Player 1"] == 0
    assert info.scores["Player 2"] == 1


def test_get_info_shuffling():
    game = mantis_logic.Mantis()
    game.Player(game, None, "Player 1")
    game.Player(game, None, "Player 2")
    game.Player(game, None, "Player 3")
    game.Player(game, None, "Player 4")

    game.start_game()

    times_not_shuffled = 0
    for _ in range(TIMES_TO_CHECK):
        info = game.get_info(shuffle=True)
        if info.player_names == ["Player 1", "Player 2", "Player 3", "Player 4"]:
            times_not_shuffled += 1
    # We need to make sure that the list isn't unshuffled EVERY time.
    assert times_not_shuffled < TIMES_TO_CHECK


def test_take_turn():
    game = mantis_logic.Mantis()
    p1 = game.Player(game, brains.RandomBrain, "Random")
    p2 = game.Player(game, brains.BlueShellBrain, "Blue Shell")
    p3 = game.Player(game, brains.ScorerBrain, "Scorer")
    p4 = game.Player(game, brains.QuantityBrain, "Quantity")

    game.start_game()

    result = game.simulate_turn(verbose=True)
    assert result["active_player"] == "Random"
    assert result["action"] == "score" or "steal"
    assert result["target"] in ["Random", "Blue Shell", "Scorer", "Quantity"]

    p1.score_pile = [
        game.Card(),
        game.Card(),
        game.Card(),
        game.Card(),
        game.Card(),
        game.Card(),
    ]
    p2.score_pile = []
    p3.score_pile = []
    p4.score_pile = []
    result = game.simulate_turn(verbose=True)
    assert result["active_player"] == "Blue Shell"
    assert result["action"] == "steal"
    assert result["target"] == "Random"

    result = game.simulate_turn(verbose=True)
    assert result["active_player"] == "Scorer"
    assert result["action"] == "score"
    assert result["target"] is "Scorer"

    p1.tank = []
    p2.tank = [
        game.Card(),
        game.Card(),
        game.Card(),
        game.Card(),
        game.Card(),
    ]
    p3.tank = []
    p4.tank = []
    result = game.simulate_turn(verbose=True)
    assert result["active_player"] == "Quantity"
    assert result["action"] == "steal"
    assert result["target"] == "Blue Shell"

def test_out_of_cards():
    """Tests game-over by running out of cards by simulating an all-Klepto game"""
    game = mantis_logic.Mantis()
    game.Player(game, brains.KleptoBrain, "Player 1")
    game.Player(game, brains.KleptoBrain, "Player 2")
    game.Player(game, brains.KleptoBrain, "Player 3")
    game.Player(game, brains.KleptoBrain, "Player 4")
    game.start_game()
    for i in range(89):
        assert not game.game_over_message()
        game.simulate_turn()
    assert game.game_over_message() == "Ran out of cards"
