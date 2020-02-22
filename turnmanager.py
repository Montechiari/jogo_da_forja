class Advantage:
    def __init__(self, who=None, kind=None):
        self.who = who
        self.kind = kind

    def __repr__(self):
        if self.who:
            return f"{self.who.name} has {self.kind} advantage."
        else:
            return "No one has advantage."


class Turn:
    def __init__(self, state_before):
        self.state_before = state_before

    def next_state(self):
        self.state_before["turn"] += 1
        return self.state_before

    def find_turn_effects(self, actions):
        ACTIONS_COMBINED = [["09", "09", "02", "03", "04", "03"],
                            ["19", "19", "12", "13", "14", "13"],
                            ["20", "21", "44", "23", "48", "64"],
                            ["30", "31", "32", "33", "74", "48"],
                            ["40", "41", "84", "47", "44", "44"],
                            ["40", "41", "46", "84", "44", "44"]]

        CODE_OF_EFFECTS = {"0": ['offensive', 0, None, 0],
                           "1": ['defensive', 0, None, 0],
                           "2": [None, 1, "slash", -1],
                           "3": [None, 1, "thrust", -1],
                           "4": [None, 0, None, -1],
                           "5": [None, 0, None, -1],
                           "6": [None, 0.5, "slash", -1],
                           "7": [None, 0.5, "thrust", -1],
                           "8": [None, 0, None, 1],
                           "9": [None, 0, None, 0]}
        action1, action2 = (action - 1 for action in actions)
        pair_of_keys = ACTIONS_COMBINED[action1][action2]
        return [CODE_OF_EFFECTS[pair_of_keys[i]] for i in range(2)]


class TurnManager:
    def __init__(self, match_log):
        # players is a pair of Combatent instances, found in combatents.py
        self.advantage = Advantage()
        self.match_log = match_log

    def start_match_log(self):
        return {player.name: [] for player in self.players}

    def process_turn(self, prior_state):
        this_turn = Turn(prior_state)
        self.match_log.add_turn(this_turn)
        return this_turn.next_state()
        # player.apply_changes(self.advantage_info, what_changes[i])

    def register_in_log(self):
        for player in self.players:
            self.match_log[player.name].append("log")

    def flavor_text(self):
        # TODO: text parser module
        return "Flavor text not implemented."
