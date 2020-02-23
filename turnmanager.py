from copy import deepcopy


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
        self.state_after = deepcopy(state_before)

    def __repr__(self):
        MOVE_TEXT = ['offensive movement', 'defensive movement',
                     'slash attack', 'thrust attack',
                     'slash defense', 'thrust defense']

        report = ["Turn: %d" % self.state_before['turn']]
        report.extend([str(self.state_before['advantage'])])
        moves = self.state_before['moves']
        report.extend([f"{MOVE_TEXT[moves[0] - 1]} {MOVE_TEXT[moves[1] - 1]}"])
        report.extend([str(player) for player in self.state_before['players']])
        return "\n".join(report)
        return str(self.state_before) + "\n"

    def next_state(self):
        what_changes = self.find_turn_effects(
                            self.state_before["moves"]
                                              )
        self.make_changes(what_changes)
        return self.state_after

    def make_changes(self, what_changes):
        for i in range(-1, 1):
            player = self.state_after['players'][i]
            name, attributes = list(player.items())[0]

            self.update_advantage(name, what_changes[i][0])
            damage = self.calculate_damage(name, attributes,
                                           what_changes[i][1:3])
            self.inflict_damage(self.state_after['players'][i + 1], damage)
            self.deduce_reflex(name, player, what_changes[i][3])

    def update_advantage(self, name, adv_instruction):
        if adv_instruction:
            self.state_after["advantage"] = {"who": name,
                                             "kind": adv_instruction}

    def calculate_damage(self, name, attributes, dmg_instruction):
        advantage = {"offensive": 2,
                     "defensive": 0.5,
                     None: 1}
        modifyer = dmg_instruction[0]
        if modifyer:
            dmg = attributes['weapon'][dmg_instruction[1]]
            if self.has_advantage(name):
                modifyer *= advantage[self.state_after['advantage']['kind']]
            return modifyer * dmg
        else:
            return 0

    def inflict_damage(self, player, damage):
        name, _ = list(player.items())[0]
        new_health = player[name]['health'] - damage
        player[name]['health'] = new_health if new_health > 0 else 0

    def deduce_reflex(self, name, player, how_much):
        advantage = {"offensive": 0,
                     "defensive": 1,
                     None: 0}

        if self.has_advantage(name):
            how_much += advantage[self.state_after['advantage']['kind']]
        new_reflex = player[name]['reflex'] + how_much
        player[name]['reflex'] = new_reflex if new_reflex > 0 else 1
        return new_reflex

    def has_advantage(self, name):
        return self.state_after['advantage']['who'] == name

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
        try:
            action1, action2 = (action - 1 for action in actions)
            if action2 >= 0:
                pair_of_keys = ACTIONS_COMBINED[action1][action2]
                return [CODE_OF_EFFECTS[pair_of_keys[i]] for i in range(2)]
            else:
                return [CODE_OF_EFFECTS[str(action1)], [None, 0, None, 0]]
        except TypeError:
            print(actions)


class TurnManager:
    def __init__(self, match_log):
        # players is a pair of Combatent instances, found in combatents.py
        self.advantage = Advantage()
        self.match_log = match_log

    def start_match_log(self):
        return {player.name: [] for player in self.players}

    def process_turn(self, prior_state):
        prior_state = deepcopy(prior_state)
        prior_state['turn'] += 1
        move_packages = self.split_bonus_actions(prior_state['moves'])
        for package in move_packages:
            prior_state['moves'] = package
            this_turn = Turn(prior_state)
            self.match_log.add_turn(this_turn)
            prior_state = this_turn.next_state()
        return prior_state

    def split_bonus_actions(self, moves):
        return [moves[i:i + 2] for i in range(0, len(moves), 2)]

    def register_in_log(self):
        for player in self.players:
            self.match_log[player.name].append("log")

    def flavor_text(self):
        # TODO: text parser module
        return "Flavor text not implemented."
