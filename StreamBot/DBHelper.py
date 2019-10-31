import os
import sqlite3


class DBHelper:

    def __init__(self, db_name):
        self.db_name = db_name
        if not os.path.isfile(db_name):
            self.create_db()
            self.populate_db()

    def create_db(self):
        conn = sqlite3.connect(self.db_name)

        c = conn.cursor()

        c.execute('''CREATE TABLE 
        origin (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL UNIQUE
        )''')
        #
        c.execute('''CREATE TABLE 
        performer (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL UNIQUE
        )''')
        #
        c.execute('''CREATE TABLE 
        games (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL UNIQUE, 
        twitch_name TEXT NOT NULL UNIQUE, 
        performer INTEGER,
        origin INTEGER,
        play_time INTEGER NOT NULL, 
        local_path TEXT NOT NULL UNIQUE,
        FOREIGN KEY(performer) REFERENCES performer(id),
        FOREIGN KEY(origin) REFERENCES origin(id)
        )''')

        conn.commit()
        conn.close()

    def populate_db(self):
        conn = sqlite3.connect(self.db_name)

        c = conn.cursor()

        # Origins
        c.execute("INSERT INTO origin "
                  "(name) VALUES "
                  "('World of Longplays')")
        #
        c.execute("INSERT INTO origin "
                  "(name) VALUES "
                  "('Network')")

        # Performers
        c.execute("INSERT INTO performer "
                  "(name) VALUES "
                  "('Spazbo4')")
        #
        c.execute("INSERT INTO performer "
                  "(name) VALUES "
                  "('Lucipher.')")


        # Games
        c.execute("INSERT INTO games "
                  "(name, twitch_name, performer, origin, play_time, local_path) VALUES "
                  "('MediEvil', 'Medievil', 2, 2, 5188, 'D:\\Videos\\Misc\\PS1\\MediEvil_0.flv')")
        #
        c.execute("INSERT INTO games "
                  "(name, twitch_name, performer, origin, play_time, local_path) VALUES "
                  "('Resident Evil 3: Nemesis', 'Resident Evil 3: Nemesis', 1, 1, 10748, 'D:\\Videos\\Misc\\PS1\\PSX_Longplay_037_Resident_Evil_3_Nemesis.mp4')")

        conn.commit()
        conn.close()

    def get_games(self):
        conn = sqlite3.connect(self.db_name)

        c = conn.cursor()
        rows = c.execute("SELECT * FROM games ORDER BY id").fetchall()

        conn.close()

        return rows
