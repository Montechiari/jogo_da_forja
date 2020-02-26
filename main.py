from combatents import DummyPlayer, HumanPlayer
from match import Match
import argparse


NAMES_FOR_TESTING = ["Carlos", "Emar"]


def create_players(mode):
    print("Game mode:", mode)
    creating_methods = {'dd': [DummyPlayer(name)
                               for name in NAMES_FOR_TESTING],
                        'hd': [combatent(NAMES_FOR_TESTING[i])
                               for i, combatent in enumerate(
                                    [HumanPlayer, DummyPlayer])]}

    pair_of_players = creating_methods[mode]
    introduce_opponents(pair_of_players)
    return pair_of_players


def introduce_opponents(players):
    for i in range(-1, len(players) - 1):
        players[i].opponent = players[i + 1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('game_mode', type=str)
    args = parser.parse_args()
    players = create_players(args.game_mode)
    match = Match(players)
    match.start()
