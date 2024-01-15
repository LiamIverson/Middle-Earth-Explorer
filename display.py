import os
from ascii_magic import AsciiArt

EXAMPLE_RES_PATH = "resources\\ExampleResource.png"

class Display:
    def __init__(self, params: dict):
        self.player = params['player']
        self.display_gui(self.player)
        # self.display_resource(EXAMPLE_RES_PATH)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_gui(self, player):
        self.clear_screen()
        print("##############################")
        print("#      Middle-earth Game     #")
        print("##############################\n")
        print(f"Player: {player.name}")

        if player.location:
            print(f"Location: {player.location.name}")
        else:
            print("Location: Unknown")

        print("------------------------------")
        player.display_inventory()
        print(f"Hunger: {player.hunger}/10\n")

    def display_resource(self, path):
        res = AsciiArt.from_image(path)
        res.to_terminal()

# test=Display({'player' : 'balls'})