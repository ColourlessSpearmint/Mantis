from game_logic import MantisGame
import random

class MatcherBot:
    """
    Strategy: Matcher
    - Chooses the player (including itself) who has the largest number of matching cards.
    - Uses the quantity of matching cards as a tiebreaker.
    """
    def turn(self, game, self_index):
        max_cards = 0
        target_index = self_index
        card_possibilities = game.state[-4:-1]
        
        for player_index in range(4):
            card_count = sum(game.state[player_index * 8 + color - 1] for color in card_possibilities)
            if card_count > max_cards:
                max_cards = card_count
                target_index = player_index
        
        game.take_turn(self_index, target_index)

class ScorerBot:
    """
    Strategy: Scorer
    - Scores if it has ANY of the colors on the draw pile.
    - Steals from the player with the most matching colors otherwise.
    """
    def turn(self, game, self_index):
        card_possibilities = game.state[-4:-1]
        self_card_count = sum(game.state[self_index * 8 + color - 1] for color in card_possibilities)
        
        if self_card_count > 0:
            game.take_turn(self_index, self_index)
        else:
            max_cards = 0
            target_index = self_index
            for player_index in range(4):
                if player_index != self_index:
                    card_count = sum(game.state[player_index * 8 + color - 1] for color in card_possibilities)
                    if card_count > max_cards:
                        max_cards = card_count
                        target_index = player_index
            game.take_turn(self_index, target_index)

class ThiefBot:
    """
    Strategy: Thief
    - Scores if it has ALL of the colors on the draw pile.
    - Steals from the player with the most matching colors otherwise.
    """
    def turn(self, game, self_index):
        card_possibilities = game.state[-4:-1]
        self_card_count = sum(game.state[self_index * 8 + color - 1] for color in card_possibilities)
        
        if self_card_count == len(card_possibilities):
            game.take_turn(self_index, self_index)
        else:
            max_cards = 0
            target_index = self_index
            for player_index in range(4):
                if player_index != self_index:
                    card_count = sum(game.state[player_index * 8 + color - 1] for color in card_possibilities)
                    if card_count > max_cards:
                        max_cards = card_count
                        target_index = player_index
            game.take_turn(self_index, target_index)

class RandomBot:
    """
    Strategy: Random
    - Chooses a random player (including itself) for each decision.
    """
    def turn(self, game, self_index):
        target_index = random.randint(0, 3)
        game.take_turn(self_index, target_index)

if __name__ == "__main__":
    game = MantisGame()
    game.debug = True
    game.reset_state()
    game.print_state()

    rounds = 5
    p0 = MatcherBot()
    p1 = ScorerBot()
    p2 = ThiefBot()
    p3 = RandomBot()
    for i in range(rounds):
        p0.turn(game, 0)
        game.new_card()
        game.print_state()
        p1.turn(game, 1)
        game.new_card()
        game.print_state()
        p2.turn(game, 2)
        game.new_card()
        game.print_state()
        p3.turn(game, 3)
        game.new_card()
        game.print_state()