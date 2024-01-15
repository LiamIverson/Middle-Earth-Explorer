import os
import sys
from ascii_magic import AsciiArt

TESTMODE = False

TEST_NUM_COLUMNS = 80
TEST_RES_PATH = "resources\\ExampleResource.png"

CENTER_ALIGN_PADDING  = 100

class Display:
    def __init__(self, params: dict):
        if TESTMODE == False:
            self.player = params['player']
            self.display_gui(self.player)
        else:
            self.display_resource(TEST_RES_PATH)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_gui(self, player):
        self.clear_screen()
        print("##############################".center(CENTER_ALIGN_PADDING))
        print("#      Middle-earth Game     #".center(CENTER_ALIGN_PADDING))
        print("##############################".center(CENTER_ALIGN_PADDING))
        print('\n')
        self.display_resource(TEST_RES_PATH)

        print(f"\n\n\nPlayer: {player.name}")

        # if player.location:
        #     print(f"Location: {player.location.name}")
        # else:
        #     print("Location: Unknown")

        # print("------------------------------")
        # player.display_inventory()
        # print(f"Hunger: {player.hunger}/10\n")


    def display_resource(self, path: str):
        """Converts and displays resource as ASCII art

        Parameters:
        path (str): Local path to image resource
            SHALL BE 3x2 ASPECT RATIO

        Returns:
        None
        """
        res = AsciiArt.from_image(path)
        numConsoleLines = TEST_NUM_COLUMNS
        ascii_data = res.to_ascii(columns=numConsoleLines, monochrome=True)

        ascii_lines = ascii_data.split('\n')
        
        # Graphics writer function
        for i in range(len(ascii_lines)):
            
            if i==1:
                print(ascii_lines[i],end='')
                print(f'\t\t INSERT STATS PRINTOUT HERE')
            else:
                print(ascii_lines[i])
    

if TESTMODE == True:
    test=Display({'player' : 'balls'})