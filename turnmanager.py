from copy import deepcopy
from numpy import floor, log2


class DeadPlayerException(Exception):
    ''' Raised when a player dies. '''
    def __init___(self, who_died):
        super(DeadPlayerException, self).__init__(f'{who_died} dies.')


class Advantage:
    def __init__(self, who=None, kind=None):
        self.who = who
        self.kind = kind

    def __str__(self):
        if self.who:
            return f"{self.who.name} has {self.kind} advantage."
        else:
            return "No one has advantage."

    def __repr__(self):
        return "{'who': %s, 'kind': %s}" % (self.who, self.kind)


class Turn:
    def __init__(self, turn_number, players, advantage):
        self.turn_number = turn_number
        self.advantage = advantage
        self.players = players
        self.extra_actions = self.order_players_by_reflex()
        self.state_before = self.write_state_before()
        self.state_after = deepcopy(self.state_before)

    def __repr__(self):
        ACTION_NAMES = ['no action',
                        'offensive movement', 'defensive movement',
                        'slash attack', 'thrust attack',
                        'slash defense', 'thrust defense']

        report = ["Turn: %d" % self.state_before['turn']]
        actions = self.state_before['actions']
        actions_line = []
        punctuation = [", ", "."]
        for i, player in enumerate(self.state_before['players']):
            name = list(player.keys())[0]
            action = ACTION_NAMES[actions[i]]
            actions_line.append(f"{name} performs {action}")
            actions_line.append(punctuation[i])
        actions_line = "".join(actions_line)
        report.extend([str(player) for player in self.state_before['players']])
        advantage = self.state_before['advantage']
        report.extend([f"{advantage['who']} has " +
                       f"{advantage['kind']} advantage."])
        report.extend([actions_line])
        return "\n".join(report)

    def order_players_by_reflex(self):
        if self.players[0].reflex != self.players[1].reflex:
            self.players.sort(key=lambda player: player.reflex,
                              reverse=True)
        # returns how many extra turns there'll be
        return int(floor(abs(log2(self.players[0].reflex /
                                  self.players[1].reflex))))

    def write_state_before(self):
        state = {'turn': self.turn_number,
                 'players': [eval(str(player)) for player in self.players],
                 'advantage': eval(repr(self.advantage)),
                 'bonus actions': self.extra_actions}
        return state

    def calculate_next_state(self, actions):
        state_placeholder = deepcopy(self.state_before)
        for action in actions:
            what_changes = self.find_turn_effects(action)
            self.make_changes(state_placeholder, what_changes)
            dead_player, first_blood = self.someone_dead(state_placeholder)
            if dead_player:
                raise DeadPlayerException(first_blood)
        state_placeholder['turn'] += 1
        self.state_after = state_placeholder
        return self.state_after

    def make_changes(self, placeholder, what_changes):
        for i, player in enumerate(placeholder['players']):
            self.update_advantage(placeholder, player, what_changes[i][0])
            damage = self.calculate_damage(placeholder, player,
                                           what_changes[i][1:3])
            self.inflict_damage(placeholder['players'][i - 1], damage)
            self.deduce_reflex(player, what_changes[i][3])

    def update_advantage(self, placeholder, player, adv_instruction):
        if adv_instruction:
            placeholder["advantage"] = {"who": player['name'],
                                        "kind": adv_instruction}

    def calculate_damage(self, placeholder, player, dmg_instruction):
        advantage = {"offensive": 2,
                     "defensive": 0.5,
                     None: 1}
        modifyer = dmg_instruction[0]
        if modifyer:
            dmg = player['weapon'][dmg_instruction[1]]
            if self.has_advantage(player['name']):
                modifyer *= advantage[placeholder['advantage']['kind']]
            return modifyer * dmg
        else:
            return 0

    def inflict_damage(self, player, damage):
        new_health = player['health'] - damage
        player['health'] = new_health if new_health > 0 else 0

    def deduce_reflex(self, player, how_much):
        new_reflex = player['reflex'] + how_much
        player['reflex'] = new_reflex if new_reflex > 0 else 1
        return new_reflex

    def someone_dead(self, state):
        for player in state['players']:
            if player['health'] == 0:
                return True, player['name']
        return False, None

    def has_advantage(self, name):
        return self.state_after['advantage']['who'] == name

    def find_turn_effects(self, actions):
        ACTIONS_COMBINED = [["09", "09", "02", "03", "04", "04"],
                            ["19", "19", "12", "13", "14", "14"],
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
        self.turn_collection = []
        self.advantage = Advantage()
        self.match_log = match_log

    def new_turn(self, players):
        new_turn = Turn(len(self.turn_collection), players, self.advantage)
        self.turn_collection.append(new_turn)
        return new_turn.state_before

    def next_state(self, actions):
        return self.current_turn().calculate_next_state(actions)

    def current_turn(self):
        return self.turn_collection[-1]

    def process_turn(self, world_state, new_turn):
        world_state = deepcopy(world_state)
        # print(world_state)
        if new_turn:
            world_state['turn'] += 1
        this_turn = Turn(world_state)
        world_state = this_turn.calculate_next_state()
        # print(world_state)
        self.match_log.add_turn(this_turn)
        return world_state

    def register_in_log(self):
        for player in self.players:
            self.match_log[player.name].append("log")

    def flavor_text(self):
        # TODO: text parser module
        return "Flavor text not implemented."
