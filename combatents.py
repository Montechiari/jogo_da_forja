from numpy.random import randint

HEALTH_REFLEX_MAX = 25
HEATH_REFLEX_MIN = 8
WEAPON_DMG_MAX = 8
WEAPON_DMG_MIN = 3


class Weapon:
    def __init__(self, thrust_damage, slash_damage):
        self.slash = slash_damage
        self.thrust = thrust_damage

    def __repr__(self):
        return f"'slash': {self.slash}, \
'thrust': {self.thrust}"


class Combatent:
    def __init__(self, name):
        self.name = name
        self.health, self.reflex, self.weapon = self.generate_stats()
        self.opponent = None
        self.action = None
        self.has_advantage = False

    def __repr__(self):
        weapon = "".join(['{', repr(self.weapon), '}'])
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

    def apply_changes(self, advantage_obj, change_instruction):
        '''format of instruction: [advantage, damage modifyer,
        damage kind, reflex modifyer]'''
        advantage, dmg_mod, dmg_kind, reflex_mod = tuple(change_instruction)
        self.change_advantage(advantage_obj, advantage)
        modifyer = self.calc_dmg_bonus(dmg_mod, advantage_obj)
        self.deal_damage(modifyer, dmg_kind)
        self.updade_reflex(advantage_obj, reflex_mod)

    def change_advantage(self, advantage_obj, new_advantage):
        if new_advantage:
            if advantage_obj.who:
                advantage_obj.who.has_advantage = False
            advantage_obj.who = self
            self.has_advantage = True
            advantage_obj.kind = new_advantage
        return self.has_advantage

    def calc_dmg_bonus(self, modifyer, advantage_obj):
        advantage = {"offensive": 2,
                     "defensive": 0.5,
                     None: 1}
        if self.has_advantage:
            return modifyer * advantage[advantage_obj.kind]
        else:
            return modifyer

    def deal_damage(self, modifyer, damage_kind):
        if damage_kind:
            damage = eval(f"self.weapon.{damage_kind}") * modifyer
            self.inflict_damage(damage)
            return damage
        else:
            return 0

    def inflict_damage(self, damage):
        self.opponent.updade_health(-1 * damage)

    def updade_health(self, how_much):
        new_health = self.health + how_much
        self.health = new_health if new_health > 0 else 0

    def updade_reflex(self, advantage_obj, how_much):
        advantage = {"offensive": 0,
                     "defensive": 1,
                     None: 0}
        if self.has_advantage:
            how_much += advantage[advantage_obj.kind]
        new_reflex = self.reflex + how_much
        self.reflex = new_reflex if new_reflex > 0 else 1
        return new_reflex


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
