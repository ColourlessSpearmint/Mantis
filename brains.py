class RandomBrain:
    import random
    def run(self, info):
        """Chooses a random player to target."""
        num_of_players = len(info.player_names)
        target_index = self.random.randint(0, num_of_players - 1)
        return info.player_names[target_index]


class ScorerBrain:
    def run(self, info):
        """Always tries to score for itself."""
        return info.active_player.name


class BlueShellBrain:
    def run(self, info):
        """Chooses the player with the highest score"""
        highest_score = -1
        best_target = None
        for player_name, score in info.scores.items():
            if score >= highest_score:
                highest_score = score
                best_target = player_name
        return best_target


class MatcherBrain:
    def run(self, info):
        """Chooses the player with the most cards in their tank that match the possible colours of the next card.
        Prioritizes the number of different matching colors, then the quantity of matching colors."""
        pass


class QuantityBrain:
    def run(self, info):
        """Chooses the player with the most cards in their tank."""
        highest_quantity = -1
        highest_quantity_players = []
        for player in info.player_names:
            quantity = len(info.tank_colours[player])
            if quantity > highest_quantity:
                highest_quantity = quantity
                highest_quantity_players = [player]
            elif quantity == highest_quantity:
                highest_quantity_players.append(player)
        if len(highest_quantity_players) == 0:
            return info.player_names[0]
        return highest_quantity_players[0]
