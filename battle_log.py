class BattleLogger:
    def __init__(self):
        self.turn_collection = []

    def add_turn(self, turn):
        self.turn_collection.append(turn)
