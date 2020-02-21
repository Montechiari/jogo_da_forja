from turnmanager import TurnManager
from battle_log import BattleLogger
from numpy import floor, log2


MAX_TURNS = 20


class Advantage:
    def __init__(self, who=None, kind=None):
        self.who = who
        self.kind = kind

    def __repr__(self):
        if self.who:
            return f"{self.who.name} has {self.kind} advantage."
        else:
            return "No one has advantage."


class Match:
    def __init__(self, players):
        self.players = players
        self.advantage = Advantage()
        self.log = BattleLogger()
        self.turn_manager = TurnManager(self.log)
        self.match_over = False

    def start(self):
        while (self.turn_manager.turn < MAX_TURNS and
               self.no_player_is_dead()):
            bonus_action = self.resolve_initiative()
            moves = self.request_actions(bonus_action)
            print(self.turn_manager.process_turn(self.match_state(moves)))

    def resolve_initiative(self):
        if self.players[0].reflex != self.players[1].reflex:
            self.players.sort(key=lambda player: player.reflex,
                              reverse=True)
        assert self.players[0].reflex != 0, "Reflex can't be zero!"
        # returns how many extra turns there'll be
        return int(floor(abs(log2(self.players[0].reflex /
                                  self.players[1].reflex))))

    def no_player_is_dead(self):
        dead_count = ['dead' for player in self.players if player.health <= 0]
        return False if 'dead' in dead_count else True

    def request_actions(self, bonus_action):
        actions = [player.take_action() for player in self.players]
        for i in range(bonus_action):
            actions.append(self.players[0].take_action)
            actions.append(0)
        return actions

    def match_state(self, moves):
        player_list = [eval(repr(player)) for player in self.players]
        advantage = {"who": self.advantage.who, "kind": self.advantage.kind}
        return {"players": player_list, "advantage": advantage, "moves": moves}
