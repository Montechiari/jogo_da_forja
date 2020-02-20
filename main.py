from combatents import DummyPlayer
from match import Match


NAMES_FOR_TESTING = ["Carlos", "Emar"]


def create_players():
    pair_of_players = [DummyPlayer(name) for name in NAMES_FOR_TESTING]
    introduce_opponents(pair_of_players)
    return pair_of_players


def introduce_opponents(players):
    for i in range(-1, len(players) - 1):
        players[i].opponent = players[i + 1]


if __name__ == '__main__':
    players = create_players()
    match = Match(players)
    match.start()
