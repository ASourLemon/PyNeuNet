from TextDuel.Domain.Weapons.DragonScimitar import DragonScimitar
from TextDuel.Domain.Weapons.DragonDagger import DragonDagger


class User:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.weapons = {}
        self.give_weapon(DragonDagger())
        self.give_weapon(DragonScimitar())

    def give_weapon(self, weapon):
        if weapon.id not in self.weapons:
            self.weapons[weapon.id] = weapon

    def get_weapon(self, weapon_id):
        for id in self.weapons:
            weapon = self.weapons[id]
            if weapon.id == weapon_id:
                return weapon
        return None
