import random
from turtle import bgcolor
from . magic import Spell
import pprint


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, deff, magic, items):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_low = atk - 10
        self.atk_high = atk + 10
        self.deff = deff
        self.magic = magic
        self.items = items
        self.actions = ['Attack', 'Magic', 'Items']
        self.name = name

    def atk_generator(self):
        return random.randrange(self.atk_low, self.atk_high)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def heal(self, dmg):
        self.hp += dmg

    def choose_action(self):
        i = 1
        print('\n' + '    ' + bcolors.BOLD +
              self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + '    Actions' + bcolors.ENDC)
        for item in self.actions:
            print('       ' + str(i) + '.', item)
            i += 1

    def choose_magic(self):
        i = 1

        print('\n' + bcolors.OKBLUE + bcolors.BOLD + '    Magic' + bcolors.ENDC)
        for spell in self.magic:
            print('       ' + str(i) + '.', spell.name,
                  '(cost:', str(spell.cost) + ')')
            i += 1

    def choose_item(self):
        i = 1
        print('\n' + bcolors.OKGREEN + bcolors.BOLD + '    Items' + bcolors.ENDC)
        for item in self.items:
            print('       ' + str(i) + '.', item['item'].name +
                  ':', item['item'].description, "(x " + str(item['quantity']) + ")")
            i += 1

# Wybieranie celu przez wrogów
    def choose_target(self, enemies):
        i = 1
        print('\n' + bcolors.FAIL + bcolors.BOLD +
              '    Target:' + bcolors.ENDC
              )
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print('       ' + str(i) + '.', enemy.name)
                i += 1
        choice = int(input('    Choose target:')) - 1
        return choice

# Pasek życia dla wroga

    def get_enemy_status(self):
        hp_bar = ''
        bar_ticks = (self.hp / self.max_hp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += '█'
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += ' '

        hp_string = str(self.hp) + '/' + str(self.max_hp)
        current_hp = ''

        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)

            while decreased > 0:
                current_hp += ' '
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print(
            '                         __________________________________________________')
        print(bcolors.BOLD + self.name + '   ' + current_hp + '  |' + bcolors.ENDC + bcolors.FAIL +
              hp_bar + bcolors.ENDC + bcolors.BOLD + '|' + bcolors.ENDC)

# Tworzenie przejrzystych wartości dla życia i many

    def get_stats(self):
        hp_bar = ''
        bar_ticks = (self.hp / self.max_hp) * 100 / 4

        mp_bar = ''
        mp_ticks = (self.mp / self.max_mp) * 100 / 10

        while bar_ticks > 0:
            hp_bar += '█'
            bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += ' '

        while mp_ticks > 0:
            mp_bar += '█'
            mp_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += ' '

# Żeby paski życia i many się nie rozjeżdżały
        hp_string = str(self.hp) + '/' + str(self.max_hp)
        current_hp = ''
        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += ' '
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + '/' + str(self.max_mp)
        current_mp = ''

        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)
            while decreased > 0:
                current_mp += ' '
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

# Wyświetlanie pasków życia i many
        print('                      _________________________              __________')
        print(bcolors.BOLD + self.name + '   ' + current_hp + '  |'+bcolors.OKGREEN +
              hp_bar + bcolors.ENDC + bcolors.BOLD + '|   ' + current_mp + '  |'+bcolors.OKBLUE + mp_bar + bcolors.ENDC+bcolors.BOLD+'|'+bcolors.ENDC)

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.spell_damage_generator()

        #pct = self.hp / self.max_hp * 100

        if self.mp < spell.cost:  # or spell.type == 'Heal' and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg
