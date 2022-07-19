import random
import logging
from entities import Entity, Hero, Enemy
import re
import os.path

def main():
    logging.basicConfig(filename = "game.log", level = logging.DEBUG, format = '%(asctime)s :: %(message)s')

    #Save file protection
    while True:
        while True:
            try:
                file_name = input("Enter save name: ")
                check = re.search(",", file_name)
                check = re.search(".", file_name)
                check = re.search("/", file_name)
                check = re.search("'", file_name)
                check = re.search('"', file_name)
                if check != None:
                    raise ValueError
            except ValueError as ve:
                print("Please, no special characters.")
                logging.error("Special characters detected.")
            else:
                break
        file_name += ".txt"
        if os.path.exists(file_name):
            print("Save detected, please try again.")
            logging.error("Attempted save overwrite.")
        else:
            break
    
    print("\n")
    adventure_log = open(file_name, 'w')
    logging.info("Configured save file.")
    lore = open('lore.txt', 'r')
    lore_txt = lore.read()
    print(lore_txt, "\n\n")
    adventure_log.write(lore_txt)
    adventure_log.write("\n\n")
    lore.close()

    character_log = 'characters.csv'
    lst_heroes = []
    lst_enemies = []
    lst_heroes = load_heroes(character_log)
    lst_enemies = load_enemies(character_log)
    logging.info("Loaded premade heroes and enemies.")

    quit = True
    tutorialized = False
    attempt = 0
    player_lst = []

    while quit:
        #Bulk of gameplay code, for replayability.
        attempt += 1
        print("Attempt " + str(attempt) + ":\n\n")
        adventure_log.write("Attempt " + str(attempt) + ":\n\n")
        
        infinity = False
        choice_mode = 2
        #Mode Selection, workaround implemented due to TypeError glitch
        while tutorialized:
            while True:
                choice_mode = input("Would you like to try inifinite mode? 1) Yes 2) No\n>> ")
                if choice_mode == "1":
                    adventure_log.write("You sense the dungeon seeming to expand, its depths fathomless before you...\n\n")
                    infinity = True
                    break
                elif choice_mode == "2":
                    break
                else:
                    print("Please try again.")
                    logging.error("Invalid input on mode selection, trying again...l")

            break


            # try:      #previously mentioned TypeError glitch
            #     choice_mode = int(input("Would you like to try inifinite mode? 1) Yes 2) No\n>> "))
            #     check = type(choice_mode)
            #     if check != int():
            #         raise TypeError
            #     if ((choice_diff < 1) or (choice_mode > 2)):
            #         raise ValueError
            # except TypeError as te:
            #     print("Please try again.")
            #     logging.error("Improper input type on mode, trying again...")
            # except ValueError as ve:
            #     print("Please try again.")
            #     logging.error("Exceeded options on mode, trying again...")
            # else:
            #     break
        # if choice_mode == 1:
        #     adventure_log.write("You sense the dungeon seeming to expand, its dempts fathomless before you...\n\n")
        #     infinity = True

        choice_diff = 1
        #Difficulty Selection, workaround deployed again
        while tutorialized:
            
            while True:
                choice_diff = int(input("How difficiult of a challenge will you face? 1) Easy 2) Medium 3) Hard\n>> "))
                if choice_diff == 1:
                    break
                if choice_diff == 2:
                    break
                if choice_diff == 3:
                    break
                else:
                    print("Please try again.")
                    logging.error("Invalid input on difficulty selection, trying again...l")
            break

            # try:
            #     choice_diff = int(input("How difficiult of a challenge will you face? 1) Easy 2) Medium 3) Hard\n>> "))
            #     check = type(choice_diff)
            #     if check != int():
            #         raise TypeError
            #     if ((choice_diff < 0) or (choice_diff > 3)):
            #         raise ValueError
            # except TypeError as te:
            #     print("Please try again.")
            #     logging.error("Improper input type on difficulty, trying again...")
            # except ValueError as ve:
            #     print("Please try again.")
            #     logging.error("Exceeded options on difficulty, trying again...")
            # else:
            #     break

        match choice_diff:
            case 1:
                diff = [1, 2]
                diff_message = "You take the well trodden path, torches aplenty.\n"
            case 2:
                diff = [2, 2]
                diff_message = "You find a hidden path, faint sounds echoing down the dusty halls.\n"
            case 3:
                diff = [2, 1]
                diff_message = "You stumble across a path, fresh blood visible in the flagstones but a glint of light taunting in the deep darkness...\n"

        
        #Character creation
        while True:
            print("Select your class:\n")
            player = None
            player = character_select(lst_heroes)
            if player != None:
                print("\n")
                break

        print(diff_message)
        adventure_log.write("Your courageous " + player.name + " has entered the dungeon!\n" + diff_message)
        print("\n")
        player.changeName()
        adventure_log.write(player.name + " prepares themselves for whatever may come.\n\n")
        print("\n")
        player_max_hp = player.current_hp

        while True:

            #blade trap
            blade = str(random.randint(1, 2))
            print("You hear a blade coming from behind!")
            adventure_log.write("You hear a blade coming from behind!\n")

            choice_blade = str(input("Do you 1) jump or 2) duck?  >> "))
            print("\n")
            if choice_blade == "1":
                if choice_blade == blade:
                    print("You accidentally jumped into the path of the blade.\n")
                    adventure_log.write("You accidentally jumped into the path of the blade, taking 5 damage.\n\n")
                    player.take_damage(5)
                else:
                    print("You manage to jump out of the way, avoiding damage.")
                    adventure_log.write("You manage to jump out of the way, avoiding damage.\n\n")
            elif choice_blade == "2":
                if choice_blade == blade:
                    print("You duck down...into the path of the blade!")
                    adventure_log.write("You duck down...into the path of the blade!\n\n")
                    player.take_damage(5)
                else:
                    print("You manage to duck out of the way, avoiding damage.")
                    adventure_log.write("You manage to duck out of the way, avoiding damage.\n\n")
            else:
                print("Stricken by indecision, you just stand there.")
                adventure_log.write("Stricken by indecision, you just stand there and take it.\n\n")
                player.take_damage(5)


            #door puzzle
            door = random.randint(1, 5)
            print("You approach five doors and a riddle:")
            adventure_log.write("You approach five doors and a riddle:\n")
            match door:
                case 1:
                    print('"What is 0! equal to?"')
                    adventure_log.write('"What is 0! equal to?"\n')
                case 2:
                    print('"What can be as lonely as one?"')
                    adventure_log.write('"What can be as lonely as one?"\n')
                case 3:
                    print('"What is a crowd?"')
                    adventure_log.write('"What is a crowd?"\n')
                case 4:
                    print('"Where___ art thou?"')
                    adventure_log.write("Where___ art thou?\n")
                case 5:
                    print('"I\'ve run out of riddles, just take the last door."')
                    adventure_log.write('"I\'ve run out of riddles, just take the last door."\n')

            while True:
                while True:
                    try:
                        choice_door = int(input("Which door will you choose? >> "))
                        check = type(choice_door)
                        if check != type(door):
                            raise TypeError
                    except TypeError as te:
                        print("Please try again.")
                        logging.error("Improper input type on door, trying again...")
                    else:
                        break

                print("\n")
                if choice_door == door:
                    print("Onward, to battle!", "\n")
                    adventure_log.write("You deduced the correct door and moved onward towards the final confrontation.\n\n")
                    break
                elif choice_door > 5:
                    print("You ran into the wall for some reason, taking 1 damage.\n")
                    player.take_damage(1)
                    adventure_log.write("You ran into the wall for some reason, bumping your nose against the stone.\n")
                elif abs(choice_door - door) < 2:
                    print("You were bitten by a door mimic!  You take 3 damage.\n")
                    adventure_log.write("You were ebitten by a door mimic, but managed to break free from it.\n")
                    player.take_damage(3)
                else:
                    print("A pit trap drops you to your doom.  Oh no.\n")
                    adventure_log.write("A pit trap drops you to your doom.  Thus an ignoble end to your tale of adventure, alas not to evil but to pure bad luck.\n")
                    quit == False
                    break
            
            if quit == False:
                break

            combat(player, lst_enemies, adventure_log, player_max_hp, diff, infinity)
            if player.current_hp != 0:
                print("You were victorious, successfully locating the Heart of Darkness, the dreaded artifact haunting the cave!\nYou're pretty sure it's just a very, very moldy onion with an unpleasant smell.\n")
                adventure_log.write("You were victorious, successfully locating the Heart of Darkness, the dreaded artifact haunting the cave!\nYou're pretty sure it's just a very, very moldy onion with an unpleasant smell.\n\n")
            tutorialized = True
            break

        player_lst.append(player)

        # while True:       #unknown TypeError glitch, still investigating, rudimentary workaround developed.
            # try:
            #     again = int(input("Would you like to try again?\n1) Yes 2) No  >>>  "))
            #     check = type(again)
            #     # if check != int():
            #     #     raise TypeError
            #     if again != (1 or 2):
            #         raise ValueError
            # except TypeError as te:
            #     print("Input error, please try again.")
            #     logging.error("Type error in input, trying again...")
            # except ValueError as ve:
            #     print("Value Error, please try again.")
            #     logging.error("Value error in input, trying again...")
            # else:
            #     break
        while True:
            again = input("Would you like to try again?\n1) Yes 2) No  >>>  ")
            if again == "1":
                break
            elif again == "2":
                print("After a long, harrowing series of adventures, the survivors retreat back to town to consider their next steps, ever seeking the Heart of Darkness...\n")
                adventure_log.write("After a long, harrowing series of adventures, the survivors retreat back to town to consider their next steps, ever seeking the Heart of Darkness...\n\n")
                print_count = 1
                for elem in player_lst:
                    adventure_log.write(str(print_count) + ")" + str(elem) + "\n")
                    print_count += 1
                adventure_log.close()
                quit = False
                break
            else:
                print("Please try again.")
                logging.error("Invalid input on 'try again', trying again, lol")


        print("\n\n")
    print_count = 1
    for elem in player_lst:
        print(str(print_count) + ")" + str(elem))
        print_count += 1

    return 0

