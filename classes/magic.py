import random


class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def spell_damage_generator(self):
        magic_low = self.dmg - 15
        magic_high = self.dmg + 15
        return random.randrange(magic_low, magic_high)


'''
    def spell_damage_generator(self, i):
        magic_low = self.magic[i]['damage'] - 5
        magic_high = self.magic[i]['damage'] + 5
        return random.randrange(magic_low, magic_high)

    def get_spell_name(self, i):
        return self.magic[i]['name']

    def get_spell_cost(self, i):
        return self.magic[i]['cost']
'''
