from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, LSTM
from combatents import DummyPlayer
from match import Match
import numpy as np
import threading

NAMES = ['Carlos', 'Emar']


class MatchThread(threading.Thread):
    def __init__(self, match):
        threading.Thread.__init__(self)
        self.match = match

    def run(self):
        self.match.start()


def bunch_of_matches(number_of_matches):
    matches = [Match([DummyPlayer(name) for name in NAMES])
               for i in range(number_of_matches)]
    match_threads = []
    for match in matches:
        this_thread = MatchThread(match)
        match_threads.append(this_thread)
        this_thread.start()
    for thread in match_threads:
        thread.join()
    return [np.array(match.turns.dump_like_vector(match.get_winner()))
            for match in matches]


def get_model():
    try:
        # open model
        pass
    except Exception:
        return Sequential([
                        Dense(51, input_shape=(17, )),
                        Dropout(0.2),
                        LSTM(34, input_shape=(51, ), recurrent_dropout=0.2)

                           ])


if __name__ == '__main__':
    bunch = bunch_of_matches(5)
    for item in bunch:
        for line in item:
            print(line)
        print('\n')
