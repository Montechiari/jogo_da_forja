from combatents import AiPlayer
from match import Match
from training import load_model, MatchThread
from tqdm import tqdm

CYCLES = 500
NUM_THREADS = 20
NAMES = ['Carlos', 'Emar']

win_register = {name: 0 for name in NAMES}
win_register[None] = 0
models = [load_model(name) for name in NAMES]

for i in tqdm(range(CYCLES)):
    matches = [Match([AiPlayer(NAMES[i], models[i]) for i in range(2)])
               for _ in range(NUM_THREADS)]
    threads = [MatchThread(match) for match in matches]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for match in matches:
        win_register[match.get_winner().name] += 1

for name in NAMES:
    print(f"{name}'s win count: {win_register[name]}.")
