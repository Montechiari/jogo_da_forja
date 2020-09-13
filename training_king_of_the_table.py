from tensorflow.keras.models import Sequential,  model_from_json
from tensorflow.keras.layers import Dense, Dropout, LSTM, Reshape
from tensorflow.keras.backend import expand_dims
from combatents import DummyPlayer, AiPlayer
from match import Match
import numpy as np
import threading
from tqdm import tqdm
from copy import copy
import os
from random import shuffle


NAMES = ['Carlos', 'Emar']
NUM_EPOCH = 20
NUM_LABELS = 7

MODELS = {'regular': Sequential([
                Dense(NUM_LABELS * 8, activation='relu',
                      input_shape=(17, ),
                      kernel_initializer='random_uniform'),
                Dropout(0.5),
                Dense(NUM_LABELS * 4, activation='relu',
                      input_shape=(NUM_LABELS * 8, ),
                      kernel_initializer='random_uniform'),
                Dropout(0.3),
                Dense(NUM_LABELS * 2, activation='relu',
                      input_shape=(NUM_LABELS * 4, ),
                      kernel_initializer='random_uniform'),
                Dropout(0.2),
                Dense(NUM_LABELS, activation='softmax',
                      input_shape=(NUM_LABELS * 2, ))
                   ]),
          'LSTM': Sequential([
                Dense(NUM_LABELS * 8, activation='relu',
                      input_shape=(17, ),
                      kernel_initializer='random_uniform'),
                Dropout(0.5),
                Reshape((NUM_LABELS * 8, 1)),
                LSTM(NUM_LABELS * 4, return_sequences=True, dropout=0.5),
                LSTM(NUM_LABELS * 2, dropout=0.2),
                Dense(NUM_LABELS, activation='softmax',
                      input_shape=(NUM_LABELS * 2, ))
          ]),
          'simplest': Sequential([
                Dense(NUM_LABELS * 3, activation='relu',
                      input_shape=(17, ),
                      kernel_initializer='random_uniform'),
                Dense(NUM_LABELS, activation='softmax',
                      input_shape=(NUM_LABELS * 3, ),
                      kernel_initializer='random_uniform')
          ])
          }


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


def matches_to_train(number_of_matches):
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

    match_logs = [(np.array(match.turns.dump_like_vector(match.get_winner())),
                   match.evaluate_match_in_respect_to(match.get_winner()))
                  for match in matches
                  if (len(match.turns.turn_collection) < 19)]
    return match_logs


def get_model(name):
    try:
        with open(f'./NN_models/{name}.json', 'r') as f:
            model = model_from_json(f.read())
        model.load_weights(f'./NN_models/{name}.h5')
        return model
    except FileNotFoundError:
        model = MODELS['simplest']

        with open(f'./NN_models/{name}.json', 'w') as f:
            f.write(model.to_json())
        return model


def compete(contender, champion, percentage_to_meet):
    contender_wins, total_valid_matches = 0, 0
    for i in tqdm(range(1000)):
        matches = [Match([AiPlayer('contender', contender),
                          AiPlayer('champion', champion)])
                   for i in range(10)]
        match_threads = []
        for match in matches:
            this_thread = MatchThread(match)
            match_threads.append(this_thread)

        for thread in match_threads:
            thread.start()

        for thread in match_threads:
            thread.join()

        for match in matches:
            if len(match.turns.turn_collection) < 19:
                total_valid_matches += 1
                if match.get_winner().name == 'contender':
                    contender_wins += 1

    rate = (contender_wins / total_valid_matches)
    print('Win rate:', rate)
    return rate > percentage_to_meet


if __name__ == '__main__':
    contender_model = get_model('contender')
    champion_model = get_model('champion')

    contender_model.compile(optimizer='adam', loss='categorical_crossentropy',
                            metrics=['accuracy'])
    champion_model.compile(optimizer='adam', loss='categorical_crossentropy',
                           metrics=['accuracy'])

    training_data = []
    print('Running matches to train...')
    for i in tqdm(range(2400)):
        bunch = matches_to_train(24)
        training_data.extend(bunch)
    print('There are {} matches to learn.'.format(len(training_data)))
    print('Taking the best 1/20...')
    training_data.sort(key=lambda match: match[1])
    training_data = training_data[0:int(len(training_data) / 20)]
    shuffle(training_data)
    testing_data = training_data[:int(len(training_data) / 20)]

    training_data, _ = zip(*training_data)
    testing_data, _ = zip(*testing_data)

    training_data = np.concatenate(training_data)
    X, y = zip(*training_data)
    X = np.array(X)
    y = np.array(y)
    contender_model.fit(X, y, epochs=20)

    testing_data = np.concatenate(testing_data)
    X2, y2 = zip(*testing_data)
    X2 = np.array(X2)
    y2 = np.array(y2)
    print(contender_model.evaluate(X2, y2))

    contender_model.save_weights('./NN_models/contender.h5')

    try:
        if(compete(contender_model, champion_model, 0.6)):
            print('Contender performed 60% better than Champion.')
            os.remove('./NN_models/champion.h5')
            os.remove('./NN_models/champion.json')
            os.rename('./NN_models/contender.h5', './NN_models/champion.h5')
            os.rename('./NN_models/contender.json',
                      './NN_models/champion.json')
        else:
            print('Contender failed to beat the Champion.')
            os.remove('./NN_models/contender.h5')
            os.remove('./NN_models/contender.json')

    except (FileNotFoundError, AssertionError):
        os.rename('./NN_models/contender.h5', './NN_models/champion.h5')
        os.rename('./NN_models/contender.json',
                  './NN_models/champion.json')
