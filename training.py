from tensorflow.keras.models import Sequential,  model_from_json
from tensorflow.keras.layers import Dense, Dropout, LSTM, Reshape
from tensorflow.keras.backend import expand_dims
from combatents import DummyPlayer, AiPlayer
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


def bunch_of_matches(number_of_matches, name_of_winner):
    model = load_model(name_of_winner)
    opponents_name = copy(NAMES)
    opponents_name.remove(name_of_winner)
    opp_model = load_model(opponents_name[0])
    matches = [Match([AiPlayer(name_of_winner, model),
                      AiPlayer(opponents_name[0], opp_model)])]
    # matches = [Match([DummyPlayer(NAMES[1]),
    #                   DummyPlayer(NAMES[0])])
    #            for i in range(number_of_matches)]
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
        model = Sequential([
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
                           ])
        with open(f'./NN_models/{name}.json', 'w') as f:
            f.write(model.to_json())
        return model


if __name__ == '__main__':
    name = NAMES[0]
    training_model = get_model(name)
    training_model.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
    training_data = []
    print('Running matches...')
    for i in tqdm(range(2000)):
        bunch = bunch_of_matches(24, name)
        training_data.extend(bunch)
    print('There are {} matches to learn.'.format(len(training_data)))
    print('Taking the best 1/20...')
    training_data.sort(key=lambda match: match[1])
    training_data = training_data[0:int(len(training_data) / 20)]
    training_data, _ = zip(*training_data)
    for epoch in range(1, NUM_EPOCH + 1):
        for i in range(len(training_data)):
            X, y = zip(*training_data[i])
            if i < len(training_data) - 1:
                print('Training:',
                      training_model.train_on_batch(np.array(X), np.array(y)))
            else:
                print('Epoch {} testing: {}'.format(epoch,
                      training_model.test_on_batch(np.array(X),
                                                   np.array(y))))

    training_model.save_weights(f'./NN_models/{name}.h5')
