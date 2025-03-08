"""
Mantis Rules
https://www.explodingkittens.com/pages/how-to-play-mantis

## Game Overview
- Players aim to be the first to collect 10+ cards in their Score Pile
- 2-6 Players
- 105 Cards
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

from utils import *

NUM_OF_COLOURS = len(COLOUR_DICT)
NUM_OF_POSSIBLE_COLOURS_PER_CARD = 3
DECK_SIZE = 105
STARTING_TANK_SIZE = 4
DEFAULT_GOAL = 10
MIN_PLAYERS = 2
MAX_PLAYERS = 6


class Mantis:
    def __init__(self):
        self.players = []
        self.deck = []
        self.goal = DEFAULT_GOAL
        self.turns = 0
        self.history = []

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

    def is_valid_num_of_players(self) -> bool:
        number_of_players = len(self.players)
        return MIN_PLAYERS <= number_of_players <= MAX_PLAYERS

    def start_game(self):
        assert self.is_valid_num_of_players()
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

    def is_valid_new_name(self, input_name:str) -> bool:
        """Checks if the given name is valid for a new player."""
        name = input_name.strip().lower()
        if self.is_existing_name(name):
            return False
        if name in DISALLOWED_NAMES:
            return False
        return True

    def is_existing_name(self, name:str) -> bool:
        """Checks if the given name is already in use."""
        for player in self.players:
            if player.name.lower() == name.lower():
                return True
        return False

    def simulate_turn(self):
        current_player = self.players[self.turns % len(self.players)]
        result = current_player.take_turn()
        self.history.append(result)
        self.turns += 1
        return result

    def get_highest_score_player(self):
        """Returns the player with the highest score"""
        winner = None
        highest_score = -1
        for player in self.players:
            if len(player.score_pile) > highest_score:
                highest_score = len(player.score_pile)
                winner = player
        return winner

    def game_over_message(self) -> str:
        for player in self.players:
            if len(player.score_pile) >= self.goal:
                winner = self.get_highest_score_player()
                winner_score = len(winner.score_pile)
                return f"{winner.name} won with a score of {winner_score}!"
        if len(self.deck) == 0:
            return "Ran out of cards"
        return ""  # If the game isn't over, we return a Falsy string

    def get_last_history_text(self, turn):
        history = self.history
        try:
            last_history = history[turn-1]
        except IndexError:
            return "No history."

        active_player = last_history['active_player']
        action = last_history['action']
        target = last_history['target']
        cards_moved = last_history['cards_moved']
        outcome = last_history['outcome']
        card_actual_colour = last_history['card_actual_colour']
        card_actual_colour_emoji = convert_colour_name_to_emoji(card_actual_colour)

        outcome_text = ""
        match outcome:
            case "success":
                outcome_text = "successfully"
            case "fail":
                outcome_text = "unsuccessfully"

        match action:
            case "score":
                return f"{active_player} {outcome_text} scored {cards_moved} {card_actual_colour_emoji} cards."
            case "steal":
                return f"{active_player} {outcome_text} stole {cards_moved} {card_actual_colour_emoji} cards from {target}."

    def print_info(self):
        turn_count = self.turns
        print(f"Turn {turn_count}: {self.get_last_history_text(turn_count)}")

        info = self.get_info(shuffle=False)
        for player in info.player_names:
            tank_colours = info.tank_colours[player]
            tank_emojis = convert_colour_list_to_emojis(tank_colours)
            tank_emojis_spaced_string = list_to_spaced_string(tank_emojis)
            print(
                f"{player} - Tank: {tank_emojis_spaced_string}, Score: {info.scores[player]}"
            )

        next_card_possible_colours = info.next_card_possible_colours
        if next_card_possible_colours:
            next_card_possible_colours_emojis = convert_colour_list_to_emojis(next_card_possible_colours)
            next_card_possible_colours_emojis_spaced_string = list_to_spaced_string(next_card_possible_colours_emojis)
            print(
                f"Next card possible colours: {next_card_possible_colours_emojis_spaced_string}"
            )
        else:
            print(
                "No cards left in the deck."
            )
        print()


    def get_info(self, shuffle=True):
        return self.Info(self, shuffle)

    class Info:
        """
        A struct for securely exposing public gamestate information.
        Has a parameter to shuffle the players to remove bias from poorly-coded Brains.

        - player_names: a list of the names of players.
                    Example: ["Player 1", "Player 2", "Player 3"]

        - tank_colours: a dictionary showing the colours of cards in each player's tank.
                    - Keys: player names (str).
                    - Values: a list of strings, where each string is a card colour (e.g., "red", "blue") in that player's tank.
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

        def __init__(self, parent_game, shuffle=True):
            # self.game = parent_game  # For security reasons, we don't expose the game object.
            input_player_names = parent_game.players.copy()
            if shuffle:
                random.shuffle(input_player_names)

            self.player_names = []
            self.tank_colours = {}
            self.scores = {}

            for player in input_player_names:
                self.player_names.append(player.name)
                self.tank_colours[player.name] = player.get_self_tank_colours()
                self.scores[player.name] = len(player.score_pile)

            if len(parent_game.deck) > 0:
                self.next_card_possible_colours = parent_game.deck[-1].possible_colours
            else:
                self.next_card_possible_colours = []

            self.active_player = parent_game.players[
                parent_game.turns % len(parent_game.players)
            ]  # It's important that this is NOT shuffled

    class Card:
        def __init__(self, auto_generate=True):
            self.possible_colours = []
            self.colour = ""
            if auto_generate:
                self.assign_random_possible_colours()
                self.assign_random_colour()

        def assign_random_possible_colours(self):
            """Assigns random possible colours to this card"""
            self.possible_colours = convert_colour_list_to_names(
                random.sample(
                    range(1, NUM_OF_COLOURS + 1), NUM_OF_POSSIBLE_COLOURS_PER_CARD
                )
            )

        def assign_random_colour(self):
            """Assigns a random colour to this card from its possible colours"""
            if self.possible_colours:
                self.colour = random.choice(self.possible_colours)
            else:
                self.assign_random_possible_colours()
                self.assign_random_colour()

    class Player:
        def __init__(self, parent_game, brain, name):
            self.game = parent_game
            if self.game.is_valid_new_name(name):
                self.name = name
            else:
                raise ValueError(f"Invalid Player Name: '{name}'")
            self.game.players.append(self)
            self.tank = []
            self.score_pile = []
            self.brain = brain

        def get_self_tank_colours(self):
            return get_tank_colours(self)

        def get_player_object_from_name(self, name:str):
            for player in self.game.players:
                if player.name.lower() == name.lower():
                    return player
            return None

        def take_turn(self):
            info = self.game.get_info(shuffle=True)
            target_name = self.brain.run(self.brain, info).lower()
            target = self.get_player_object_from_name(target_name)
            if target is None:
                raise ValueError(f"Invalid target name: '{target_name}'")
            result = self.action(target)
            result["active_player"] = self.name
            result["target"] = target.name
            return result

        def action(self, target) -> dict:
            if target.name == self.name:
                return self.score_action()
            else:
                return self.steal_action(target)

        def steal_action(self, target) -> dict:
            card = self.game.draw_card()
            if get_matching_colours_of_player(target, card.colour):
                target.tank.append(card)
                cards_moved = move_colours_from_tank(target, card.colour, self.tank)
                outcome = "success"
            else:
                target.tank.append(card)
                cards_moved = 1
                outcome = "fail"

            result = {
                "card_actual_colour": card.colour,
                "cards_moved": cards_moved,
                "outcome": outcome,
                "action": "steal"
            }
            return result

        def score_action(self) -> dict:
            card = self.game.draw_card()
            if self.get_self_matching_colours(card.colour):
                self.tank.append(card)
                cards_moved = self.move_colours_from_self_tank(card.colour, self.score_pile)
                outcome = "success"
            else:
                self.tank.append(card)
                cards_moved = 1
                outcome =  "fail"

            result = {
                "card_actual_colour": card.colour,
                "cards_moved": cards_moved,
                "outcome": outcome,
                "action": "score"
            }
            return result


        def move_colours_from_self_tank(self, colour: str, target: list) -> int:
            return move_colours_from_tank(self, colour, target)

        def get_self_matching_colours(self, colour: str) -> list:
            return get_matching_colours_of_player(self, colour)
