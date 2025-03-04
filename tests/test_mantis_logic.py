import pytest
import mantis_logic

class Sample_Cards:
    def __init__(self):
        game = mantis_logic.Mantis()
        self.red_card = game.Card()
        self.red_card.colour = "red"
        self.green_card = game.Card()
        self.green_card.colour = "green"
        self.blue_card = game.Card()
        self.blue_card.colour = "blue"
        self.blue_card.possible_colours = ["blue", "orange", "yellow"]

def test_convert_colour_index_to_name():
    assert mantis_logic.convert_colour_index_to_name(1) == "red"
    assert mantis_logic.convert_colour_index_to_name(2) == "orange"
    assert mantis_logic.convert_colour_index_to_name(3) == "yellow"
    assert mantis_logic.convert_colour_index_to_name(4) == "green"
    assert mantis_logic.convert_colour_index_to_name(5) == "blue"
    assert mantis_logic.convert_colour_index_to_name(6) == "purple"
    assert mantis_logic.convert_colour_index_to_name(7) == "pink"

def test_convert_colour_list_to_names():
    assert mantis_logic.convert_colour_list_to_names([1,2,3]) == ["red","orange","yellow"]
    assert mantis_logic.convert_colour_list_to_names([4,5,6]) == ["green","blue","purple"]
    assert mantis_logic.convert_colour_list_to_names([3,5,7]) == ["yellow","blue","pink"]

def test_validate_colour():
    assert mantis_logic.validate_colour("red") is True
    assert mantis_logic.validate_colour("orange") is True
    assert mantis_logic.validate_colour("yellow") is True
    assert mantis_logic.validate_colour("green") is True
    assert mantis_logic.validate_colour("blue") is True
    assert mantis_logic.validate_colour("purple") is True
    assert mantis_logic.validate_colour("pink") is True

    assert mantis_logic.validate_colour("1") is False

def test_card_generation():
    game = mantis_logic.Mantis()
    for _ in range(100):
        card = game.Card()
        assert card.colour in card.possible_colours

def test_is_valid_name():
    game = mantis_logic.Mantis()
    game.Player(game, None, "Player 1")
    assert game.is_valid_name("Player 1") is False
    assert game.is_valid_name("Player 2") is True
    game.Player(game, None, "Player 2")
    assert game.is_valid_name("Player 1") is False
    assert game.is_valid_name("Player 2") is False

def test_score_action():
    game = mantis_logic.Mantis()
    sample_cards = Sample_Cards()
    assert len(game.deck) == 0

    p1 = game.Player(game, None, "Player 1")

    assert p1.tank == []
    assert p1.score_pile == []

    game.deck = [sample_cards.red_card, sample_cards.green_card]

    p1.tank = [sample_cards.red_card]

    assert game.deck[-1].colour == "green"
    assert game.deck[-2].colour == "red"
    assert p1.tank[0].colour == "red"

    # Unsucessfully score, adding the unmatched green card to tank
    p1.score_action()
    assert p1.score_pile == []
    assert p1.get_tank_colours() == ["red", "green"]

    # Sucessfully score, transferring both red cards to score pile
    p1.score_action()
    assert len(p1.score_pile) == 2
    assert p1.score_pile[0].colour == "red"
    assert p1.score_pile[1].colour == "red"
    assert p1.get_tank_colours() == ["green"]

def test_steal_action():
    game = mantis_logic.Mantis()
    sample_cards = Sample_Cards()
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

    # Unsucesfully steal, giving the drawn green card to p2's tank
    p1.steal_action(p2)
    assert p1.get_tank_colours() == ["green"]
    assert p2.get_tank_colours() == ["red", "green"]
    assert p1.score_pile == []
    assert p2.score_pile == []

    # Sucessfully steal, moving p2's red cards to p1's tank
    p1.steal_action(p2)
    assert p1.get_tank_colours() == ["green", "red", "red"]
    assert p2.get_tank_colours() == ["green"]
    assert p1.score_pile == []
    assert p2.score_pile == []

def test_get_info():
    game = mantis_logic.Mantis()
    sample_cards = Sample_Cards()
    p1 = game.Player(game, None, "Player 1")
    p2 = game.Player(game, None, "Player 2")

    game.deck = [sample_cards.blue_card]
    p1.tank = [sample_cards.green_card, sample_cards.green_card]
    p2.tank = [sample_cards.red_card, sample_cards.red_card]
    p2.score_pile = [sample_cards.green_card]

    info = game.get_info()

    assert info.player_names == ["Player 1", "Player 2"]
    assert info.tank_colours["Player 1"] == ["green", "green"]
    assert info.tank_colours["Player 2"] == ["red", "red"]
    assert info.next_card_possible_colours == ["blue", "orange", "yellow"]
    assert info.scores["Player 1"] == 0
    assert info.scores["Player 2"] == 1