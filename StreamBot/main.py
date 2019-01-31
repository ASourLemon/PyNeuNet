import sys
import time
import json

import logging
from StreamBot.OBSHelper import OBSHelper

logging.basicConfig(level=logging.INFO)
sys.path.append('../')

host = "localhost"
port = 4444
password = "secret"





def main():




    new_playlist = ["D:\\"]

    osbh = OBSHelper(host, port, password)

    osbh.change_vlc_source_playlist("VLC Video Source", new_playlist)


    print("Done!")



main()