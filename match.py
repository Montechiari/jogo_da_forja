from turnmanager import TurnManager, DeadPlayerException
from battle_log import BattleLogger
from numpy import floor, log2


MAX_TURNS = 20
NO_ACTIONS_YET = [0, 0]


class Match:
    def __init__(self, players):
        self.players = players
        self.battle_log = BattleLogger(self.players)
        self.turns = TurnManager(self.battle_log)

    def start(self):
        for i in range(MAX_TURNS):
            try:
                current_state = self.turns.new_turn(self.players)

                self.print_current_state(current_state)

                actions = self.request_actions(current_state)
                effects_message = self.turns.next_state(actions)
                print('actions: ', actions)

                self.print_turn_effects(effects_message)
                print('\n')
                self.update_players(effects_message)
            except DeadPlayerException as person:
                print(f'\n{person} dies.\n\n-- Game Over --\n')
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

    def request_actions(self, state):
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

        number_of_bonus_actions = state['bonus actions']
        actions = [[request(player) for player in self.players]]
        for _ in range(number_of_bonus_actions):
            actions.append([request(self.players[0], bonus=True), 0])
        return actions

    def update_players(self, state):
        for i, player in enumerate(self.players):
            attributes = state['players'][i]
            player.health = attributes['health']
            player.reflex = attributes['reflex']

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

    def print_current_state(self, state):
        print(state)

    def print_turn_effects(self, state):
        print(state)
