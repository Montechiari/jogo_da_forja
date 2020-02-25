from turnmanager import TurnManager
from battle_log import BattleLogger
from numpy import floor, log2


MAX_TURNS = 20
NO_ACTIONS_YET = [0, 0]


class Match:
    def __init__(self, players):
        self.players = players
        self.battle_log = BattleLogger()
        self.battle_log.set_individual_logs(self.players)
        self.turn_manager = TurnManager(self.battle_log)
        self.match_over = False

    def start(self):
        current_state = self.match_state(NO_ACTIONS_YET)
        for i in range(MAX_TURNS):
            how_many_bonus_actions = self.order_by_reflex(current_state)
            pairs_of_actions = self.request_actions(how_many_bonus_actions)
            for i, pair in enumerate(pairs_of_actions):
                all_alive = self.no_player_is_dead()
                if all_alive:
                    current_state['actions'] = pair
                    is_a_new_turn = True if i == 0 else False
                    current_state = self.turn_manager.process_turn(
                                                        current_state,
                                                        new_turn=is_a_new_turn
                                                                    )
                    self.update_players(current_state)
            if not all_alive:
                break

        # FOR TESTING ONLY
        for turn in self.battle_log.turn_collection:
            print("\n", turn)
        print("\n", self.battle_log.turn_collection[-1].state_after)

    def order_by_reflex(self, state):
        if self.players[0].reflex != self.players[1].reflex:
            self.players.sort(key=lambda player: player.reflex,
                              reverse=True)
        state["players"] = [{player.name: eval(repr(player))}
                            for player in self.players]
        # returns how many extra turns there'll be
        return int(floor(abs(log2(self.players[0].reflex /
                                  self.players[1].reflex))))

    def no_player_is_dead(self):
        dead_count = ['dead' for player in self.players if player.health <= 0]
        return False if 'dead' in dead_count else True

    def request_actions(self, how_many_bonus_actions):
        actions = [[player.take_action() for player in self.players]]
        for i in range(how_many_bonus_actions):
            actions.append([self.players[0].take_action(), 0])
        return actions

    def update_players(self, state):
        for player in self.players:
            for new_attributes in state['players']:
                if player.name in new_attributes:
                    player.update(new_attributes[player.name])

    def match_state(self, actions, state=None):
        player_list = [{player.name: eval(repr(player))}
                       for player in self.players]
        if not state:
            advantage = {"who": None,
                         "kind": None}
            return {"turn": 0, "players": player_list,
                    "advantage": advantage, "actions": actions}
        else:
            state['players'] = player_list
            state["actions"] = actions
            return state
