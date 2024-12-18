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

    def __init__(self, debug=False):
        # Initialize the state with zeros
        self.state = [0] * (7 * 4 + 4 + 3 + 1)
        self.debug = debug

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
        self.state[-4:] = self.generate_card()

    def reset_state(self):
        """
        Resets the game state to an initial random state.
        """
        # Reset player tanks and scores
        for player in range(4):
            for i in range(4): # Deal 4 random cards
                state_index = random.randint(0,7)+(player*8)
                self.state[state_index] += 1
            self.state[player * 8 + 7] = 0  # Reset score to 0

        # Generate a new deck card
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
            7: ("Pink", "\033[1;35m")
        }

        color_info = color_map.get(color_index, ("Unknown", ""))
        return (color_info[0] if format == "plain" else color_info[1])
    
    def print_state(self):
        """
        Prints the game state as a human-readable format
        """
        for player_index in range(4):
            print(f"Player {player_index}: ", end="")
            for color_map_index in range(1,8):
                color_state_index = color_map_index-1+(player_index*8)
                ansi_code = self.convert_color(color_map_index, "ansi")
                print(f"{ansi_code}{self.state[color_state_index]}\033[0m", end=', ')
            print(f"Score: {self.state[player_index*8+7]}")

        print("Possible Card Colors: ", end='')
        for card_index in self.state[-4:-1]:
            ansi_code = self.convert_color(card_index, "ansi")
            print(f"{ansi_code}#\033[0m ", end='')
        print()

        if self.debug:
            ansi_code = self.convert_color(self.state[-1], "ansi")
            print(f"(Debug Mode) Actual Card Color: {ansi_code}#\033[0m")

# Example Usage
if __name__ == "__main__":
    game = MantisGame(debug=True)
    game.reset_state()
    game.print_state()
