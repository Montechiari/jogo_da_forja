class Advantage:
    def __init__(self, who=None, kind=None):
        self.who = who
        self.kind = kind


class TurnManager:
    def __init__(self, players):
        # players is a pair of Combatent instances, found in combatents.py
        self.advantage_info = Advantage()
        self.players = players
        self.match_log = self.start_match_log()
        self.turn = 0

    def start_match_log(self):
        return {player.name: [] for player in self.players}

    def process_turn(self):
        self.turn += 1
        what_changes = self.find_turn_effects()
        for i, player in enumerate(self.players):
            player.apply_changes(self.advantage_info, what_changes[i])
        self.register_in_log()
        return self.flavor_text()

    def register_in_log(self):
        for player in self.players:
            self.match_log[player.name].append("log")

    def flavor_text(self):
        # TODO: text parser module
        return "Flavor text not implemented."

    def find_turn_effects(self):
        ACTIONS_COMBINED = [["09", "09", "02", "03", "04", "03"],
                            ["19", "19", "12", "13", "14", "13"],
                            ["20", "21", "44", "23", "48", "64"],
                            ["30", "31", "32", "33", "74", "48"],
                            ["40", "41", "84", "47", "44", "44"],
                            ["40", "41", "46", "84", "44", "44"]]

        CODE_OF_EFFECTS = {"0": ['ofensiva', 0, None, 0],
                           "1": ['defensiva', 0, None, 0],
                           "2": [None, 1, "slash", -1],
                           "3": [None, 1, "thrust", -1],
                           "4": [None, 0, None, -1],
                           "5": [None, 0, None, -1],
                           "6": [None, 0.5, "slash", -1],
                           "7": [None, 0.5, "thrust", -1],
                           "8": [None, 0, None, 1],
                           "9": [None, 0, None, 0]}

        action1, action2 = (self.players[i].action - 1 for i in range(2))
        pair_of_keys = ACTIONS_COMBINED[action1][action2]
        return [CODE_OF_EFFECTS[pair_of_keys[i]] for i in range(2)]
