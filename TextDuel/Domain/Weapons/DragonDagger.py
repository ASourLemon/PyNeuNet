import random as rd
from TextDuel.Domain.Weapons.WeaponsCatalog import WeaponsCatalog


class DragonDagger:

    def __init__(self):
        self.id = WeaponsCatalog.DRAGON_DAGGER_ID
        self.max_hit = 20

    def get_hit(self):
        hit0 = rd.randint(0, self.max_hit)
        hit1 = rd.randint(0, self.max_hit)
        return [hit0, hit1]

