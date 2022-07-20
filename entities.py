import logging
import re

class Entity:   #Superclass for the heroes and enemies I will create
    logging.basicConfig(filename = "game.log", level = logging.DEBUG, format = '%(asctime)s :: %(message)s')
    def __init__(self, name, hp, power, lvl):
        self.name = name
        self.hp = int(hp)
        self.power = int(power)
        self.lvl = int(lvl)
        #Not all values related to the class are taken directly from file, some are calculated on instantiation from given data.
        self.current_hp = self.hp * self.lvl

    def attack(self):       #Similar to the above, except it's to return a specific value instead of holding onto a changing value.
        return int(self.power * self.lvl)

    def __str__(self):      #Formats the appearance of the string representation of the classes.
        return "Name: " + str(self.name) + ", hp: " + str(self.current_hp) + ", Power: " + str(self.power) + ", Level: " + str(self.lvl)

    def take_damage(self, dmg):     #Current hp and damaging it is handled inside the superclass since everything takes damage.
        if dmg <= 0:
            print(self.name, "deflected the attack!")   #Uses the later implemented defense calculation.
        else:
            print(self.name, "took", dmg, "damage!\n")
            self.current_hp -= dmg
        if self.current_hp <0:      #To make sure the hp never goes negative.
            self.current_hp = 0

class Hero(Entity):
    def changeName(self):
        while True:
            try:        #Basic input checking try/except block to prevent commas from being entered.
                name = input("What's your character's name?\n")
                check = re.search(",", name)
                if check != None:
                    raise ValueError
            except ValueError as ve:
                print("Warning, improper input, commas detected.")
                logging.error("Attempted illegal comma in name, trying again...")
            else:
                break
        self.name = name

    def lvlUp(self):    #Players level up differently from monsters.
        if self.lvl <10:
            self.lvl += 1
            self.power += 2

class Enemy(Entity):
    pass
    def lvlUp(self):    #Monsters gain less power per level up but can level up more times, allowing for the monsters to outscale the players and kill them.
        if self.lvl <15:
            self.lvl += 1
            self.power += 1
