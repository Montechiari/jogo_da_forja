class BattleLogger:

    MOVE_TEXT = ['offensive movement', 'defensive movement',
                 'slash attack', 'thrust attack',
                 'slash defense', 'thrust defense']

    def __init__(self):
        self.turn_collection = []

    def add_turn(self, turn):
        self.turn_collection.append(turn)

    def dump_turns(self):
        for turn in self.turn_collection:
            print(repr(turn))

    def set_individual_logs(self, players):
        self.individual_logs = {player.name: [] for player in players}
        for i in range(-1, 1):
            self.individual_logs[players[i].name].extend([
                    players[i].weapon.slash / players[i].weapon.thrust,
                    players[i].weapon.slash / players[i + 1].weapon.slash,
                    players[i].weapon.thrust / players[i + 1].weapon.thrust,
                    players[i].health / players[i].reflex,
                    players[i].health / players[i + 1].health,
                    players[i].reflex / players[i + 1].reflex,
            ])
