from numpy import round


class BattleLogger:
    def __init__(self):
        self.turn_collection = []

    def add_turn(self, turn):
        self.turn_collection.append(turn)

    def dump_turns(self):
        for turn in self.turn_collection:
            print(repr(turn))

    def set_individual_logs(self, players):
        self.static_logs = {player.name: [] for player in players}
        for i in range(-1, 1):
            self.static_logs[players[i].name].extend([
                    players[i].health,
                    players[i].reflex,
                    players[i + 1].health,
                    players[i + 1].reflex,
                    players[i].weapon.slash / players[i].weapon.thrust,
                    players[i].weapon.slash / players[i + 1].weapon.slash,
                    players[i].weapon.thrust / players[i + 1].weapon.thrust,
                    players[i].health / players[i].reflex,
                    players[i].health / players[i + 1].health,
                    players[i].reflex / players[i + 1].reflex,
            ])

    def make_turn_vector(self, turn, player_name):
        vector = self.static_logs[player_name][4:]
        vector.extend([0, 0, 0, 0, 0, 0, 0, 0])
        turn_info = turn.state_before
        for i, player in enumerate(turn_info['players']):
            iterated_name = list(player.items())[0][0]
            iterated_dict = player[iterated_name]
            if iterated_name == player_name:
                starting_health, starting_reflex = tuple(
                            self.static_logs[player_name][:2])
                vector[6] = (iterated_dict['health'] / starting_health)
                vector[7] = (iterated_dict['reflex'] / starting_reflex)
                vector[12] = turn_info['actions'][0]
                vector[13] = turn_info['actions'][1]
                if i != 0:
                    vector[12], vector[13] = vector[13], vector[12]
            else:
                starting_health, starting_reflex = tuple(
                            self.static_logs[player_name][2:4])
                vector[8] = (iterated_dict['health'] / starting_health)
                vector[9] = (iterated_dict['reflex'] / starting_reflex)
        vector[10] = 1 if turn_info['advantage']['who'] == player_name else 0
        kind = turn_info['advantage']['kind']
        vector[11] = {'offensive': 1, 'defensive': 0, None: 0.5}[kind]

        return [round(value, 3) for value in vector]
