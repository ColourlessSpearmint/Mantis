import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import MantisGame
import src.bots as bots

def test_match_player():
    game = MantisGame()

    # No other player has any of the colors
    game.load_gamestate(0)
    assert bots.MatchPlayer(game) == 0

    # All players have at least one matching color
    game.load_gamestate(1)
    assert bots.MatchPlayer(game) == 3

    # Players 1 and 2 have equivalent quantities and numbers of matching colors
    game.load_gamestate(2)
    assert bots.MatchPlayer(game) == 1

    # Player 1 has a greater quantity of matching colors
    game.load_gamestate(3)
    assert bots.MatchPlayer(game) == 1

    # No player has any matching cards, but the default is player 2
    game.load_gamestate(4)
    assert bots.MatchPlayer(game, 2) 

def test_MatcherBot():
    game = MantisGame()
    bot = bots.MatcherBot()
    
    game.load_gamestate(0)
    assert bot.turn(game, 0) == 0

    game.load_gamestate(1)
    assert bot.turn(game, 2) == 3

    game.load_gamestate(2)
    assert bot.turn(game, 3) == 1

    # If no player has any of the cards (scenario 4), the bot should return its player index
    game.load_gamestate(4)
    assert bot.turn(game, 0) == 0
    assert bot.turn(game, 1) == 1
    assert bot.turn(game, 2) == 2
    assert bot.turn(game, 3) == 3

def test_ScorerBot():
    game = MantisGame()
    bot = bots.ScorerBot()
    
    game.load_gamestate(0)
    assert bot.turn(game, 0) == 0

    game.load_gamestate(1)
    assert bot.turn(game, 2) == 2

    game.load_gamestate(2)
    assert bot.turn(game, 3) == 3
