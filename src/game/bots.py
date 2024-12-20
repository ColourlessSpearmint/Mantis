from game import MantisGame
import random


class MatcherBot:
    """
    Strategy: Matcher
    - Chooses the player (including itself) who has the largest number of matching cards.
    """

    def __init__(self):
        self.name = "MatcherBot"

    def turn(self, game, self_index):
        max_cards = 0
        target_index = self_index
        card_possibilities = game.state[-4:-1]

        for player_index in range(4):
            card_count = sum(
                game.state[player_index * 8 + color - 1] for color in card_possibilities
            )
            if card_count > max_cards:
                max_cards = card_count
                target_index = player_index

        return target_index


class ScorerBot:
    """
    Strategy: Scorer
    - Scores if it has ANY of the colors on the draw pile.
    - Steals from the player with the most matching colors otherwise.
    """

    def __init__(self):
        self.name = "ScorerBot"

    def turn(self, game, self_index):
        card_possibilities = game.state[-4:-1]
        self_card_count = sum(
            game.state[self_index * 8 + color - 1] for color in card_possibilities
        )

        if self_card_count > 0:
            return self_index
        else:
            max_cards = 0
            target_index = self_index
            for player_index in range(4):
                if player_index != self_index:
                    card_count = sum(
                        game.state[player_index * 8 + color - 1]
                        for color in card_possibilities
                    )
                    if card_count > max_cards:
                        max_cards = card_count
                        target_index = player_index
            return target_index


class ThiefBot:
    """
    Strategy: Thief
    - Scores if it has ALL of the colors on the draw pile.
    - Steals from the player with the most matching colors otherwise.
    """

    def __init__(self):
        self.name = "ThiefBot"

    def turn(self, game, self_index):
        card_possibilities = game.state[-4:-1]
        self_card_count = sum(
            game.state[self_index * 8 + color - 1] for color in card_possibilities
        )

        if self_card_count == len(card_possibilities):
            return self_index
        else:
            max_cards = 0
            target_index = self_index
            for player_index in range(4):
                if player_index != self_index:
                    card_count = sum(
                        game.state[player_index * 8 + color - 1]
                        for color in card_possibilities
                    )
                    if card_count > max_cards:
                        max_cards = card_count
                        target_index = player_index
            return target_index


class RandomBot:
    """
    Strategy: Random
    - Chooses a random player (including itself) for each decision.
    """

    def __init__(self):
        self.name = "RandomBot"

    def turn(self, game, self_index):
        target_index = random.randint(0, 3)
        return target_index


def bot_duel(verbose=True):
    """
    Simulates a game of Mantis between the four prebuilt bots

    Args:
        verbose (bool): Whether to print the state after each turn.

    Returns:
        winner (int): The index of the winning player.
        turns (int): The number of turns that elapsed in the game.
    """
    game = MantisGame()
    game.reset_state()
    if verbose:
        game.print_state()

    game.set_player(0, MatcherBot())
    game.set_player(1, ScorerBot())
    game.set_player(2, ThiefBot())
    game.set_player(3, RandomBot())

    turns = 0
    while game.check_gameover() == None:
        print()
        game.simulate_turn(turns % 4, verbose=verbose)
        turns += 1
    winner = game.check_gameover()
    state = game.state
    if verbose:
        print(f"\n{game.get_playername(winner)} won in {turns} turns.")
    return winner, turns, state


if __name__ == "__main__":
    bot_duel()