def roll(n):
    hit = random.randint(1, n)
    if hit > 10:
        return True
    else:
        return False

def combat(player, lst_enemies, adventure_log, player_max_hp, diff, infinity):
    xp = 0
    battle_count = 0
    player_max_hp = (player.hp * player.lvl)
    while True:     #primary combat initialization, looped through in infinity mode.
        turn_count = 1
        battle_count += 1
        xp_threshold = 5 * player.lvl
        foe_rng = random.randint(0, (len(lst_enemies) - 1))
        #foe = lst_enemies[foe_rng]
        foe = Enemy(lst_enemies[foe_rng].name, lst_enemies[foe_rng].hp, lst_enemies[foe_rng].power, lst_enemies[foe_rng].lvl)
        if infinity:
            print("Fight " + str(battle_count) + "\n")
            if battle_count > 1:
                i = 0
                while i < (battle_count - 1):
                    foe.lvlUp()
                    i += 1
        foe.current_hp = foe.hp * foe.lvl
        print("You turn a corner and find a level " + str(foe.lvl) + " " + foe.name + " blocking your path!")
        adventure_log.write("\nYou turn a corner and find a level "  + str(foe.lvl) + " " + foe.name + " blocking your path!\n\n")
        
        while True:     #Primary combat loop, regardless of mode.
            print("\n")
            print(player.name + " HP: " + str(player.current_hp) + "/" + str(player_max_hp))
            defend = 0
            dmg = player.attack() * diff[1]
            while True:
                try:
                    player_turn = int(input("1) Attack\n2) Defend\n3) Potion\n>>> "))
                    # if type(player_turn) != int():
                    #     raise TypeError
                    if (player_turn < 0) or (player_turn >3):
                        raise ValueError
                # except TypeError as te:
                #     print("Please try again.\n")
                #     logging.error("Invalid action input, trying again...")
                except ValueError as ve:
                    print("Please try again, exceeded list value.\n")
                    logging.error("Exceeded list value, trying again...")
                else:
                    break

            match player_turn:
                case 1:
                    if roll(20):
                        foe.take_damage(dmg)
                    else:
                        print("The " + foe.name + " managed to avoid your strike.\n")
                case 2:
                    print("You brace yourself for the enemy's attack!\n")
                    defend = dmg
                case 3:
                    print("You chug a potion, trying to heal yourself.  You regain " + str(player.hp) + " hp.\n")
                    player.current_hp += player.hp
                    if player.current_hp > player_max_hp:
                        player.current_hp = player_max_hp
                case default:
                    print("You think too long and too hard, the " + foe.name + " acting during your moment of distraction!\n")

            if foe.current_hp == 0:
                print("You defeated the " + foe.name + "!  Congratulations!\n")
                adventure_log.write("The " + foe.name + " has been defeated!  ")

                if player.current_hp >= (player_max_hp / 2):
                    adventure_log.write("It was an easy battle, leaving you ready for more.\n\n")
                elif player.current_hp <= (player_max_hp / 4):
                    adventure_log.write("It was a long, difficult battle, leaving you barely alive.\n\n")
                else:
                    adventure_log.write("You were victorious, though you were not without injury yourself.\n\n")

                break

            foe_dmg = 0
            print(foe)
            if ((turn_count % foe.power) != 0):
                if roll(20):
                    print("The " + foe.name + " attacks, landing a solid blow.\n")
                    foe_dmg = (foe.attack() * diff[0]) - defend
                    player.take_damage(foe_dmg)
                else:
                    print("The " + foe.name + " attacks, but misses you by a mile.\n")
            else:
                print("The vicious " + foe.name + " takes a moment to prepare itself.\n")

            if (player.current_hp == 0):
                print("You have been struck down by the " + foe.name + "!  Unfortunately, your adventure ends here.\n")
                print(str(foe) + "\n")
                adventure_log.write("You have been struck down by the " + foe.name + "!  Unfortunately, your adventure ends here.\n\n")
                adventure_log.write(str(foe) + "\n\n")
                break

        if infinity == False:
            break
        else:
            if player.current_hp != 0:
                print("You proceed deeper into the dark ruins, seeking ever deeper depths.\n\n\n")
                adventure_log.write("You proceed deeper into the dark ruins, seeking ever deeper depths.\n\n")
                xp += (foe.power * foe.lvl)
                if xp >= xp_threshold:
                    print("Level up!\n")
                    player.lvlUp()
                    xp -= xp_threshold
                    player_max_hp = player.hp * player.lvl
                    player.current_hp += player.hp
                    if player.current_hp > player_max_hp:
                        player.current_hp = player_max_hp
            else:
                if battle_count == 1:
                    print("You were defeated by your very first opponent, an unfortunate result.\n\n")
                    adventure_log.write("You were defeated by your very first opponent, an unfortunate result.\n\n\n")
                else:
                    print("You managed to survive " + str(battle_count) + " fights before losing.\n\n")
                    adventure_log.write("You managed to survive " + str(battle_count) + " fights before losing.\n\n\n")
                break



