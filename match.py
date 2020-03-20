from turnmanager import TurnManager, DeadPlayerException


MAX_TURNS = 20
NO_ACTIONS_YET = [0, 0]


class Match:
    def __init__(self, players):
        self.players = players
        self.turns = TurnManager()

    def start(self, verbose=False):
        for i in range(MAX_TURNS):
            try:
                current_state = self.turns.new_turn(self.players)
                self.display_message(verbose, current_state, 'pre_action')
                actions = self.request_actions(current_state)
                self.action_message(actions, current_state)
                new_state = self.turns.next_state(actions)
                self.update_players(new_state)

            except DeadPlayerException as person:
                print(f'{person} dies.\n\n-- Game Over --\n')
                break

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

    def display_message(self, verbose, state, kind):
        if verbose:
            message_callbacks = {
                                 'pre_action': self.pre_action_message,
                                 'action': self.action_message,
                                 'post_action': self.post_action_message
                                 }
            print(message_callbacks[kind](state))

    def pre_action_message(self, state):
        message = ['-- Turn {} --'.format(state['turn'])]
        message.extend(["{name1}, w({slash1}sl/{thrust1}th):\
 {hp1}hp, {rx1}rx.".format(
            name1=player['name'],
            slash1=player['weapon']['slash'],
            thrust1=player['weapon']['thrust'],
            hp1=player['health'], rx1=player['reflex'])
                  for player in state['players']])
        message.append('{}\n'.format(self.advantage_message(state)))
        return '\n'.join(message)

    def advantage_message(self, state):
        advantage = state['advantage']
        if advantage['who']:
            return f"{advantage['who']} has {advantage['kind']} advantage."
        else:
            return "No one has advantage."

    def action_message(self, actions, state):
        ACTION_NAMES = ['no action',
                        'offensive movement', 'defensive movement',
                        'slash attack', 'thrust attack',
                        'slash defense', 'thrust defense']
        for pair in actions:
            for i, action in enumerate(pair):
                print(f"{state['players'][i]['name']} performs",
                      ACTION_NAMES[action])
            print('\n')

    def post_action_message(self, state):
        pass
