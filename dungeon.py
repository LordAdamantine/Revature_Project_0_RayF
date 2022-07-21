from multiprocessing.sharedctypes import Value
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
        #Save protection checks if a file with that name already exists, forcing the user to pick a new one if it does.
        if os.path.exists(file_name):
            print("Save detected, please try again.")
            logging.error("Attempted save overwrite.")
        else:
            break
    
    #This block configures the now confirmed save file name and pre loads it and the console with the lore.
    print("\n")
    adventure_log = open(file_name, 'w')
    logging.info("Configured save file.")
    lore = open('lore.txt', 'r')
    lore_txt = lore.read()
    print(lore_txt, "\n\n")
    adventure_log.write(lore_txt)
    adventure_log.write("\n\n")
    lore.close()

    #This block loads the external file of different player classes and enemies, initializing the enemies before closing the reference file and logging the action.
    character_log = 'characters.csv'
    lst_heroes = []
    lst_enemies = []
    lst_heroes = load_heroes(character_log)
    lst_enemies = load_enemies(character_log)
    logging.info("Loaded premade heroes and enemies.")

    #This is just to instantiate certain values for later.
    quit = True
    tutorialized = False
    attempt = 0
    player_lst = []

    while quit:
        #Bulk of gameplay code is in this while loop, for replayability..
        #This is to help differentiate between runs in the logs.
        attempt += 1
        print("Attempt " + str(attempt) + ":\n\n")
        adventure_log.write("Attempt " + str(attempt) + ":\n\n")
        
        infinity = False
        choice_mode = 2
        #Mode Selection, locked behind a variable that is changed after the first run, unlocking it by winning.
        while tutorialized:
            try:
                choice_mode = int(input("Would you like to try inifinite mode? 1) Yes 2) No\n>> "))
                check = type(choice_mode)
                if ((choice_mode < 1) or (choice_mode > 2)):
                    raise ValueError
            except ValueError as ve:
                print("Please try again.")
                logging.error("Improper input on mode, trying again...")
            else:
                if choice_mode == 1:
                    adventure_log.write("You sense the dungeon seeming to expand, its depths fathomless before you...\n\n")
                    infinity = True
                break

    

        choice_diff = 1
        #Difficulty Selection, also locked behind first run.
        while tutorialized:
            try:
                choice_diff = int(input("How difficiult of a challenge will you face? 1) Easy 2) Medium 3) Hard\n>> "))
                check = type(choice_diff)
                if ((choice_diff < 1) or (choice_diff > 3)):    #basically checks to see if you enter anything that isn't 1, 2, or 3
                    raise ValueError
            except ValueError as ve:
                print("Please try again.")
                logging.error("Improper input on difficulty, trying again...")
            else:
                break

        match choice_diff:      #Modifies certain values later on.
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
            
        #This section instantiates the max hp value not currently connected to the main class for ease of use.
        #It also loads in messages to the console and adventure log based on your character and difficulty selection.
        print(diff_message)
        adventure_log.write("Your courageous " + player.name + " has entered the dungeon!\n" + diff_message)
        print("\n")
        player.changeName()
        adventure_log.write(player.name + " prepares themselves for whatever may come.\n\n")
        print("\n")
        player_max_hp = player.current_hp

        while True:     #This is the bulk of the actual gameplay, including the trap, puzzle, and combat() call.

            #blade trap
            blade = str(random.randint(1, 2))
            print("You hear a blade coming from behind!")
            adventure_log.write("You hear a blade coming from behind!\n")

            #Bases the results off of the user's input and whether or not it matches a randomly generated value.
            #If it detects a non standard input, it has a joke response.
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
            else:       #This is basically my error exception for this block since I don't care about what wrong input comes in, only if it's wrong.
                print("Stricken by indecision, you just stand there.")
                adventure_log.write("Stricken by indecision, you just stand there and take it.\n\n")
                player.take_damage(5)


            #door puzzle, produces one of 5 randomized riddles for the door.
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

            while True:     #This is the rest of the door puzzle code, inside a while loop because of input checking and one of the options.
                while True:
                    try:    #Normal input check shenanigans here.
                        choice_door = int(input("Which door will you choose? >> "))
                        check = type(choice_door)
                        if check != type(door):
                            raise TypeError
                    except ValueError as ve:
                        print("Please try again.")
                        logging.error("Invalid input type on door, trying again...")
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
                elif choice_door > 5:   #This is the joke result that requires the door section looping, alongside the door mimic.
                    print("You ran into the wall for some reason, bumping your nose against the stones.\n")
                    player.take_damage(1)
                    adventure_log.write("You ran into the wall for some reason, bumping your nose against the stones.\n\n")
                elif abs(choice_door - door) < 2:
                    print("You were bitten by a door mimic!\n")
                    adventure_log.write("You were bitten by a door mimic, but managed to break free from it.\n\n")
                    player.take_damage(3)
                else:       #If you're too far off, it just kills you, again as a joke.
                    print("A pit trap drops you to your doom.  Oh no.\n")
                    adventure_log.write("A pit trap drops you to your doom.  Thus an ignoble end to your tale of adventure, alas not to evil but to pure bad luck.\n\n")
                    quit = False
                    break
            
            if quit != True:
                break

            combat(player, lst_enemies, adventure_log, player_max_hp, diff, infinity)
            

            if player.current_hp != 0:  #Checks if you won or lost, opening up full functionality if you have.
                print("You were victorious, successfully locating the Heart of Darkness, the dreaded artifact haunting the cave!\nYou're pretty sure it's just a very, very moldy onion with an unpleasant smell.\n")
                adventure_log.write("You were victorious, successfully locating the Heart of Darkness, the dreaded artifact haunting the cave!\nYou're pretty sure it's just a very, very moldy onion with an unpleasant smell.\n\n")
                tutorialized = True

            break
        
        quit = True
        #This just collects a list of characters created for each save.
        player_lst.append(player)

        #Weird TypeError glitch earlier, left like this to not have to re-re-rewrite this block.
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

    #Returns all of the used characters before closing the program.    
    print_count = 1
    for elem in player_lst:
        print(str(print_count) + ")" + str(elem))
        print_count += 1
    print("\n")
    return 0

