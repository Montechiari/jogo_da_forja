from tensorflow.keras.models import Sequential,  model_from_json
from tensorflow.keras.layers import Dense, Dropout
from combatents import DummyPlayer
from match import Match
import numpy as np
import threading
from tqdm import tqdm
from copy import copy


NAMES = ['Carlos', 'Emar']
NUM_EPOCH = 20
NUM_LABELS = 7


class MatchThread(threading.Thread):
    def __init__(self, match):
        threading.Thread.__init__(self)
        self.match = match

    def run(self):
        self.match.start()


def load_model(name):
    with open(f'./NN_models/{name}.json', 'r') as f:
        model = model_from_json(f.read())
        model.load_weights(f'./NN_models/{name}.h5')
    return model


def bunch_of_matches(number_of_matches):
    matches = [Match([DummyPlayer(NAMES[1]),
                      DummyPlayer(NAMES[0])])
               for i in range(number_of_matches)]

    match_threads = []
    for match in matches:
        this_thread = MatchThread(match)
        match_threads.append(this_thread)

    for thread in match_threads:
        thread.start()

    for thread in match_threads:
        thread.join()

    match_logs = []
    for match in matches:
        if (len(match.turns.turn_collection) < 19):
            match_logs.append((get_perm_log(match), 1))
            match_logs.append((get_perm_log(match, winner=False), 0))

    return match_logs


def get_perm_log(match, winner=True):
    player = match.get_winner() if winner else match.get_winner().opponent
    match_log = match.turns.dump_like_vector(player)
    return match_log[0][0][:6]


def get_model(name):
    try:
        with open(f'./NN_models/{name}.json', 'r') as f:
            model = model_from_json(f.read())
        model.load_weights(f'./NN_models/{name}.h5')
        return model
    except FileNotFoundError:
        model = Sequential([
                        Dense(24, activation='relu',
                              input_shape=(6, ),
                              kernel_initializer='random_uniform'),
                        Dropout(0.5),
                        Dense(24, activation='relu',
                              input_shape=(24, ),
                              kernel_initializer='random_uniform'),
                        Dropout(0.5),
                        Dense(12, activation='relu',
                              input_shape=(24, ),
                              kernel_initializer='random_uniform'),
                        Dropout(0.5),
                        Dense(1, activation='sigmoid',
                              input_shape=(12, ))
                           ])
        with open(f'./NN_models/{name}.json', 'w') as f:
            f.write(model.to_json())
        return model


if __name__ == '__main__':
    name = 'win_chance'
    training_model = get_model(name)
    training_model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['binary_accuracy'])

    training_data = []
    print('Running matches...')
    for i in tqdm(range(20)):
        training_data.extend(bunch_of_matches(24))
    np.random.shuffle(training_data)

    length = len(training_data)
    test_marker = int(length - (length * 0.1))
    X_train, y_train = zip(*training_data[:test_marker])
    X_test, y_test = zip(*training_data[test_marker:])

    for i, datum in enumerate(X_train):
        print(training_model.predict([X_train[i]]), y_train[i])
    # print(X_train[0])
    # training_model.fit(X_train, y_train, epochs=20)
    # training_model.evaluate(X_test, y_test)
    # training_model.save_weights(f'./NN_models/{name}.h5')
