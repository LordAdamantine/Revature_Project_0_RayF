import random
import logging
from entities import Entity, Hero, Enemy
#adventure_log.write()

def main():
    logging.basicConfig(filename = "game.log", level = logging.DEBUG, format = '%(asctime)s :: %(message)s')

    lore = open('lore.txt', 'r')
    adventure_log = open('Your Adventure.txt', 'w')
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

    while True:

        #Character creation
        while True:
            print("Select your class:\n")
            player = None
            player = character_select(lst_heroes)
            if player != None:
                break
    
        adventure_log.write("Your courageous " + player.name + " has entered the dungeon!\n")
        print("\n")
        player.changeName()
        adventure_log.write(player.name + " prepares themselves for whatever may come.")
        print("\n")

        #blade trap
        blade = random.randint(1, 2)
        print("You hear a blade coming from behind!")
        adventure_log.write("You hear a blade coming from behind!")

        choice_blade = str(input("Do you 1)jump or 2)duck?  >>"))
        print("\n")
        if choice_blade == "1":
            if choice_blade == blade:
                print("You accidentally jumped into the path of the blade, taking 5 damage.", "\n")
                adventure_log.write("You accidentally jumped into the path of the blade, taking 5 damage.")
                player.take_damage(5)
            else:
                print("You manage to jump out of the way, avoiding damage.", "\n")
                adventure_log.write("You manage to jump out of the way, avoiding damage.")
        elif choice_blade == "2":
            if choice_blade == blade:
                print("You duck down...into the path of the blade!", "\n")
                adventure_log.write("You duck down...into the path of the blade!")
                player.take_damage(5)
            else:
                print("You manage to duck out of the way, avoiding damage.", "\n")
                adventure_log.write("You manage to duck out of the way, avoiding damage.")
        else:
            print("Stricken by indecision, you just stand there.")
            adventure_log.write("Stricken by indecision, you just stand there.")
            player.take_damage(5)

        
        status(player)

        #door puzzle

        #combat method
        foe = None
        if player.hp == 0:
            input("Oh no, you were killed by " + foe.name + ". Would you like to try again?")

        break


    adventure_log.close()

    return 0

def status(player):
    print((str(player.name) + " HP: " + str(player.hp)))
    print("\n")

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
    
def character_select(choices):
    while True:
        option = 1
        for elem in choices:
            print(str(option) + ")", elem)
            option += 1

        #implement try/except block
        decision = int(input(""))
        if decision > len(choices):
            print("Please try again.\n")
        else:
            decision -= 1
            player = choices[decision]
            break
    #print("\n")
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