def load_heroes(fname):
    lst_heroes = []

    with open(fname, "r") as f:

        for line in f:
            info = line.split(',')
            if info[0] == "Hero":
                character = Hero(info[1], info[2], info[3], info[4])
            else:
                character = None

            #testing for presence
            #print(character, "\n")

            if character != None:
                lst_heroes.append(character)
            
        return lst_heroes

def load_enemies(fname):
    lst_enemies = []

    with open(fname, "r") as f:

        for line in f:
            info = line.split(',')
            if info[0] == "Enemy":
                character = Enemy(info[1], info[2], info[3], info[4])
            else:
                character = None

            # testing for presence
            #print(character, "\n")

            if character != None:
                lst_enemies.append(character)
            
        return lst_enemies
    
# def character_select(choices):
#     #Dynamically print character options based on preloaded characters.
#     option = 1
#     for elem in choices:
#         print(str(option) + ")", elem)
#         option += 1

#     while True:
#         try:
#             decision = int(input(""))
#             # if type(decision) != int():
#             #     raise TypeError
#             if decision > len(choices):
#                 raise ValueError
#         except TypeError as te:
#             print("Improper input, try again.")
#             logging.error("Improper input, trying again...")
#         except ValueError as ve:
#             print("Try again.")
#             logging.error("Exceeded list, trying again...")
#         else:
#             decision -= 1
#             player = choices[decision]
#             break

def character_select(choices):
    #Dynamically print character options based on preloaded characters.
    option = 1
    fill = []
    for elem in choices:
        print(str(option) + ")", elem)
        option += 1

    while True:
        try:
            decision = int(input(""))
            # if type(decision) != int():
            #     raise TypeError
            if decision > len(choices):
                raise ValueError
        except TypeError as te:
            print("Improper input, try again.")
            logging.error("Improper input, trying again...")
        except ValueError as ve:
            print("Try again.")
            logging.error("Exceeded list, trying again...")
        else:
            decision -= 1
            player = Hero(choices[decision].name, choices[decision].hp, choices[decision].power, choices[decision].lvl)
            break

    return player



'''
Lore Intro - kinda check
Load characters/enemies - check

Pick Character - check
Optional name change - check

Blade trap - check, hiccup on taking damage
Door Puzzle -
Boss fight -

Infinite battle mode - ?
'''

if __name__ == "__main__":
    main()