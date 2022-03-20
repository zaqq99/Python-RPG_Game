# Importowanie klas
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

defeated_enemies = 0
defeated_players = 0

# Tworzenie zaklęć
fireball = Spell('Fireball', 25, 300, 'Pyromancy')
thunder = Spell('Thunder Strike', 60, 220, 'Aeromancy')
ice = Spell('Ice bolt', 50, 450, 'Hydromancy')
meteor = Spell('Meteor', 80, 880, 'Pyromancy')
earthquake = Spell('Earthquake', 200, 1400, 'Geomancy')
first_aid = Spell('First Aid', 30, 420, 'Heal')
restoration = Spell('Restoration', 80, 1250, 'Heal')

# Zaklęcia gracza
player_magic = [fireball, thunder, ice,
                meteor, earthquake, first_aid, restoration]

# Zaklęcia przeciwników
enemy_magic = [fireball, meteor, first_aid]

# Tworzenie przedmiotów
lesser_potion = Item('Lesser potion', 'potion', 'Heals for 250 HP', 250)
potion = Item('Potion', 'potion', 'Heals for 500 HP', 500)
bigger_potion = Item('Bigger potion', 'potion', 'Heals for 1500 HP', 1500)
scroll_restoration = Item('Scroll of restoration', 'scroll_restoration',
                          'Fully restores HP/MP of one part member', 10000)
scroll_multi_restorations = Item('Scroll of multi-restorations', 'scroll_restoration',
                                 "Fully restores party's HP/MP ", 10000)

grenade = Item('Grenade', 'grenade',
               'Deals 500 damage', 500)

# Przedmioty gracza wraz z ilościami
player_items = [{'item': lesser_potion, 'quantity': 15},
                {'item': potion, 'quantity': 5},
                {'item': bigger_potion, 'quantity': 5},
                {'item': scroll_restoration, 'quantity': 5},
                {'item': scroll_multi_restorations, 'quantity': 5},
                {'item': grenade, 'quantity': 5}]

# Tworzenie postaci
player1 = Person('Zaqq  :', 231, 565, 160, 34, player_magic, player_items)
player2 = Person('Kika  :', 226, 105, 402, 34, player_magic, player_items)
player3 = Person('Chucky:', 351, 265, 320, 34, player_magic, player_items)

# Tworzenie przeciwników
enemy1 = Person('Bandit :', 18200, 125, 445, 25, enemy_magic, [])
enemy2 = Person('Assasin:', 8200, 165, 845, 225, enemy_magic, [])
enemy3 = Person('Bowman :', 1200, 165, 645, 125, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + 'An Enemy attacks!' + bcolors.ENDC)


while running:
    print('=======================')

    print('\n')
    print('NAME                            HP                               MP')
    for player in players:
        player.get_stats()

    print('\n')

    for enemy in enemies:
        enemy.get_enemy_status()

    for player in players:

        player.choose_action()
        choice = input('    Choose action: ')
        index = int(choice) - 1
        # Zwykły atak
        if index == 0:
            dmg = player.atk_generator()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print('You attacked ' + enemies[enemy].name.replace(' ', '') + ' for', dmg,
                  'points of damage.')
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + ' has died.')
                #
                print('defeated enemies', defeated_enemies)
                defeated_enemies += 1
                del enemies[enemy]

        # Wybór magii
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input('    Choose spell:')) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.spell_damage_generator()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + 'Not enough mana' + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == 'Heal':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals for " +
                      str(magic_dmg) + 'HP' + bcolors.ENDC)

            elif spell.type != 'Heal':

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + spell.name + ' deals ' +
                      str(magic_dmg) + ' to ' + enemies[enemy].name.replace(' ', '')+bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + ' has died.')
                    #
                    print('defeated enemies', defeated_enemies)
                    defeated_enemies += 1
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input('    Choose item:')) - 1

    # Powrót do poprzedniego menu
            if item_choice == -1:
                continue

            item = player.items[item_choice]['item']

    # Warunek na zerową ilość przedmiotu, wtedy jeśli go wybierzemy przejdziemy do początku pętli
            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + '\n' + 'None left...' + bcolors.ENDC)
                continue

            player.items[item_choice]['quantity'] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + " heals for " +
                      str(item.prop) + 'HP' + bcolors.ENDC)
            elif item.type == 'scroll_restoration':
                if item.name == 'Scroll of multi-restorations':
                    for i in players:
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                    print(bcolors.OKGREEN + '\n' + item.name +
                          ' fully restores HP/MP ' + bcolors.ENDC)

            elif item.type == 'grenade':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + '\n' + item.name +
                      ' deals', str(item.prop), 'points of damage to ' + enemies[enemy].name.replace(' ', '') + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(' ', '') + ' has died.')
                    #
                    defeated_enemies += 1
                    print('defeated enemies', defeated_enemies)
                    del enemies[enemy]

# Sprawdzenie czy dalej toczymy walke
    #defeated_enemies = 0
    #defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
# Sprawdzenie czy wygraliśmy
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + 'You win!' + bcolors.ENDC)
        running = False

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
# Sprawdzenie czy przegraliśmy
    if defeated_players == 2:
        print(bcolors.FAIL + 'Your enemies have defeated you!' + bcolors.ENDC)
        running = False
# Tura przeciwników
    for enemy in enemies:
        enemy_choice = random.randrange(0, 1)
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.atk_generator()

            players[target].take_damage(enemy_dmg)
            print('\n'+enemy.name.replace(' ', '') + ' attacks ' +
                  players[target].name.replace(' ', '') + ' for', enemy_dmg)
# !!!!!!! Magia jest do poprawy
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == 'Heal':

                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals "+enemy.name + " for " +
                      str(magic_dmg) + 'HP' + bcolors.ENDC)

            elif spell.type != 'Heal':

                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + enemy.name.replace(' ', '') + "'s " + spell.name + ' deals ' +
                      str(magic_dmg) + ' to ' + players[target].name.replace(' ', '')+bcolors.ENDC)

                if players[target].get_hp() <= 0:
                    print('\n'+players[target].name + ' has died.')
                    del players[player]
            #print('Enemy chose', spell, 'damage is', magic_dmg)
