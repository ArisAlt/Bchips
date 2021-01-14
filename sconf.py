import configparser
import json

class Settings:
    def __init__(self, file = "settings.ini"):
        self.file = file
        self.screen = "screen.json"

    def read(self, section, parameter):
        config = configparser.ConfigParser()
        config.read(self.file)
        value = config[section][parameter]
        return value

    def read_screen_area(self):
        area = {"top": 0, "left": 0, "width": 0, "height": 0}
        with open(self.screen, mode="r") as file:
            config = json.load(file)
            area["top"] = config["top"]
            area["left"] = config["left"]
            area["width"] = config["width"]
            area["height"] = config["height"]
        return area

if __name__ == "__main__":
   print(Settings().read_screen_area().get("top"))
