import mantis_logic

def test_convert_to_colour_name():
    assert mantis_logic.convertColourIndexToName(1) == "red"
    assert mantis_logic.convertColourIndexToName(2) == "orange"
    assert mantis_logic.convertColourIndexToName(3) == "yellow"
    assert mantis_logic.convertColourIndexToName(4) == "green"
    assert mantis_logic.convertColourIndexToName(5) == "blue"
    assert mantis_logic.convertColourIndexToName(6) == "purple"
    assert mantis_logic.convertColourIndexToName(7) == "pink"

    assert mantis_logic.convertColourListToNames([1,2,3]) == ["red","orange","yellow"]
    assert mantis_logic.convertColourListToNames([4,5,6]) == ["green","blue","purple"]
    assert mantis_logic.convertColourListToNames([3,5,7]) == ["yellow","blue","pink"]

def test_validate_colour():
    assert mantis_logic.validateColour("red") is True
    assert mantis_logic.validateColour("orange") is True
    assert mantis_logic.validateColour("yellow") is True
    assert mantis_logic.validateColour("green") is True
    assert mantis_logic.validateColour("blue") is True
    assert mantis_logic.validateColour("purple") is True
    assert mantis_logic.validateColour("pink") is True

    assert mantis_logic.validateColour("1") is False
def test_card_generation():
    game = mantis_logic.Mantis()
    for i in range(100):
        card = game.Card()
        assert card.colour in card.possibleColours