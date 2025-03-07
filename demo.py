import mantis_logic
from brains import *

def demo(input_brains:list):
    game = mantis_logic.Mantis()
    manual_players = 0
    for brain in input_brains:
        object_name = brain.__name__
        strategy_name = object_name.replace("Brain", "")
        name = strategy_name
        if name == "Manual":
            while True:
                manual_players += 1
                player_input = input(f"Manual Player {manual_players}, choose a name: ")
                if game.is_valid_new_name(player_input):
                    name = player_input
                    break
                else:
                    print(f"Invalid name: '{player_input}'. Try again.")
                    continue
        else:
            for i in range(2, 100):
                if not game.is_valid_new_name(name):
                    name = f"{strategy_name}{i}"
                else:
                    break
        game.Player(game, brain, name)
    game.start_game()
    game.print_info()
    while not game.game_over_message():
        game.simulate_turn()
        game.print_info()
    print(game.game_over_message())

if __name__ == "__main__":
    brains = [
        ManualBrain,
        RandomBrain,
        ScorerBrain,
        KleptoBrain,
        QuantityBrain,
        QuantityBrain
    ]
    demo(brains)
