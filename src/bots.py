try:
    from src import MantisGame
except ModuleNotFoundError:
    from game_logic import MantisGame
import random


def MatchPlayer(game, self_index):
    max_cards = 0
    target_index = self_index  # Default to scoring (in case no player has any matching colors)
    card_possibilities = game.state[-4:-1]

    for player_index in range(4):
        card_count = 0
        for color in card_possibilities:
            if game.state[player_index * 8 + color - 1]:
                card_count += 1
        if card_count > max_cards:
            max_cards = card_count
            target_index = player_index

    return target_index


class MatcherBot:
    """
    Strategy: Matcher
    - Chooses the player (including itself) who has the most matching colors.
    """

    def __init__(self):
        self.name = "MatcherBot"

    def turn(self, game, self_index):
        return MatchPlayer(game, self_index)


class ScorerBot:
    """
    Strategy: Scorer
    - Scores every turn.
    """

    def __init__(self):
        self.name = "ScorerBot"

    def turn(self, game, self_index):
        target_index = self_index
        return target_index


class CertaintyBot:
    """
    Strategy: Certainty
    - Scores if it has ANY of the colors on the draw pile.
    - Chooses the player with the most matching colors otherwise.
    """

    def __init__(self):
        self.name = "CertaintyBot"

    def turn(self, game, self_index):
        card_possibilities = game.state[-4:-1]
        self_card_count = 0
        for color in card_possibilities:
            if game.state[self_index * 8 + color - 1]:
                self_card_count += 1

        if self_card_count > 0:
            return self_index
        else:
            return MatchPlayer(game, self_index)


class ThiefBot:
    """
    Strategy: Thief
    - Scores if it has ALL of the colors on the draw pile.
    - Chooses the player with the most matching colors otherwise.
    """

    def __init__(self):
        self.name = "ThiefBot"

    def turn(self, game, self_index):
        card_possibilities = game.state[-4:-1]
        self_card_count = 0
        for color in card_possibilities:
            if game.state[self_index * 8 + color - 1]:
                self_card_count += 1

        if self_card_count == len(card_possibilities):
            return self_index
        else:
            return MatchPlayer(game, self_index)


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


class DefenderBot:
    """
    Strategy: Defender
    - Chooses the player (including itself) with the highest score, so long as they have ANY matching cards.
    - Chooses the player with the most matching colors otherwise.
    """

    def __init__(self):
        self.name = "DefenderBot"

    def turn(self, game, self_index):
        max_score = 0
        target_index = MatchPlayer(game, self_index)
        for player_index in range(4):
            card_possibilities = game.state[-4:-1]
            card_count = 0
            for color in card_possibilities:
                if game.state[player_index * 8 + color - 1]:
                    card_count += 1
            if card_count > 0:
                player_score = game.state[player_index * 8 + 7]
                if player_score > max_score:
                    max_score = player_score
                    target_index = player_index
        return target_index


def bot_duel(players=["default"], verbose=True):
    """
    Simulates a game of Mantis between a specifiable sequence of bots

    Args:
        players (list): Ordered list of players in the game
        verbose (bool): Whether to print the state after each turn.

    Returns:
        winner (int): The index of the winning player.
        turns (int): The number of turns that elapsed in the game.
        state (list): the game state at the end of the game.
    """
    if players != ["default"]:
        assert len(players) == 4

    game = MantisGame()
    game.reset_state()
    if verbose:
        game.print_state()

    if players == ["default"]:  # If no custom players are chosen, use the default bots
        players = [MatcherBot(), ScorerBot(), ThiefBot(), RandomBot()]
    for i in range(4):
        game.set_player(i, players[i])

    turns = 0
    while game.check_gameover() == None:
        if verbose:
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
