import random as rd
from TextDuel.Domain.Weapons.WeaponsCatalog import WeaponsCatalog

class DragonScimitar:

    def __init__(self):
        self.id = WeaponsCatalog.DRAGON_SCIMITAR_ID
        self.max_hit = 35

    def get_hit(self):
        return [rd.randint(0, self.max_hit)]
        self.base_hit = 20

    def get_hit(self):
        return [rd.randint(-1, 1) + self.base_hit]

