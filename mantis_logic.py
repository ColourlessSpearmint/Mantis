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
    "red": {"index": 1, "name": "red", "emoji": "🟥"},
    "orange": {"index": 2, "name": "orange", "emoji": "🟧"},
    "yellow": {"index": 3, "name": "yellow", "emoji": "🟨"},
    "green": {"index": 4, "name": "green", "emoji": "🟩"},
    "blue": {"index": 5, "name": "blue", "emoji": "🟦"},
    "purple": {"index": 6, "name": "purple", "emoji": "🟪"},
    "pink": {"index": 7, "name": "pink", "emoji": "🌸"},
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

    class Card:
        def __init__(self):
            self.possible_colours = []
            self.assign_random_possible_colours()
            self.assign_random_colour()

        def assign_random_possible_colours(self):
            self.possible_colours = convert_colour_list_to_names(random.sample(range(1, NUM_OF_COLOURS+1), NUM_OF_POSSIBLE_COLOURS))

        def assign_random_colour(self):
            self.colour = self.possible_colours[random.randint(1, NUM_OF_POSSIBLE_COLOURS)-1]

    class Player:
        def __init__(self, game, brain, name):
            self.game = game
            if game.is_valid_name(name):
                self.name = name
            else:
                raise ValueError(f"Duplicate names are not allowed: \'{name}\'")
            self.tank = []
            self.score_pile = []
            self.brain = brain
        
        def print_tank(self):
            
            tank_colours = []
            for card in self.tank:
                tank_colours.append(card.colour)
            print(f"{self.name}'s Tank: {tank_colours}")

        def get_matching_colours(self, colour):
            assert validate_colour(colour)
            matching_cards = []
            for card in self.tank:
                if colour == card.colour:
                    matching_cards.append(card)
            return matching_cards

        def take_turn(self):
            target = self.brain.run()
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

def validate_colour(colour=""):
    return colour.lower() in COLOUR_DICT

