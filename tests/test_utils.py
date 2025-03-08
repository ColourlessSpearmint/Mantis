import utils

def test_convert_colour_index_to_name():
    assert utils.convert_colour_index_to_name(1) == "red"
    assert utils.convert_colour_index_to_name(2) == "orange"
    assert utils.convert_colour_index_to_name(3) == "yellow"
    assert utils.convert_colour_index_to_name(4) == "green"
    assert utils.convert_colour_index_to_name(5) == "blue"
    assert utils.convert_colour_index_to_name(6) == "purple"
    assert utils.convert_colour_index_to_name(7) == "pink"


def test_convert_colour_list_to_names():
    assert utils.convert_colour_list_to_names([1, 2, 3]) == [
        "red",
        "orange",
        "yellow",
    ]
    assert utils.convert_colour_list_to_names([4, 5, 6]) == [
        "green",
        "blue",
        "purple",
    ]
    assert utils.convert_colour_list_to_names([3, 5, 7]) == [
        "yellow",
        "blue",
        "pink",
    ]


def test_validate_colour():
    assert utils.validate_colour("red") is True
    assert utils.validate_colour("orange") is True
    assert utils.validate_colour("yellow") is True
    assert utils.validate_colour("green") is True
    assert utils.validate_colour("blue") is True
    assert utils.validate_colour("purple") is True
    assert utils.validate_colour("pink") is True

    assert utils.validate_colour("1") is False
