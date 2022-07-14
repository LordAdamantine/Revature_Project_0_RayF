
    #You enter a long hallway, and suddenly hear a blade coming from behind.  Do you: duck or jump?
    #One kills you, the other is a success.

    #You reach 5 doors, only one leads to safe passage.
    #Solve a randomly generated math problem to proceed.

    #You face the boss, attacking or defending each turn until it is dead.
    #One weapon does double damage.
import random
from entities import entity, enemy, character

def main():
    print("\n")

    blade = random.randint(0, 1)
    #blade = 1
    print("You hear a blade coming from behind!  Do you duck or jump?")

    #some user input, filler for now
    choice_blade = random.randint(0, 1)
    #choice_blade = 0

    if choice_blade == 0:
        print("You duck!")
    else:
        print("You jump!")
    if choice_blade != blade:
        print("You live!", "\n")
    else:
        print("You die!", "\n")
        return 0

    door = random.randint(1, 5)
    #door = 1
    print("You approach a door with a riddle:")
    match door:
        case 1:
            print("What is 0! equal to?")
        case 2:
            print("What can be as lonely as one?")
        case 3:
            print("What is a crowd?")
        case 4:
            print("Where___ art thou?")
        case 5:
            print("I've run out of riddles, just take the last door.")

    #again, input
    choice_door = random.randint(1, 5)
    #choice_door = 1
    print("You pick door number " + str(choice_door) + "!")

    if choice_door == door:
        print("Onward, to battle!", "\n")
    elif choice_door > 5:
        print("You ran into the wall for some reason, dying on impact.", "\n")
        return 0
    elif abs(choice_door - door) < 2:
        print("You were eaten by a door mimic.", "\n")
        return 0
    else:
        print("A pit trap drops you to your doom.", "\n")
        return 0

    print("You come upon the boss!", "\n")

    player = character("Name", 10)
    boss = enemy("Name", 20)
    weakness = random.randint(1, 3)
    #weakness = 2

    while (True):
        #some form of input to pick weapon
        weapon = 1
        attack = random.randint(3, 5)
        if weapon == weakness:
            attack *= 2
        print("You deal", attack, "damage!", "\n")
        boss.damage(attack)

        if boss.hp < 0:
            boss.defeat()
            break

        hit1 = random.randint(1, 2)
        hit2 = random.randint(1, 2)
        if hit1 == hit2:
            cattack = random.randint(3, 5)
            print("You take", cattack, "damage!  Ouch!", "\n")
            player.damage(cattack)
        else:
            print("You avoided their blow.", "\n")

        if player.hp < 1:
            player.defeat()
            break

main()
