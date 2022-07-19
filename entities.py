import logging
import re

class Entity:
    logging.basicConfig(filename = "game.log", level = logging.DEBUG, format = '%(asctime)s :: %(message)s')
    def __init__(self, name, hp, power, lvl):
        self.name = name
        self.hp = int(hp)
        self.power = int(power)
        self.lvl = int(lvl)
        self.current_hp = self.hp * self.lvl

    def attack(self):
        return int(self.power * self.lvl)

    def __str__(self):
        return "Name: " + str(self.name) + ", hp: " + str(self.current_hp) + ", Power: " + str(self.power) + ", Level: " + str(self.lvl)

    def take_damage(self, dmg):
        if dmg <= 0:
            print(self.name, "deflected the attack!")
        else:
            print(self.name, "took", dmg, "damage!\n")
            self.current_hp -= dmg
        if self.current_hp <0:
            self.current_hp = 0

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
        self.name = name

    def lvlUp(self):
        if self.lvl <10:
            self.lvl += 1
            self.power += 2

class Enemy(Entity):
    pass
    def lvlUp(self):
        if self.lvl <15:
            self.lvl += 1
            self.power += 1
