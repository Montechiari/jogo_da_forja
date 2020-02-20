from turnmanager import TurnManager, Turn
from battle_log import BattleLogger
from numpy import floor, log2


class Match:
    def __init__(self, players):
        self.players = players
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

    def resolve_initiative(self):
        if self.players[0].reflex != self.players[1].reflex:
            self.players.sort(key=lambda player: player.reflex,
                              reverse=True)
        assert self.players[0].reflex != 0, "Reflex can't be zero!"
        # returns how many extra turns there'll be
        return floor(abs(log2(self.players[0].reflex /
                              self.players[1].reflex)))
