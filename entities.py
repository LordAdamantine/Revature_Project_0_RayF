import logging
import re

class Entity:
    logging.basicConfig(filename = "game.log", level = logging.DEBUG, format = '%(asctime)s :: %(message)s')
    def __init__(self, name, hp, power, lvl):
        self.name = name
        self.hp = hp
        self.power = power
        self.lvl = lvl

    def attack(self):
        return self.power

    def __str__(self):
        return "Name: " + str(self.name) + ", hp: " + str(self.hp) + ", Power: " + str(self.power) + ", Level: " + str(self.lvl)

class Hero(Entity):
    def changeName(self):
        #implement try/except block
        while True:
            try:
                name = input("What's your character's name?\n")
                check = re.search(",", name)
                if check != None:
                    raise ValueError
            except ValueError as ve:
                print("Warning, improper input, commas detected.")
                logging.error("Attempted illegal comma in name, trying again...")
            else:
                break
        self.name=name

    def lvlUp(self):
        if self.lvl <10:
            self.lvl += 1
            self.power += 2
            self.hp += 5

    def take_damage(self, dmg):
        if dmg == 0:
            print(self.name, "deflected the attack!")
        else:
            print(self.name, "took", dmg, "damage!")
        self.hp -= dmg
        if self.hp <0:
            self.hp = 0

class Enemy(Entity):
    def lvlUp(self):
        if self.lvl <15:
            self.lvl += 1
            self.power += 1
            self.hp += 1

    def take_damage(self, dmg):
        print(self.name, "took", dmg, "damage!")
        self.hp -= dmg
        if self.hp <0:
            self.hp = 0
