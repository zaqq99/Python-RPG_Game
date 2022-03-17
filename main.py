from classes.game import Person, bcolors
from classes.magic import Spell

# Creating Magic Spells
fireball = Spell('Fireball', 10, 100, 'Pyromancy')
thunder = Spell('Thunder Strike', 20, 120, 'Aeromancy')
ice = Spell('Ice bolt', 30, 150, 'Hydromancy')
meteor = Spell('Meteor', 40, 280, 'Pyromancy')
earthquake = Spell('Earthquake', 50, 400, 'Geomancy')
first_aid = Spell('First Aid', 12, 120, 'Heal')
restoration = Spell('Restoration', 20, 250, 'Hydromancy')


player_magic = [fireball, thunder, ice,
                meteor, earthquake, first_aid, restoration]


# Creating People
player = Person(460, 65, 60, 34, player_magic)
enemy = Person(1200, 65, 45, 25, [])


running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + 'An Enemy attacks!' + bcolors.ENDC)


while running:
    print('=======================')
    player.choose_action()
    choice = input('Choose action:')
    index = int(choice) - 1

    if index == 0:
        dmg = player.atk_generator()
        enemy.take_damage(dmg)
        print('You attacked for', dmg,
              'points of damage.')
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input('Choose spell:')) - 1

        spell = player.magic[magic_choice]
        magic_dmg = spell.spell_damage_generator()

    # magic_dmg = player.spell_damage_generator(magic_choice)
    # spell = player.get_spell_name(magic_choice)
    # cost = player.get_spell_cost(magic_choice)

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + 'Not enough mana' + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)
        enemy.take_damage(magic_dmg)
        print(bcolors.OKBLUE + spell.name + ' deals ' +
              str(magic_dmg) + bcolors.ENDC)

    enemy_choice = 1
    enemy_dmg = enemy.atk_generator()
    player.take_damage(enemy_dmg)
    print('Enemy attacks for', enemy_dmg)

    print('-----------------------')
    print('Enemy HP:', bcolors.FAIL + str(enemy.get_hp()) +
          '/' + str(enemy.get_max_hp()) + bcolors.ENDC)
    print('Your HP:', bcolors.OKGREEN + str(player.get_hp()) +
          '/' + str(player.get_max_hp()) + bcolors.ENDC)
    print('Your Mana:', bcolors.OKBLUE + str(player.get_mp()) +
          '/' + str(player.get_max_mp()) + bcolors.ENDC + '\n')

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + 'You win!' + bcolors.ENDC)
        running = False

    if player.get_hp() == 0:
        print(bcolors.FAIL + 'Your enemy has defeated you!' + bcolors.ENDC)
        running = False
