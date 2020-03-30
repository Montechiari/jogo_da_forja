from combatents import DummyPlayer, HumanPlayer, AiPlayer
from match import Match
import argparse


NAMES_FOR_TESTING = ["Carlos", "Emar"]


def instantiate_players(mode):
    full_mode_name = {'dd': 'two dummies',
                      'hd': 'human vs dummy',
                      'ai': 'ai vs dummy'}
    print("Game mode:", full_mode_name[mode], '\n')
    instructions_for_creation = {'dd': [DummyPlayer(name)
                                        for name in NAMES_FOR_TESTING],
                                 'hd': [combatent(NAMES_FOR_TESTING[i])
                                        for i, combatent in enumerate(
                                    [HumanPlayer, DummyPlayer])
                                        ],
                                 'ai': [AiPlayer(NAMES_FOR_TESTING[0]),
                                        AiPlayer(NAMES_FOR_TESTING[1])]}

    pair_of_players = instructions_for_creation[mode]
    relate_opponents(pair_of_players)
    return pair_of_players


def relate_opponents(players):
    for i in range(-1, len(players) - 1):
        players[i].opponent = players[i + 1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('game_mode', type=str)
    args = parser.parse_args()

    players = instantiate_players(args.game_mode)
    match = Match(players)
    match.start(verbose=True)
