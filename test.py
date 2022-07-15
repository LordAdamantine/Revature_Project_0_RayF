from entities import Entity, Hero
import unittest

class TestHero(unittest.TestCase):
    def test_attack(self):
        p1 = Hero("Dummy", 10, 10, 5)
        self.assertEqual(p1.attack(), 10)

    def test_take_damage(self):
        p1 = Hero("Dummy", 10, 10, 5)
        p1.take_damage(7)
        self.assertEqual(p1.hp, 3)
        p1.take_damage(5)
        self.assertEqual(p1.hp, 0)

    def test_name(self):
        p1 = Hero("Dummy", 10, 10, 5)
        p1.changeName()
        self.assertEqual(p1.name, "Player")

    def test_lvlUp(self):
        p1 = Hero("Dummy", 10, 10, 5)
        p1.lvlUp()
        self.assertEqual(p1.lvl, 6)
        p1.lvlUp()
        self.assertEqual(p1.lvl, 7)
        p1.lvlUp()
        self.assertEqual(p1.lvl, 8)
        p1.lvlUp()
        self.assertEqual(p1.lvl, 9)
        p1.lvlUp()
        self.assertEqual(p1.lvl, 10)
        p1.lvlUp()
        self.assertEqual(p1.lvl, 10)

if __name__ == '__main__':
    unittest.main()