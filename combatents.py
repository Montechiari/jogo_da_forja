from numpy.random import randint

HEALTH_REFLEX_MAX, HEATH_REFLEX_MIN = 25, 8
WEAPON_DMG_MAX, WEAPON_DMG_MIN = 8, 3


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
        self.opponent = None
        self.action = None
        self.has_advantage = False

    def __repr__(self):
        weapon = "".join(['{', str(self.weapon), '}'])
        return ", ".join([
                          "{'health': %d" % self.health,
                          "'reflex': %d" % self.reflex,
                          "'weapon': %s}" % weapon])

    def generate_stats(self):
        def random_stats(max, min):
            points_to_distribute = max - (2 * min)
            first_attribute = min + randint(0, points_to_distribute + 1)
            second_attribute = max - first_attribute
            return (first_attribute, second_attribute)

        health, reflex = random_stats(HEALTH_REFLEX_MAX, HEATH_REFLEX_MIN)
        weapon = Weapon(*random_stats(WEAPON_DMG_MAX, WEAPON_DMG_MIN))
        return health, reflex, weapon

    def update(self, new_attributes_dict):
        self.health = new_attributes_dict['health']
        self.reflex = new_attributes_dict['reflex']


class HumanPlayer(Combatent):
    def __init__(self, name):
        Combatent.__init__(self, name)

    def take_action(self):
        return "Not implemented"


class AIPlayer(Combatent):
    def __init__(self, name):
        Combatent.__init__(self, name)

    def take_action(self):
        return "Not implemented"


class DummyPlayer(Combatent):
    def __init__(self, name):
        Combatent.__init__(self, name)

    def take_action(self):
        self.action = randint(1, 7)
        return self.action
