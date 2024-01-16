import os
import art
from ascii_magic import AsciiArt

TESTMODE = False

TEST_NUM_COLUMNS = 80
TEST_RES_PATH = "resources\\ExampleResource.png"
TEST_NUM_PLAYER_ATTRIB = 4

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
        Title = art.text2art("Middle Earth Game")
        print(Title)
        # print("##############################".center(CENTER_ALIGN_PADDING))
        # print("#      Middle-earth Game     #".center(CENTER_ALIGN_PADDING),end='')
        # print("PLAYER STATS")
        # print("##############################".center(CENTER_ALIGN_PADDING))

        self.display_resource(TEST_RES_PATH, player)

        print('\n')

        # if player.location:
        #     print(f"Location: {player.location.name}")
        # else:
        #     print("Location: Unknown")

        # print("------------------------------")
        # player.display_inventory()
        # print(f"Hunger: {player.hunger}/10\n")


    def display_resource(self, path: str, player):
        """Converts and displays resource as ASCII art
        Also needs to display everything to the right
        of the ASCII art

        Parameters:
        path (str): Local path to image resource
            SHALL BE 3x2 ASPECT RATIO
        player: Contains player attributes for
            printing stats

        Returns:
        None
        """
        res = AsciiArt.from_image(path)
        numConsoleLines = TEST_NUM_COLUMNS
        ascii_data = res.to_ascii(columns=numConsoleLines, monochrome=True, width_ratio=5.)

        ascii_lines = ascii_data.split('\n')
        
        # Graphics writer function
        numAttributes = TEST_NUM_PLAYER_ATTRIB
        for i in range(len(ascii_lines)):
            # Print all player attributes
            # name
            # location
            # inventory
            # hunger
            # exhaustion
            # strength
            # dexterity
            # intelligence
            if i >= numAttributes:
                print(ascii_lines[i])
            else:
                print(ascii_lines[i],end='')
            if i==0:
                print(f'\t\tName: {player.name}')
            elif i==1:
                print(f'\t\tLocation: {player.location}')
            elif i==2:
                print(f'\t\tInventory: {player.inventory}')
            elif i==3:
                print(f'\t\tHunger: {player.hunger}')

            # elif i==4:
            #     print(ascii_lines[i],end='')
            #     print(f'\t\tExhaustion: {player.exhaustion}')
            # elif i==5:
            #     print(ascii_lines[i],end='')
            #     print(f'\t\tStrength: {player.strength}')
            # elif i==6:
            #     print(ascii_lines[i],end='')
            #     print(f'\t\tDexterity: {player.dexterity}')
            # elif i==7:
            #     print(ascii_lines[i],end='')
            #     print(f'\t\tIntelligence: {player.intelligence}')
            else:
                print(ascii_lines[i])
    

if TESTMODE == True:
    test=Display({'player' : 'balls'})