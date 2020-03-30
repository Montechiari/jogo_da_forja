from numpy.random import randint
from numpy import array

HEALTH_MAX_MIN = [25, 8]
WEAPON_MAX_MIN = [8, 3]


class Weapon:
    def __init__(self, thrust_damage, slash_damage):
        self.slash = slash_damage
        self.thrust = thrust_damage

    def __str__(self):
        return f"'slash': {self.slash}, 'thrust': {self.thrust}"

    def __repr__(self):
        return [self.slash, self.thrust]


class Combatent:
    def __init__(self, name):
        self.name = name
        self.health, self.reflex, self.weapon = self.generate_stats()
        self.starting_health, self.starting_reflex = self.health, self.reflex
        self.opponent = None

    def __str__(self):
        weapon = "".join(['{', str(self.weapon), '}'])
        return ", ".join([
                          "{'name': '%s'" % self.name,
                          "'health': %d" % self.health,
                          "'reflex': %d" % self.reflex,
                          "'weapon': %s}" % weapon])

    def __repr__(self):
        return [self.name, self.health, self.reflex, repr(self.weapon)]

    def generate_stats(self):
        def random_stats(max, min):
            points_to_distribute = max - (2 * min)
            first_attribute = min + randint(0, points_to_distribute + 1)
            second_attribute = max - first_attribute
            return (first_attribute, second_attribute)

        health, reflex = random_stats(*HEALTH_MAX_MIN)
        weapon = Weapon(*random_stats(*WEAPON_MAX_MIN))
        return health, reflex, weapon

    def update(self, new_attributes_dict):
        self.health = new_attributes_dict['health']
        self.reflex = new_attributes_dict['reflex']


class HumanPlayer(Combatent):
    def __init__(self, name):
        Combatent.__init__(self, name)

    def take_action(self):
        self.last_action = input(f"What action does {self.name} take?\n")
        self.last_action = int(self.last_action)
        return self.last_action


class AiPlayer(Combatent):
    def __init__(self, name):
        Combatent.__init__(self, name)
        from tensorflow.keras.models import model_from_json
        with open(f'./NN_models/{name}.json', 'r') as f:
            self.model = model_from_json(f.read())
        self.model.load_weights(f'./NN_models/{name}.h5')

    def take_action(self, vector):
        vector = array(vector)
        vector.shape = (1, 17)
        prediction = list(self.model.predict_on_batch(vector))
        value = list(prediction[0]).index(max(prediction[0]))
        return value


class DummyPlayer(Combatent):
    def __init__(self, name):
        Combatent.__init__(self, name)

    def take_action(self):
        self.last_action = randint(1, 7)
        return self.last_action
