"""
Mantis Rules
https://www.explodingkittens.com/pages/how-to-play-mantis

## Game Overview
- Players aim to be the first to collect 10+ cards in their Score Pile
- 2-4 Players
- Game uses 60 cards (6 colour, 10 of each colour)
- Cards have two sides: white side (front) and peach side (back) with three different colours
- The colour on the front is always one of the three colours shown on the back
- The seven colours are: red, orange, yellow, green, blue, purple, pink

## Setup
- Shuffle the deck
- Deal 4 cards face up (white side) to each player's Tank (hand)
- Play proceeds clockwise

## Turn Structure
On your turn, choose ONE of these two actions:

1. **Try to Score**:
   - Take the top card from the Draw Pile
   - Flip it over in YOUR Tank
   - If the card colour matches any cards in your Tank:
     - Move ALL cards of that colour (including the new one) to your Score Pile
   - If no match:
     - Leave the card in your Tank

2. **Try to Steal**:
   - Take the top card from the Draw Pile
   - Flip it over in ANOTHER player's Tank
   - If the card colour matches any cards in their Tank:
     - Move ALL cards of that colour (including the new one) to YOUR Tank
   - If no match:
     - Leave the card in their Tank

## Winning
- First player with 10+ cards in their Score Pile wins
- If Draw Pile runs out, player with most cards in Score Pile wins
- If tied on Score Pile size, player with most cards in Tank wins
"""


import random

COLOUR_DICT = {
    "red": {"index": 1, "name": "red", "emoji": "❤️"},
    "orange": {"index": 2, "name": "orange", "emoji": "🧡"},
    "yellow": {"index": 3, "name": "yellow", "emoji": "💛"},
    "green": {"index": 4, "name": "green", "emoji": "💚"},
    "blue": {"index": 5, "name": "blue", "emoji": "💙"},
    "purple": {"index": 6, "name": "purple", "emoji": "💜"},
    "pink": {"index": 7, "name": "pink", "emoji": "🩷"},
}
NUM_OF_COLOURS = len(COLOUR_DICT)
NUM_OF_POSSIBLE_COLOURS = 3
DECK_SIZE = 105
STARTING_TANK_SIZE = 4
DEFAULT_GOAL = 10

