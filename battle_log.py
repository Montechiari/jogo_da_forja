from numpy import round


class BattleLogger:
    def __init__(self, players):
        self.players = players
        self.set_individual_logs()
        self.turn_collection = []

    def add_turn(self, turn):
        self.turn_collection.append(turn)

    def dump_turns(self):
        for turn in self.turn_collection:
            print(repr(turn))

    def set_individual_logs(self):
        self.permanent_info = {player.name: [] for player in self.players}
        for i in range(-1, 1):
            self.permanent_info[self.players[i].name].extend([
                    self.players[i].health,
                    self.players[i].reflex,
                    self.players[i + 1].health,
                    self.players[i + 1].reflex,
                    self.players[i].weapon.slash / self.players[i].weapon.thrust,
                    self.players[i].weapon.slash / self.players[i + 1].weapon.slash,
                    self.players[i].weapon.thrust / self.players[i + 1].weapon.thrust,
                    self.players[i].health / self.players[i].reflex,
                    self.players[i].health / self.players[i + 1].health,
                    self.players[i].reflex / self.players[i + 1].reflex,
            ])

    def make_turn_vector(self, turn, player_name):
        vector = self.permanent_info[player_name][4:]
        vector.extend([0, 0, 0, 0, 0, 0, 0, 0])
        turn_info = turn.state_before
        for i, player in enumerate(turn_info['players']):
            iterated_name = list(player.items())[0][0]
            iterated_dict = player[iterated_name]
            if iterated_name == player_name:
                starting_health, starting_reflex = tuple(
                            self.permanent_info[player_name][:2])
                vector[6] = (iterated_dict['health'] / starting_health)
                vector[7] = (iterated_dict['reflex'] / starting_reflex)
                vector[12] = turn_info['actions'][0]
                vector[13] = turn_info['actions'][1]
                if i != 0:
                    vector[12], vector[13] = vector[13], vector[12]
            else:
                starting_health, starting_reflex = tuple(
                            self.permanent_info[player_name][2:4])
                vector[8] = (iterated_dict['health'] / starting_health)
                vector[9] = (iterated_dict['reflex'] / starting_reflex)
        vector[10] = 1 if turn_info['advantage']['who'] == player_name else 0
        kind = turn_info['advantage']['kind']
        vector[11] = {'offensive': 1, 'defensive': 0, None: 0.5}[kind]

        return [round(value, 3) for value in vector]
