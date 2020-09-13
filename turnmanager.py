from copy import deepcopy
from numpy import floor, log2


class DeadPlayerException(Exception):
    ''' Raised when a player dies. '''
    def __init___(self, who_died):
        super(DeadPlayerException, self).__init__(f'{who_died} dies.')


class TurnVector:
    def __init__(self, player, manager):
        self.player = player
        self.manager = manager
        self.starting_state = self.manager.starting_turn().state_before
        # for line in self.match_vectors():
        #     print(line)

    def match_vectors(self):
        previous_action = [0, 0]
        out = []
        permanent_info = self.get_permanent_info()
        for turn in self.manager.turn_collection:
            entire_turn = deepcopy(permanent_info[6:])
            turn_info = self.get_current_info(permanent_info, turn.turn_number)
            turn_info.append(turn.state_before['bonus actions'])
            entire_turn.extend(turn_info)
            for i, action_pair in enumerate(turn.actions):
                turn_with_action = deepcopy(entire_turn)
                turn_with_action.append(i)
                turn_with_action.extend([action / 6
                                         for action in previous_action])
                previous_action = [action_pair[permanent_info[0]],
                                   action_pair[permanent_info[1]]]
                out.append((turn_with_action,
                            self.spit_one_off(7, previous_action[0])))

        return out
    #
    # def assemble_vector(self, turn):
    #     previous_action = [0, 0]
    #     permanent_info = self.get_permanent_info()
    #     entire_turn = deepcopy(permanent_info[6:])
    #     turn_info = self.get_current_info(permanent_info, turn.turn_number)
    #     turn_info.append(turn.state_before['bonus actions'])
    #     entire_turn.extend(turn_info)
    #     for i, action_pair in enumerate(turn.actions):
    #         turn_with_action = deepcopy(entire_turn)
    #         turn_with_action.append(i)
    #         turn_with_action.extend([action / 6
    #                                  for action in previous_action])
    #         previous_action = [action_pair[permanent_info[0]],
    #                            action_pair[permanent_info[1]]]
    #         out.append((turn_with_action,
    #                     self.spit_one_off(7, previous_action[0])))

    def get_permanent_info(self):
        players_state = self.starting_state['players']
        my_index = self.find_self_idx(players_state)
        opn_index = (my_index + 1) % 2
        fields = {'my index': my_index, 'opponents index': opn_index,
                  'my starting health': players_state[my_index]['health'],
                  'my starting reflex': players_state[my_index]['reflex'],
                  'opn starting_health': players_state[opn_index]['health'],
                  'opn starting reflex': players_state[opn_index]['reflex'],
                  'health vs reflex': (players_state[my_index]['health'] /
                                       players_state[my_index]['reflex']),
                  'my health vs opn': (players_state[my_index]['health'] /
                                       players_state[opn_index]['health']),
                  'my reflex vs opn': (players_state[my_index]['reflex'] /
                                       players_state[opn_index]['reflex']),
                  'weapon ratio': (players_state[my_index]['weapon']['slash'] /
                                   players_state[my_index]['weapon']['thrust']
                                   ),
                  'slash vs': (players_state[my_index]['weapon']['slash'] /
                               players_state[opn_index]['weapon']['slash']),
                  'thrust vs': (players_state[my_index]['weapon']['thrust'] /
                                players_state[opn_index]['weapon']['thrust'])
                  }
        _, out = zip(*[item for item in fields.items()])
        return list(out)

    def get_current_info(self, perm_info, turn_number):
        turn_state = self.manager.turn_collection[turn_number].state_before
        perm_info[0] = self.find_self_idx(turn_state['players'])
        perm_info[1] = (perm_info[0] + 1) % 2
        adv_vect = self.get_advantage_vector(turn_state)
        info = {'turn number': turn_number / 20,
                'my hp pct': (turn_state['players'][perm_info[0]]['health'] /
                              perm_info[2]),
                'my rp pct': (turn_state['players'][perm_info[0]]['reflex'] /
                              perm_info[3]),
                'opn hp pct': (turn_state['players'][perm_info[1]]['health'] /
                               perm_info[4]),
                'opn rp pct': (turn_state['players'][perm_info[1]]['reflex'] /
                               perm_info[5]),
                'advantage who': adv_vect[0],
                'advantage kind': adv_vect[1]}
        _, out = zip(*[item for item in info.items()])
        return list(out)

    def get_advantage_vector(self, state):
        players = state['players']
        my_idx = self.find_self_idx(players)
        names = [players[my_idx]['name'],
                 players[(my_idx + 1) % 2]['name'],
                 None]
        who_values = [1, 0, 0.5]
        who_bit = {names[i]: who_values[i] for i in range(len(names))}
        kind_bit = {'offensive': 1, 'defensive': 0, None: 0.5}
        adv = state['advantage']
        return [who_bit[adv['who']], kind_bit[adv['kind']]]

    def get_action_vector(self, prefix, state, actions):
        pass

    def find_self_idx(self, player_dicts):
        if player_dicts[0]['name'] == self.player.name:
            return 0
        else:
            return 1

    def spit_one_off(self, size, number):
        out_array = [0 for _ in range(size)]
        out_array[number] = 1
        return out_array


class TurnManager:
    def __init__(self):
        self.turn_collection = []
        self.advantage = {'who': None, 'kind': None}

    def new_turn(self, players):
        new_turn = Turn(len(self.turn_collection), players, self.advantage)
        self.turn_collection.append(new_turn)
        return new_turn.state_before

    def next_state(self, actions):
        this_turn = self.current_turn()
        next_state = this_turn.calculate_next_state(actions)
        self.advantage = next_state['advantage']
        return next_state

    def current_turn(self):
        return self.turn_collection[-1]

    def starting_turn(self):
        return self.turn_collection[0]

    def dump_like_vector(self, player):
        turnvect = TurnVector(player, self)
        return turnvect.match_vectors()

    def get_current_vector(self):
        pass


class Turn:
    def __init__(self, turn_number, players, advantage):
        self.turn_number = turn_number
        self.players = players
        self.advantage = advantage
        self.extra_actions = self.order_players_by_reflex()
        self.state_before = self.write_state_before()
        self.state_after = deepcopy(self.state_before)
        self.actions = [[0, 0]]

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
                 'advantage': self.advantage,
                 'bonus actions': self.extra_actions}
        return state

    def calculate_next_state(self, actions):
        self.actions = actions
        state_placeholder = deepcopy(self.state_before)
        for action in actions:
            what_changes = self.find_turn_effects(action)
            self.make_changes(state_placeholder, what_changes)
            dead_player, first_blood = self.someone_dead(state_placeholder)
            if dead_player:
                self.state_after = state_placeholder
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
            if dmg_instruction[1] is None:
                dmg = 4
            else:
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
                           "8": [None, 1, None, 1],
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
