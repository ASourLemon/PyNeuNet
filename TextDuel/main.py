from TextDuel.Domain.User import User
from TextDuel.Domain.Duel import Duel



duels = []


def main():



    p0 = User(0, "TOrpedo")
    p1 = User(1, "Easts")

    d = Duel(p0, p1)
    d.attack_user(0, 0)
    d.attack_user(0, 0)
    d.attack_user(0, 0)
    d.attack_user(0, 1)
    d.attack_user(0, 1)
    d.use_weapon(0, 0)



    print("Done!")

main()