class Mantis:
    def __init__(self):
        self.players = []
        self.deck = []
        self.goal = DEFAULT_GOAL
        self.turns = 0

    def draw_card(self):
        """Returns and pops (REMOVES) the top card from the deck."""
        return self.deck.pop()
    
    def generate_card(self, possible_colours, random_colour=True):
        card = self.Card()
        card.possible_colours = possible_colours
        if random_colour:
            card.assign_random_colour()
        else:
            card.colour = possible_colours[0]
        return card

    def start_game(self):
        self.shuffle_deck()
        self.deal_cards()

    def deal_cards(self):
        for player in self.players:
            new_tank = []
            for i in range(STARTING_TANK_SIZE):
                new_tank.append(self.draw_card())
            player.tank = new_tank

    def shuffle_deck(self):
        new_deck = []
        for i in range(DECK_SIZE):
            new_deck.append(self.Card())
        self.deck = new_deck

    def is_valid_name(self, name):
        for player in self.players:
            if player.name == name:
                return False
        return True
    
    def simulate_turn(self):
        current_player = self.players[self.turns % len(self.players)]
        current_player.take_turn()
        self.turns += 1
    
    def print_info(self):
        info = self.get_info()
        print(f"Next card: {convert_colour_list_to_emojis(info.next_card_possible_colours)}")
        for player in info.player_names:
            print(f"{player} - Tank: {convert_colour_list_to_emojis(info.tank_colours[player])}, Score: {info.scores[player]}")
        
    def get_info(self, shuffle=True):
        return self.Info(self, shuffle)

    class Info:
        """
        A struct for securely exposing public gamestate information.
        Has a parameter to shuffle the players to remove bias from poorly-coded Brains.
        
        - player_names: a list of the names of players.
                    Example: ["Player 1", "Player 2", "Player 3"]

        - tank_colours: a dictionary showing the colors of cards in each player's tank.
                    - Keys: player names (str).
                    - Values: a list of strings, where each string is a card color (e.g., "red", "blue") in that player's tank.
                    Example:
                    {
                        "Player 1": ["red", "green"],
                        "Player 2": ["orange", "purple", "yellow"],
                        "Player 3": ["pink", "blue", "green", "green"]
                    }

        - scores: a dict where keys are player names and values are the number of cards in their score pile.
                    - Keys: player names (str).
                    - Values: an int representing the size of that player's score pile.
                    Example:
                    {
                        "Player 1": 0,
                        "Player 2": 3,
                        "Player 3": 7
                    }

        - next_card_possible_colours: a list of the possible colours of the next card in the deck.
                    Example: ["red", "orange", "yellow"]
        - active_player: the player whose turn it is next/currently.
        """
        def __init__(self, game, shuffle=True):
            input_player_names = game.players.copy()
            if shuffle:
                random.shuffle(input_player_names)

            self.player_names = []
            self.tank_colours = {}
            self.scores = {}

            for player in input_player_names:
                self.player_names.append(player.name)
                self.tank_colours[player.name] = player.get_tank_colours()
                self.scores[player.name] = (len(player.score_pile))

            self.next_card_possible_colours = game.deck[-1].possible_colours

            self.active_player = game.players[game.turns % len(game.players)]  # It's important that this is NOT shuffled

    class Card:
        def __init__(self):
            self.possible_colours = []
            self.assign_random_possible_colours()
            self.assign_random_colour()

        def assign_random_possible_colours(self):
            self.possible_colours = convert_colour_list_to_names(random.sample(range(1, NUM_OF_COLOURS+1), NUM_OF_POSSIBLE_COLOURS))

        def assign_random_colour(self):
            self.colour = random.choice(self.possible_colours)

    class Player:
        def __init__(self, game, brain, name):
            self.game = game
            if game.is_valid_name(name):
                self.name = name
            else:
                raise ValueError(f"Duplicate names are not allowed: \'{name}\'")
            self.game.players.append(self)
            self.tank = []
            self.score_pile = []
            self.brain = brain
        
        def get_tank_colours(self):
            tank_colours = []
            for card in self.tank:
                tank_colours.append(card.colour)
            return tank_colours

        def get_matching_colours(self, colour):
            assert validate_colour(colour)
            matching_cards = []
            for card in self.tank:
                if colour == card.colour:
                    matching_cards.append(card)
            return matching_cards

        def take_turn(self):
            info = self.game.get_info(shuffle=True)
            target_name = self.brain.run(self.brain, info)
            for player in self.game.players:
                if player.name == target_name:
                    target = player
            if target is None:
                raise ValueError(f"Invalid target name: \'{target_name}\'")
            self.action(target)

        def action(self, target):
            if target.name == self.name:
                self.steal_action()
            else:
                self.score_action()

        def steal_action(self, target):
            card = self.game.draw_card()
            if target.get_matching_colours(card.colour):
                target.tank.append(card)
                target.move_colours(card.colour, self.tank)
            else:
                target.tank.append(card)

        def score_action(self):
            card = self.game.draw_card()
            if self.get_matching_colours(card.colour):
                self.tank.append(card)
                self.move_colours(card.colour, self.score_pile)
            else:
                self.tank.append(card)
        
        def move_colours(self, colour, target: list):
            for card in self.get_matching_colours(colour):
                self.tank.remove(card)
                target.append(card)

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

def validate_colour(colour=""):
    return colour.lower() in COLOUR_DICT

# A demo of print_info()
if __name__ == "__main__":
    game = Mantis()
    game.Player(game, None, "Player 1")
    game.Player(game, None, "Player 2")
    game.start_game()
    game.print_info()
