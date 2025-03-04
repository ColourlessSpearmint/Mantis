import pytest
import mantis_logic

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
    
def test_score_action():
    game = mantis_logic.Mantis()
    assert len(game.deck) == 0

    p1 = game.Player(game, None, "Player 1")

    assert p1.tank == []
    assert p1.score_pile == []

    red_card = game.Card()
    red_card.colour = "red"
    green_card = game.Card()
    green_card.colour = "green"
    game.deck = [red_card, green_card]

    p1.tank = [red_card]

    assert game.deck[-1].colour == "green"
    assert game.deck[-2].colour == "red"
    assert p1.tank[0].colour == "red"

    # Unsucessfully score, adding the unmatched green card to tank
    p1.score_action()
    assert p1.score_pile == []
    assert p1.tank[0].colour == "red"
    assert p1.tank[1].colour == "green"

    # Sucessfully score, transferring both red cards to score pile
    p1.score_action()
    assert len(p1.score_pile) == 2
    assert p1.score_pile[0].colour == "red"
    assert p1.score_pile[1].colour == "red"
    assert p1.tank[0].colour == "green"

def test_steal_action():
    game = mantis_logic.Mantis()
    assert len(game.deck) == 0

    p1 = game.Player(game, None, "Player 1")
    p2 = game.Player(game, None, "Player 2")

    assert p1.tank == []
    assert p1.score_pile == []
    assert p2.tank == []
    assert p2.score_pile == []

    red_card = game.Card()
    red_card.colour = "red"
    green_card = game.Card()
    green_card.colour = "green"
    game.deck = [red_card, green_card]

    p1.tank = [green_card]
    p2.tank = [red_card]

    # Unsucesfully steal, giving the drawn green card to p2's tank
    p1.steal_action(p2)
    assert p1.tank[0].colour == "green"
    assert p2.tank[0].colour == "red"
    assert p2.tank[1].colour == "green"
    assert p1.score_pile == []
    assert p2.score_pile == []

    # Sucessfully steal, moving p2's red cards to p1's tank
    p1.steal_action(p2)
    assert p1.tank[0].colour == "green"
    assert p1.tank[1].colour == "red"
    assert p1.tank[2].colour == "red"
    assert p2.tank[0].colour == "green"
    assert p1.score_pile == []
    assert p2.score_pile == []
