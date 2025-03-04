import mantis_logic

class RandomBrain:
    import random
    def run(self, info):
        """Chooses a random player to target."""
        num_of_players = len(info.player_names)
        target_index = self.random.randint(0, num_of_players-1)
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
        highest_num_of_matches = -1
        highest_num_of_matches_players = []
        for player in info.player_names:
            deduplicated_tank = self.remove_duplicates(info.tank_colours[player])
            num_of_matches = self.count_shared_items(deduplicated_tank, info.next_card_possible_colours)
            if num_of_matches > highest_num_of_matches:
                highest_num_of_matches = num_of_matches
                highest_num_of_matches_players = [player]
            elif num_of_matches == highest_num_of_matches:
                highest_num_of_matches_players.append(player)
        if len(highest_num_of_matches_players) == 0:
            return info.player_names[0]
        if len(highest_num_of_matches_players) == 1:
            return highest_num_of_matches_players[0]
        highest_quantity_of_matches = -1
        highest_quantity_of_matches_players = []
        for player in highest_num_of_matches_players:
            quantity_of_matches = self.count_shared_items(info.tank_colours[player], info.next_card_possible_colours)
            if quantity_of_matches > highest_quantity_of_matches:
                highest_quantity_of_matches = quantity_of_matches
                highest_quantity_of_matches_players = [player]
            elif quantity_of_matches == highest_quantity_of_matches:
                highest_quantity_of_matches_players.append(player)
        return highest_quantity_of_matches_players[0]
    

    def remove_duplicates(self, input_list: list):
        return list(set(input_list))
    
    def count_shared_items(self, list1, list2):
        """Counts shared items using sets."""
        set1 = set(list1)
        set2 = set(list2)
        return len(set1.intersection(set2))