def roll(n):    #Basic die roller essentially for processing of attacks.
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
        xp_threshold = 5 * player.lvl       #Initialize xp_threshold here because leveling up happens at the end of fights.

        #Randomizing which enemy and loading the enemy's information to a new object to not overwrite the originals in the list.
        foe_rng = random.randint(0, (len(lst_enemies) - 1))
        foe = Enemy(lst_enemies[foe_rng].name, lst_enemies[foe_rng].hp, lst_enemies[foe_rng].power, lst_enemies[foe_rng].lvl)
        if infinity:    #For multiple looped battles, levels up the enemy each time.
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

            #The following two are reinstantiated each time to prevent accidentally inflation of values.  Difficulty selection from before decides damage numbers.
            defend = 0
            dmg = player.attack() * diff[1]     #Attack value from object class combined with difficulty modifier.
            while True:
                try:    #Basic player action menu.
                    player_turn = int(input("1) Attack\n2) Defend\n3) Potion\n>>> "))
                    if (player_turn < 0) or (player_turn >3):
                        raise ValueError
                except ValueError as ve:
                    print("Please try again.\n")
                    logging.error("Input error on player turn, trying again...")
                else:
                    break

            match player_turn:
                case 1:
                    if roll(20):    #If you hit, you deal damage, nuff said.
                        foe.take_damage(dmg)
                    else:
                        print("The " + foe.name + " managed to avoid your strike.\n")
                case 2:             #Reduce damage the enemy causes, gets reset each turn obviously.
                    print("You brace yourself for the enemy's attack!\n")
                    defend = dmg
                case 3:             #Healing option based on character's base hp value.
                    print("You chug a potion, trying to heal yourself.  You regain " + str(player.hp) + " hp.\n")
                    player.current_hp += player.hp
                    if player.current_hp > player_max_hp:
                        player.current_hp = player_max_hp
                case default:       #If improper input manages to slip through, saved by this joke response.
                    print("You think too long and too hard, the " + foe.name + " acting during your moment of distraction!\n")

            if foe.current_hp == 0:     #Checks if you've won, removing the need to continue the fight.
                print("You defeated the " + foe.name + "!  Congratulations!\n")
                adventure_log.write("The " + foe.name + " has been defeated!  ")

                #Logs different messages based on the results of the fight before breaking out.
                if player.current_hp >= (player_max_hp / 2):
                    adventure_log.write("It was an easy battle, leaving you ready for more.\n\n")
                elif player.current_hp <= (player_max_hp / 4):
                    adventure_log.write("It was a long, difficult battle, leaving you barely alive.\n\n")
                else:
                    adventure_log.write("You were victorious, though you were not without injury yourself.\n\n")

                break

            foe_dmg = 0     #Reinstantiates the dmg value to be safe.

            if ((turn_count % foe.power) != 0):     #Enemy either attacks or waits
                if roll(20):
                    print("The " + foe.name + " attacks, landing a solid blow.\n")
                    foe_dmg = (foe.attack() * diff[0]) - defend
                    player.take_damage(foe_dmg)
                else:
                    print("The " + foe.name + " attacks, but misses you by a mile.\n")
            else:
                print("The vicious " + foe.name + " takes a moment to prepare itself.\n")

            if (player.current_hp == 0):        #Checks if you were defeated, logging who did it.
                print("You have been struck down by the " + foe.name + "!  Unfortunately, your adventure ends here.\n")
                print(str(foe) + "\n")
                adventure_log.write("You have been struck down by the " + foe.name + "!  Unfortunately, your adventure ends here.\n\n")
                adventure_log.write(str(foe) + "\n\n")
                break

        if infinity == False:       #After battle, checks to see if you're in infinity mode or not before breaking out of the combat loop.
            break
        else:
            if player.current_hp != 0:  #If you win, you go deeper, get experience, heal some, and the battle count goes up, leveling up the enemies.
                print("You proceed deeper into the dark ruins, seeking ever deeper depths.\n\n\n")
                adventure_log.write("You proceed deeper into the dark ruins, seeking ever deeper depths.\n\n")
                if player.lvl < 10:
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


