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
