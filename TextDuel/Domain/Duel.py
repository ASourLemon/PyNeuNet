

class Duel:

    def __init__(self, user0, user1):
        self.users = {
            user0.id: user0,
            user1.id: user1
        }
        self.hit_points = {
            user0.id: 99,
            user1.id: 99
        }
        print("A duel was created with " + user0.name + " and " + user1.name)

    def damage_user(self, user_id, damage):
        self.hit_points[user_id] -= damage

    def is_user_dead(self, user_id):
        return self.hit_points[user_id] < 1

    def user_won(self, user_id):
        print("User " + self.users[user_id].name + " won the match.")

    def attack_user(self, user_id, weapon_id):
        if user_id in self.users:
            user = self.users[user_id]
            if weapon_id in user.weapons:
                weapon = user.get_weapon(weapon_id)
                hits = weapon.get_hit()
                total_damage = 0
                text = ""
                for hit in hits:
                    total_damage += hit
                    text += " " + str(hit)

                for id in self.users:
                    if id != user_id:
                        self.damage_user(id, total_damage)
                        print(user.name + " hitted" + text + " on " + self.users[id].name)

                        if self.is_user_dead(id):
                            self.user_won(user_id)

                        break
            else:
                print("User " + str(user_id) + " does not own a " + str(weapon_id))
        else:
            print("User " + str(user_id) + " does not exist in this duel.")