#Loads the list of heroes/enemies from the characters file.  The next two are essentially identical and so will only be explained once.
def load_heroes(fname):
    lst_heroes = []

    with open(fname, "r") as f:     #Opens file of premade entities.

        for line in f:
            info = line.split(',')
            if info[0] == "Hero":   #Parses each line, loading the relevant entities into a list of like characters, either player class options or enemies.
                character = Hero(info[1], info[2], info[3], info[4])
            else:
                character = None

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

            if character != None:
                lst_enemies.append(character)
            
        return lst_enemies


def character_select(choices):
    #Dynamically print character options based on preloaded characters.
    option = 1
    fill = []
    for elem in choices:
        print(str(option) + ")", elem)
        option += 1

    while True:     #Checks user input for errors before loading a custom class copied from one of the preloaded options.
        try:
            decision = int(input(""))
            if decision > len(choices):
                raise ValueError
        except ValueError as ve:
            print("Try again.")
            logging.error("Exceeded list, trying again...")
        else:
            decision -= 1
            player = Hero(choices[decision].name, choices[decision].hp, choices[decision].power, choices[decision].lvl)
            break

    return player



'''
Lore Intro - check
Load characters/enemies - check

Pick Character - check
Optional name change - check

Blade trap - check
Door Puzzle - check
Boss fight - check

Infinite battle mode - check
'''

if __name__ == "__main__":
    main()