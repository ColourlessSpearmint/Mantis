import random


class MantisGame:
    """
    Game State Encoding:

    p=player
    c=color
    s=score
    dp=deck_possible
    da=deck_actual

    [p1c1,p1c2,p1c3,p1c4,p1c5,p1c6,p1c7,p1s,
    p2c1,p2c2,p2c3,p2c4,p2c5,p2c6,p2c7,p2s,
    p3c1,p3c2,p3c3,p3c4,p3c5,p3c6,p3c7,p3s,
    p4c1,p4c2,p4c3,p4c4,p4c5,p4c6,p4c7,p4s,
    dp1,dp2,dp3,da]
    """

    def __init__(self):
        # Initialize the state with zeros
        self.state = [0] * (7 * 4 + 4 + 3 + 1)
        self.goal = 10
        self.debug = False
        self.playernames = ["Player Zero", "Player One", "Player Two", "Player Three"]
        self.players = ["manual", "manual", "manual", "manual"]

    def set_player(self, player_index, player=None):
        if player == None:
            player = "manual"
        self.players[player_index] = player
        try: 
            self.playernames[player_index] = player.name
        except AttributeError:
            pass

    def generate_card(self):
        """
        Randomly generates a card's three potential colors.
        Returns a tuple of four integers representing the colors.
        """
        possibilies = random.sample(range(1, 8), 3)
        actual = random.sample(possibilies, 1)
        possibilies.append(actual[0])
        return possibilies

    def new_card(self):
        """
        Generates a new card and updates the game state.
        """
        self.state[-4:] = self.generate_card()

    def reset_state(self):
        """
        Resets the game state to an initial random state.
        """
        # Reset game state
        self.state = [0] * (7 * 4 + 4 + 3 + 1)

        # Reset player tanks and scores
        for player in range(4):
            for i in range(4):  # Deal 4 random cards
                state_index = random.randint(0, 7) + (player * 8)
                self.state[state_index] += 1
            self.state[player * 8 + 7] = 0  # Reset score to 0

        # Generate new card actual and possibilities
        self.new_card()

    def convert_color(self, color_index, format="plain"):
        """
        Converts a color index to its corresponding color name or ANSI escape code.

        Args:
            color_index: An integer representing the color index.
            format: The desired output format, either "plain" for color name or "ansi" for ANSI escape code.

        Returns:
            The color name or ANSI escape code corresponding to the index, or "Unknown" if the index is invalid.
        """

        color_map = {
            1: ("Red", "\033[31m"),
            2: ("Orange", "\033[38;5;208m"),
            3: ("Yellow", "\033[33m"),
            4: ("Green", "\033[32m"),
            5: ("Blue", "\033[34m"),
            6: ("Purple", "\033[35m"),
            7: ("Pink", "\033[1;35m"),
        }

        color_info = color_map.get(color_index, ("Unknown", ""))
        return color_info[0] if format == "plain" else color_info[1]

    def print_state(self):
        """
        Prints the game state as a human-readable format
        """
        for player_index in range(4):
            print(f"{self.playernames[player_index]}: ", end="")
            for color_map_index in range(1, 8):
                color_state_index = color_map_index - 1 + (player_index * 8)
                color_quantity = self.state[color_state_index]
                ansi_code = self.convert_color(color_map_index, "ansi")
                if color_quantity != 0:
                    print(f"{ansi_code}{color_quantity}\033[0m", end=", ")
            print(f"Score: {self.state[player_index*8+7]}")

        print("Possible Card Colors: ", end="")
        for card_index in self.state[-4:-1]:
            ansi_code = self.convert_color(card_index, "ansi")
            print(f"{ansi_code}#\033[0m ", end="")
        print()

        if self.debug:
            ansi_code = self.convert_color(self.state[-1], "ansi")
            print(f"(Debug Mode) Actual Card Color: {ansi_code}#\033[0m")

    def check_gameover(self):
        """
        Checks if any player has reached the goal score.

        Returns:
            The index of the winning player, or None if no player has won yet.
        """
        for player_index in range(4):
            if self.state[player_index * 8 + 7] >= self.goal:
                return player_index
        return None

    def reveal_card(self):
        """
        Prints the actual card color with colored text.
        """
        actual_color = self.state[-1]
        ansi_code = self.convert_color(actual_color, "ansi")
        print(f"Actual Card Color: {ansi_code}#\033[0m")

    def action(self, player_index, target_index=None, verbose=True):
        """
        Performs an action from one player to another.

        Args:
            player_index (int): The index of the current player (0-3).
            target_index (int): The index of the target player (0-3).

        Returns:
            None
        """
        # Validate inputs
        assert target_index is not None and target_index < 4, "Invalid target player."

        # Determine action based on target_index
        action = "score" if target_index == player_index else "steal"

        if verbose:
            print(f"{self.playernames[player_index]} ({player_index}) performed action \'{action}\'{f' on {self.playernames[target_index]} ({target_index})' if action=='steal' else ''}.")
        # Extract the card color
        card_color = self.state[-1]

        if action == "score":
            self.score_action(player_index, card_color)
        elif action == "steal":
            self.steal_action(player_index, target_index, card_color)

    def score_action(self, player_index, card_color):
        """
        Perform the score action for the current player.

        Args:
            player_index (int): Index of the current player'.
            card_color (int): The color of the top card.

        Returns:
            None
        """
        tank_index = player_index * 8 + card_color - 1
        tank_quantity = self.state[tank_index]
        if tank_quantity > 0:
            cards_to_score = tank_quantity + 1  # Add one to include the new card
            self.state[tank_index] = 0  # Remove cards from tank
            self.state[player_index * 8 + 7] += cards_to_score  # Add to score pile
        else:
            self.state[tank_index] = (
                1  # If the player does not have that card, give it to them
            )

    def steal_action(self, player_index, target_index, card_color):
        """
        Perform the steal action from the current player to the target player.

        Args:
            player_index (int): Index of the current player.
            target_index (int): Index of the target player.
            card_color (int): The color of the top card.

        Returns:
            None
        """
        target_tank_index = target_index * 8 + card_color - 1
        target_tank_quantity = self.state[target_tank_index]
        if target_tank_quantity > 0:
            cards_to_steal = target_tank_quantity + 1  # Add one to include the new card
            self.state[target_tank_index] = 0  # Remove cards from target's tank
            self.state[
                player_index * 8 + card_color - 1
            ] += cards_to_steal  # Add to current player's tank
        else:
            self.state[target_tank_index] = (
                1  # If the target does not have that card, give it to them
            )

    def simulate_turn(self, player_index, manual_target_index=None, verbose=True):
        """
        Simulates one turn for the specified player.

        Args:
            player_index (int): The index of the current player (0-3).
            manual_target_index (int, optional): The index of the target player (0-3) if the player is manual.
            verbose (bool): Whether to print the state after the turn.

        Returns:
            None
        """
        player = self.players[player_index]
        if player == "manual":
            assert manual_target_index != None # If the player is under manual control, it must specify a target
            target_index = manual_target_index
        else:
            target_index = player.turn(self, player_index)
        self.action(player_index, target_index, verbose)
        self.new_card()
        if verbose:
            self.print_state()

# Example Usage
if __name__ == "__main__":
    game = MantisGame()
    game.debug = True
    game.reset_state()
    game.print_state()
