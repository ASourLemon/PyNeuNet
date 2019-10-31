import sys
import time
import json

import logging

from StreamBot.OBSHelper import OBSHelper
from StreamBot.DBHelper import DBHelper


logging.basicConfig(level=logging.INFO)
sys.path.append('../')

host = "localhost"
port = 4444
password = "secret"

db_local = "data//games.db"


def main():

    db = DBHelper(db_local)
    games = db.get_games()

    osbh = OBSHelper(host, port, password)

    while True:
        for g in games:

            name = g[1]
            twitch_name = g[2]
            performer_id = g[3]
            origin_id = g[4]
            play_time = int(g[5])
            local_path = g[6]

            new_playlist = [local_path]
            osbh.change_vlc_source_playlist("VLC Video Source", new_playlist)

            print("Now playing " + name + " for " + str(play_time) + " seconds.")
            time.sleep(play_time)




    print("Done!")



main()