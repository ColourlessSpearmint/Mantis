import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import MantisGame


def test_reset():
    # Note: This test relies on randomness and must be run many times
    game = MantisGame()
    for i in range(100): 
        game.reset_state()
        for player_index in range(4):
            card_quantity = 0
            for color_index in range(7):
                card_quantity += game.state[player_index * 8 + color_index]
            assert card_quantity == 4


def test_generate_card():
    game = MantisGame()
    card = game.generate_card()
    assert len(card) == 4
    assert len(set(card[:-1])) == 3
    assert card[-1] in card[:-1]


def test_new_card():
    game = MantisGame()
    game.new_card()
    assert len(game.state[-4:]) == 4


def test_convert_color():
    game = MantisGame()
    assert game.convert_color(1) == "Red"
    assert game.convert_color(1, "ansi") == "\033[31m"
    assert game.convert_color(8) == "Unknown"


def test_check_gameover():
    game = MantisGame()
    game.reset_state()
    game.state[7] = 1  # Set player 0's score to 1
    assert game.check_gameover() == None  # No player should have won
    game.state[7] = 10  # Set player 0's score to 10
    assert game.check_gameover() == 0  # Player 0 should have won


def test_score_action():
    game = MantisGame()
    game.state[0] = 2  # Player 0 has 2 Red cards
    game.state[7] = 0  # Player 0's score is 0
    game.score_action(0, 1)  # Score with Red card
    assert game.state[0] == 0  # Player 0's Red cards should be 0
    assert game.state[7] == 3  # Player 0's score should be 3
    game.state[7] = 0  # Player 0's score is 0
    game.state[0] = 0  # Player 0 has 0 Red cards
    game.score_action(0, 1)  # Score with Red card
    assert game.state[0] == 1  # Player 0's Red cards should be 0
    assert game.state[7] == 0  # Player 0's score should be 3


def test_steal_action():
    game = MantisGame()
    game.state[0] = 0  # Player 0 has 0 Red cards
    game.state[8] = 2  # Player 1 has 2 Red cards
    game.steal_action(0, 1, 1)  # Player 0 steals Red cards from Player 1
    assert game.state[8] == 0  # Player 1's Red cards should be 0
    assert game.state[0] == 3  # Player 0's Red cards should be 3
    assert game.state[7] == 0  # Player 0's score should be 0
    assert game.state[15] == 0  # Player 1's score should be 0
    game.state[0] = 1  # Player 0 has 0 Red cards
    game.state[8] = 2  # Player 1 has 2 Red cards
    game.steal_action(0, 1, 1)  # Player 0 steals Red cards from Player 1
    assert game.state[8] == 0  # Player 1's Red cards should be 0
    assert game.state[0] == 4  # Player 0's Red cards should be 3
    assert game.state[7] == 0  # Player 0's score should be 0
    assert game.state[15] == 0  # Player 1's score should be 0
