import random

class entity:
    def __init__(self, name, hp):
        self.name = str(name)
        self.hp = int(hp)
        if self.hp < 1:
            self.hp = 0
    def damage(self, damage):
        self.hp -= damage

class character(entity):
    def defeat(self):
        print("You are defeated!")

class enemy(entity):
    def defeat(self):
        print("You are victorious!")


