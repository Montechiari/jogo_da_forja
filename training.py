from tensorflow.keras.models import Sequential,  model_from_json
from tensorflow.keras.layers import Dense, Dropout, LSTM, Reshape
from tensorflow.keras.backend import expand_dims
from combatents import DummyPlayer, AiPlayer
from match import Match
import numpy as np
import threading


NAMES = ['Carlos', 'Emar']
NUM_EPOCH = 10


class MatchThread(threading.Thread):
    def __init__(self, match):
        threading.Thread.__init__(self)
        self.match = match

    def run(self):
        self.match.start()


def bunch_of_matches(number_of_matches, name_of_winner):
    matches = [Match([AiPlayer(NAMES[0]), DummyPlayer(NAMES[1])])
               for i in range(number_of_matches)]
    match_threads = []
    for match in matches:
        this_thread = MatchThread(match)
        match_threads.append(this_thread)
        this_thread.start()
    for thread in match_threads:
        thread.join()
    return [np.array(match.turns.dump_like_vector(match.get_winner()))
            for match in matches
            if (len(match.turns.turn_collection) < 19) and
            match.winner == name_of_winner]


def get_model(name):
    try:
        with open(f'./NN_models/{name}.json', 'r') as f:
            model = model_from_json(f.read())
        model.load_weights(f'./NN_models/{name}.h5')
        return model
    except FileNotFoundError:
        model = Sequential([
                        Dense(51, activation='relu', input_shape=(17, )),
                        Dropout(0.2),
                        Reshape((51, 1)),
                        LSTM(34, activation='relu',
                             input_shape=(51, ), stateful=False),
                        Dropout(0.2),
                        Dense(17, activation='relu', input_shape=(34, )),
                        Dropout(0.2),
                        Dense(7, activation='softmax', input_shape=(17, ))
                           ])
        with open(f'./NN_models/{name}.json', 'w') as f:
            f.write(model.to_json())
        return model


if __name__ == '__main__':
    name = NAMES[1]
    training_model = get_model(name)
    training_model.compile(optimizer='rmsprop',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

    for k in range(100):
        bunch = bunch_of_matches(10, name)
        for epoch in range(1, NUM_EPOCH + 1):
            for i in range(len(bunch)):
                X, y = zip(*bunch[i])
                if i < len(bunch) - 1:
                    training_model.train_on_batch(np.array(X), np.array(y))
                else:
                    print(k, epoch,
                          training_model.test_on_batch(np.array(X),
                                                       np.array(y)))

    training_model.save_weights(f'./NN_models/{name}.h5')
