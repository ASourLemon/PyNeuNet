from TextDuel.Domain.User import User
from TextDuel.Domain.Duel import Duel


duels = []


def main():

    p0 = User(0, "TorPED0")
    p1 = User(1, "Easts")

    d = Duel(p0, p1)

    user_to_attack = 0
    while True:
        weapon = int(input())
        if weapon == 99:
            break
        d.attack_user(user_to_attack, weapon)
        user_to_attack += 1
        user_to_attack %= 2

    print("Done!")


main()