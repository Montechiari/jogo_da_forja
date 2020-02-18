from turnmanager import TurnManager
from combatents import DummyPlayer


class Match:
    def __init__(self):
        self.players = self.create_combatents()
        self.turn_manager = TurnManager(self.players)

    def start(self):
        while self.turn_manager.turn < 20:
            self.resolve_initiative()
            for player in self.players:
                player.take_action()
            self.turn_manager.process_turn()

    def create_combatents(self):
        raise AttributeError

    def resolve_initiative(self):
        pass


class MatchAutomatic(Match):
    def __init__(self):
        Match.__init__(self)

    def create_combatents(self):
        return [DummyPlayer("Carlos"), DummyPlayer("Erasmo")]


if __name__ == '__main__':
    match = MatchAutomatic()
    match.start()
