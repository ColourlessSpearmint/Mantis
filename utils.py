COLOUR_DICT = {
    "red": {"index": 1, "name": "red", "emoji": "❤️"},
    "orange": {"index": 2, "name": "orange", "emoji": "🧡"},
    "yellow": {"index": 3, "name": "yellow", "emoji": "💛"},
    "green": {"index": 4, "name": "green", "emoji": "💚"},
    "blue": {"index": 5, "name": "blue", "emoji": "💙"},
    "purple": {"index": 6, "name": "purple", "emoji": "💜"},
    "pink": {"index": 7, "name": "pink", "emoji": "🩷"},
}


def convert_colour_index_to_name(colour_index: int) -> str:
    for colour in COLOUR_DICT.values():
        if colour["index"] == colour_index:
            return colour["name"]
    raise LookupError(f"Invalid colour_index: \'{colour_index}\'")


def convert_colour_list_to_names(colour_index_list: list) -> list:
    colour_name_list = []
    for colour_index in colour_index_list:
        colour_name_list.append(convert_colour_index_to_name(colour_index))
    return colour_name_list


def convert_colour_name_to_emoji(colour_name: str) -> str:
    return COLOUR_DICT[colour_name]["emoji"]


def convert_colour_list_to_emojis(colour_name_list: list) -> list:
    colour_emoji_list = []
    for colour_name in colour_name_list:
        colour_emoji_list.append(convert_colour_name_to_emoji(colour_name))
    return colour_emoji_list


def validate_colour(colour: str = "") -> bool:
    return colour.lower() in COLOUR_DICT


def get_tank_colours(player) -> list:
    """Returns a list of the colours in this player's tank."""
    tank_colours = []
    for card in player.tank:
        tank_colours.append(card.colour)
    return tank_colours


def get_matching_colours_in_list(input_list: list, colour: str) -> list:
    """Returns a list of the cards in this player's tank that match the given colour."""
    assert validate_colour(colour)
    matching_cards = []
    for card in input_list:
        if colour == card.colour:
            matching_cards.append(card)
    return matching_cards


def get_matching_colours_of_player(player, colour: str) -> list:
    return get_matching_colours_in_list(player.tank, colour)


def move_colours_from_list(source_list: list, colour: str, target_list: list):
    for card in get_matching_colours_in_list(source_list, colour):
        source_list.remove(card)
        target_list.append(card)


def move_colours_from_tank(player, colour: str, target_list: list):
    move_colours_from_list(player.tank, colour, target_list)
