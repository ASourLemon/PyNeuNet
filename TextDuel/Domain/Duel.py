

class Duel:

    def __init__(self, user0, user1):
        self.users = {
            user0.id: user0,
            user1.id: user1
        }
        self.user0_hit_points = 99
        self.user1_hit_points = 99
        print("A duel was created with " + user0.name + " and " + user1.name)

    def use_weapon(self, user_id, weapon_id):
        if user_id in self.users:
            user = self.users[user_id]
            if weapon_id in user.weapons:
                weapon = user.get_weapon(weapon_id)
                hits = weapon.get_hit()
                s = ""
                for hit in hits:
                    s += " " + str(hit)
                print(user.name + " hitted" + s + ".")
            else:
                print("User " + str(user_id) + " does not own a " + str(weapon_id))
        else:
            print("User " + str(user_id) + " does not exist in this duel.")
