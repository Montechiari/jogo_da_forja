from turnmanager import TurnManager
from combatents import DummyPlayer


class Match:
    def __init__(self):
        self.players = self.create_combatents()
        self.introduce_opponents(self.players)
        self.turn_manager = TurnManager(self.players)

    def start(self):
        game_over = False
        while (self.turn_manager.turn < 20 and game_over is False):
            self.resolve_initiative()
            moves = []
            for player in self.players:
                player.take_action()
                moves.append(player.action)
            print(f"\nTurn {self.turn_manager.turn + 1} - {moves} -",
                  self.turn_manager.advantage_info, "\n")
            game_over = self.turn_manager.process_turn()

    def create_combatents(self):
        raise AttributeError

    def resolve_initiative(self):
        pass

    def introduce_opponents(self, players):
        for i in range(-1, len(players) - 1):
            players[i].opponent = players[i + 1]


class MatchAutomatic(Match):
    def __init__(self):
        Match.__init__(self)

    def create_combatents(self):
        return [DummyPlayer("Carlos"), DummyPlayer("Erasmo")]


if __name__ == '__main__':
    match = MatchAutomatic()
    match.start()
