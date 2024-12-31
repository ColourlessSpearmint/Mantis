import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import MantisGame, ScorerBot, MatcherBot, CollectorBot

class mantis:
    def __init__(self):
        self.game = MantisGame()
        self.other_players = [ScorerBot(), MatcherBot(), CollectorBot()]
        self.game.set_player(0, "manual") # Player 0, the NN, is under external control
        self.game.playernames[0] = "NN"
        for i in range(3):
            self.game.set_player(i+1, self.other_players[i])

    def reset(self):
        self.game.reset_state()

    def take_action(self, output_target):
        self.game.simulate_turn(0, output_target, False)
        for i in range(1,4):
            self.game.simulate_turn(i, self.game.players[i].turn(self.game, i), False)

        if self.game.check_gameover() == None:
            is_done = False
        else:
            is_done = True

        return (self.game.state)[:-1], is_done
    
    def get_inputs(self):
        return (self.game.state)[:-1]
    
    def has_won(self):
        if self.game.check_gameover() == 0:
            return True
        else:
            return False
