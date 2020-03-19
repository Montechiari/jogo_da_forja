from turnmanager import TurnManager
from battle_log import BattleLogger
from numpy import floor, log2


MAX_TURNS = 20
NO_ACTIONS_YET = [0, 0]


class Match:
    def __init__(self, players):
        self.players = players
        self.battle_log = BattleLogger(self.players)
        self.turn_manager = TurnManager(self.battle_log)

    def start(self):
        current_state = self.match_state(NO_ACTIONS_YET)
        self.display_match_start(current_state)

        for i in range(MAX_TURNS):
            number_of_bonus_actions = self.order_players_by_reflex(current_state)
            pairs_of_actions = self.request_actions(number_of_bonus_actions)
            for i, pair in enumerate(pairs_of_actions):
                everybody_is_alive = self.no_player_is_dead()
                if everybody_is_alive:
                    current_state['actions'] = pair
                    is_a_new_turn = True if i == 0 else False
                    current_state = self.turn_manager.process_turn(
                                                        current_state,
                                                        new_turn=is_a_new_turn
                                                                    )
                    self.update_players(current_state)
                    # print(self.battle_log.turn_collection[-1].state_after)
            if not everybody_is_alive:
                break

    def display_match_start(self, state):
        message = ["The match is about to start...\n\n"]
        for player in state['players']:
            name, data = list(player.items())[0]
            message.append(f"{name}: {data['health']}hp | \
{data['reflex']}rx | weapon: {data['weapon']}\n")
        message.append("No one have advantage yet.")
        print("".join(message))

    def order_players_by_reflex(self, state):
        if self.players[0].reflex != self.players[1].reflex:
            self.players.sort(key=lambda player: player.reflex,
                              reverse=True)
        state["players"] = [{player.name: eval(str(player))}
                            for player in self.players]
        # returns how many extra turns there'll be
        return int(floor(abs(log2(self.players[0].reflex /
                                  self.players[1].reflex))))

    def no_player_is_dead(self):
        dead_count = [f"{player.name} is dead."
                      for player in self.players if player.health <= 0]
        self.match_over_message(dead_count)
        return False if len(dead_count) > 0 else True

    def match_over_message(self, dead_count):
        if len(dead_count) > 1:
            message = "Both combatents are dead.\n"
        elif len(dead_count) == 1:
            message = dead_count[0]
        else:
            return
        print("".join(["\n", message, "\nGame over."]))

    def request_actions(self, number_of_bonus_actions):
        def request(player, bonus=False):
            if bonus:
                print(f"{player.name} have superior \
reflexes and can take a bonus action.")
            while True:
                try:
                    action_number = player.take_action()
                    assert (0 < action_number < 7)
                    break
                except (AssertionError, ValueError):
                    print("Action has to be an integer between 1 and 6.")
            return action_number

        actions = [[request(player) for player in self.players]]
        for _ in range(number_of_bonus_actions):
            actions.append([request(self.players[0], bonus=True), 0])
        return actions

    def update_players(self, state):
        for player in self.players:
            for new_attributes in state['players']:
                if player.name in new_attributes:
                    player.update(new_attributes[player.name])

    def match_state(self, actions, state=None):
        player_list = [{player.name: eval(str(player))}
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
