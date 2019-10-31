from obswebsocket import obsws, events, requests


class OBSHelper:

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.ws = obsws(self.host, self.port, self.password)

    def change_vlc_source_playlist(self, source_name, playlist):

        self.ws.connect()

        current_scene = self.ws.call(requests.GetCurrentScene())
        sources = current_scene.getSources()

        has_source = False
        for s in sources:
            current_source_name = s["name"]
            if current_source_name == source_name:
                has_source = True
                break

        if has_source:

            source_settings = self.ws.call(requests.GetSourceSettings(source_name))

            new_source_settings = source_settings.getSourcesettings()

            new_playlist = []
            for v in playlist:
                new_playlist.append({"value": v})

            new_source_settings["playlist"] = new_playlist

            self.ws.call(requests.SetSourceSettings(sourceName=source_name, sourceSettings=new_source_settings))

        else:
            print("Current Scene has no Source named '" + source_name + "'")

        self.ws.disconnect()

