import os
import art
from ascii_magic import AsciiArt

TEST_NUM_COLUMNS = 80
TEST_RES_PATH = "resources\\ExampleResource.png"
TEST_NUM_PLAYER_ATTRIB = 4

CENTER_ALIGN_PADDING  = 100

class Display:
    def __init__(self, params: dict):
        if params == {}:
            print('Please pass a proper set of parameters to display API\nMake sure to update player stats before calling')
            return
        self.player_stats = params['player']
        self.display_gui(self.player_stats)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_gui(self, player_stats):
        self.clear_screen()
        Title = art.text2art("MIDDLE EARTH GAME", font='small')
        print(Title, end='')
        print('########################################################\
###############################################################')
        print('\t#\t\t\033[1mPLAYER STATS\033[0;0m'.rjust(108))    # Todo: figure out deterministic relationship for where to put this

        self.display_resource(TEST_RES_PATH, player_stats)
        print('\t\t\t\t\t\t\t\t\t\t\t#\n',end='')
        print('\t\t\t\t\t\t\t\t\t\t\t#')
        print('########################################################\
###############################################################')

        # if player.location:
        #     print(f"Location: {player.location.name}")
        # else:
        #     print("Location: Unknown")

        # print("------------------------------")
        # player.display_inventory()
        # print(f"Hunger: {player.hunger}/10\n")


    def display_resource(self, path: str, player_stats):
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
        ascii_data = res.to_ascii(columns=numConsoleLines, monochrome=True, width_ratio=3.)

        ascii_lines = ascii_data.split('\n')

        # Graphics writer function
        numAttributes = len(player_stats)
        stats = list(player_stats)
        stat_vals = list(player_stats.values())
        
        for i in range(len(ascii_lines)):
            # Print all player attributes in player_stats alongside ASCII art
            print(ascii_lines[i], end='')

            if i >= numAttributes:  # Handle terminating character on lines we don't print stats on
                print('\t#')
            else:
                print(f'\t#\t{stats[i]}: {stat_vals[i]}')