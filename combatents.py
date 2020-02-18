from numpy.random import randint

HEALTH_REFLEX_MAX = 25
HEATH_REFLEX_MIN = 8
WEAPON_DMG_MAX = 8
WEAPON_DMG_MIN = 3


class Weapon:
    def __init__(self, thrust_damage, slash_damage):
        self.slash = slash_damage
        self.thrust = thrust_damage


class Combatent:
    def __init__(self, name):
        self.name = name
        self.health, self.reflex, self.weapon = self.generate_stats()
        self.opponent = None
        self.action = None
        self.has_advantage = False

    def generate_stats(self):

        def random_stats(max, min):
            points_to_distribute = max - (2 * min)
            first_attribute = min + randint(0, points_to_distribute + 1)
            second_attribute = max - first_attribute
            return (first_attribute, second_attribute)

        health, reflex = random_stats(HEALTH_REFLEX_MAX, HEATH_REFLEX_MIN)
        weapon = Weapon(*random_stats(WEAPON_DMG_MAX, WEAPON_DMG_MIN))
        return health, reflex, weapon

    def updade_health(self, how_much):
        self.health += how_much

    def updade_reflex(self, how_much):
        new_reflex = self.reflex + how_much
        self.reflex = new_reflex if new_reflex > 0 else 1

    def inflict_damage(self, kind):
        damage = self.weapon[kind]
        self.opponent.updade_health(-1 * damage)

    def apply_changes(self, advantage_obj, change_instruction):
        '''format of instruction: [advantage, damage modifyer,
        damage kind, reflex modifyer]'''
        advantage, dmg_mod, dmg_kind, reflex_mod = tuple(change_instruction)
        self.change_advantage(advantage_obj, advantage)

    def change_advantage(self, advantage_obj, new_advantage):
        if new_advantage:
            if advantage_obj.who:
                advantage_obj.who.has_advantage = False
            advantage_obj.who = self
            self.has_advantage = True
            advantage_obj.kind = new_advantage


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
