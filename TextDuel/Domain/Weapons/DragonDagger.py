import random as rd
from TextDuel.Domain.Weapons.WeaponsCatalog import WeaponsCatalog


class DragonDagger:

    def __init__(self):
        self.id = WeaponsCatalog.DRAGON_DAGGER_ID
        self.base_hit = 15

    def get_hit(self):
        hit0 = rd.randint(-1, 1) + self.base_hit
        hit1 = rd.randint(-1, 1) + self.base_hit
        return [hit0, hit1]

