from turnmanager import TurnManager
from battle_log import BattleLogger
from numpy import floor, log2


MAX_TURNS = 20


class Match:
    def __init__(self, players):
        self.players = players
        self.log = BattleLogger()
        self.turn_manager = TurnManager(self.log)
        self.match_over = False

    def start(self):
        current_state = None
        for i in range(MAX_TURNS):
            if self.no_player_is_dead():
                bonus_actions = self.resolve_initiative()
                moves = self.request_actions(bonus_actions)
                current_state = self.turn_manager.process_turn(
                                self.match_state(moves, current_state)
                                                          )
                self.update_players(current_state)
                print(current_state)
            else:
                break

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

    def request_actions(self, bonus_actions):
        actions = [player.take_action() for player in self.players]
        for i in range(bonus_actions):
            actions.append(self.players[0].take_action)
            actions.append(0)
        return actions

    def update_players(self, state):
        for player in self.players:
            for new_attributes in state['players']:
                if player.name in new_attributes:
                    player.update(new_attributes[player.name])

    def match_state(self, moves, state=None):
        player_list = [{player.name: eval(repr(player))}
                       for player in self.players]
        if not state:
            advantage = {"who": None,
                         "kind": None}
            return {"turn": 0, "players": player_list,
                    "advantage": advantage, "moves": moves}
        else:
            state['players'] = player_list
            state["moves"] = moves
            return state
