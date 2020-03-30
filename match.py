from turnmanager import TurnManager, DeadPlayerException
from combatents import AiPlayer


MAX_TURNS = 20


class Match:
    def __init__(self, players):
        self.players = players
        self.relate_opponents(self.players)
        self.turns = TurnManager()
        self.winner = None

    def start(self, verbose=False):
        for i in range(MAX_TURNS):
            try:
                current_state = self.turns.new_turn(self.players)
                self.display_message(verbose, current_state, 'pre_action')
                actions = self.request_actions(current_state, verbose)
                if verbose:
                    self.action_message(actions, current_state)
                new_state = self.turns.next_state(actions)
                self.update_players(new_state)

            except DeadPlayerException as person:
                final_state = self.turns.current_turn().state_after
                self.display_message(verbose, final_state, 'pre_action')
                # print(f'{person} died.')
                self.winner = self.get_opponent_of(person)
                # print(self.winner,
                #       "wins!\n\n-- Game Over --")
                break
        self.end_by_turn_limit()
        # for player in self.players:
        #     if player.name == self.winner:
        #         for line in self.turns.dump_like_vector(player):
        #             print(line)

    def request_actions(self, state, verbose):
        def request(player, bonus=False):
            if bonus and verbose:
                print(f"{player.name} have superior \
reflexes and can take a bonus action.")
            while True:
                try:
                    if isinstance(player, AiPlayer):
                        action_number = player.take_action(
                                            self.turn_vector(player)
                                                            )
                    else:
                        action_number = player.take_action()
                    assert (0 < action_number < 7)
                    break
                except (AssertionError, ValueError) as e:
                    print("Action has to be an integer between 1 and 6.")
                    print(e)
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

    def get_opponent_of(self, player_name):
        try:
            for i, player in enumerate(self.players):
                if player.name is str(player_name):
                    return player.opponent.name
        except (AttributeError, TypeError):
            raise AssertionError('Input variables should be strings')

    def relate_opponents(self, players):
        for i in range(-1, len(players) - 1):
            players[i].opponent = players[i + 1]

    def get_winner(self):
        for player in self.players:
            if player.name == self.winner:
                return player
        print('NO WINNER', len(self.turns.turn_collection))
        raise AssertionError

    def end_by_turn_limit(self):
        sorted_players = sorted(self.players,
                                key=lambda player: player.health,
                                reverse=True)
        self.winner = sorted_players[0].name

    def turn_vector(self, player):
        big_log = self.turns.dump_like_vector(player)
        vectors, action = zip(*big_log)
        return vectors[-1]
