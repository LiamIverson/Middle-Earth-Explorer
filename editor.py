import curses
import pickle


from location import Location
from building import Building
from npc import NPC

location = None
npc = None


def save_location(location, filename):
    with open(filename, 'wb') as file:
        pickle.dump(location, file)


def draw_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = "Editor Menu"
    stdscr.addstr(0, w//2 - len(title)//2, title)

    # Display current location attributes
    if location:
        stdscr.addstr(2, 2, "Current Location Attributes:")
        stdscr.addstr(3, 4, f"Name: {location.name}")
        stdscr.addstr(4, 4, f"Description: {location.description}")
        stdscr.addstr(5, 4, f"Is Town: {location.is_town}")
        stdscr.addstr(6, 4, f"Buildings: {location.buildings}")
        stdscr.addstr(7, 4, f"Town: {location.town}")
    else:
        stdscr.addstr(2, 2, "No location created yet.")

    menu_items = ["Create Location", "Create Enemy", "Exit"]
    for idx, item in enumerate(menu_items):
        x = w//2 - len(item)//2
        y = h//2 - len(menu_items)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, item)

    stdscr.refresh()
def create_location(stdscr):
    global location
    in_menu = True

    while in_menu:
        if location is None:
            location = Location("", "")

        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Create Location"
        stdscr.addstr(0, w//2 - len(title)//2, title)

        # Display current location attributes
        stdscr.addstr(2, 2, "Current Location Attributes:")
        stdscr.addstr(3, 4, f"Name: {location.name}")
        stdscr.addstr(4, 4, f"Description: {location.description}")
        stdscr.addstr(5, 4, f"Is Town: {location.is_town}")
        stdscr.addstr(6, 4, f"Buildings: {location.buildings}")
        stdscr.addstr(7, 4, f"Town: {location.town}")

        stdscr.addstr(9, 2, "Select an attribute to edit (Press Enter to confirm):")

        attributes = ["Name", "Description", "Is Town", "Buildings", "Town", "Save", "Exit"]
        current_attribute_idx = 0

        while True:
            for idx, attribute in enumerate(attributes):
                x = 4
                y = 11 + idx
                if idx == current_attribute_idx:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, attribute)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, attribute)

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_attribute_idx > 0:
                current_attribute_idx -= 1
            elif key == curses.KEY_DOWN and current_attribute_idx < len(attributes) - 1:
                current_attribute_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_attribute_idx == 0:
                    stdscr.addstr(19, 2, "Enter name:")
                    stdscr.refresh()
                    location.name = ""
                    while True:
                        key = stdscr.getch()
                        if key == 10:  # Enter key
                            break
                        elif key == 127:  # Backspace key
                            location.name = location.name[:-1]
                        else:
                            location.name += chr(key)
                        stdscr.addstr(20, 2, location.name.ljust(20))  # Display input text
                        stdscr.refresh()
                elif current_attribute_idx == 1:
                    stdscr.addstr(19, 2, "Enter description:")
                    stdscr.refresh()
                    location.description = ""
                    while True:
                        key = stdscr.getch()
                        if key == 10:  # Enter key
                            break
                        elif key == 127:  # Backspace key
                            location.description = location.description[:-1]
                        else:
                            location.description += chr(key)
                        stdscr.addstr(20, 2, location.description.ljust(60))  # Display input text
                        stdscr.refresh()
                elif current_attribute_idx == 2:
                    stdscr.addstr(19, 2, "Is town (True/False) Press Enter:")
                    stdscr.refresh()
                    is_town_input = stdscr.getstr(20, 2, 5).decode(encoding="utf-8").lower()
                    stdscr.addstr(21, 2, f"You entered: {is_town_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    location.is_town = is_town_input.strip().lower() == "t"
                
                elif current_attribute_idx == 3:
                    stdscr.addstr(19, 2, "Enter buildings (comma-separated list):")
                    stdscr.refresh()
                    buildings_input = ""
                    while True:
                        stdscr.addstr(20, 2, buildings_input)
                        stdscr.refresh()
                        key = stdscr.getch()
                        if key == curses.KEY_ENTER or key in [10, 13]:
                            break
                        elif key == curses.KEY_BACKSPACE:
                            buildings_input = buildings_input[:-1]
                        else:
                            buildings_input += chr(key)
                    building_names = buildings_input.split(",")
                    location.buildings = []
                    for name in building_names:
                        location.buildings.append(Building(name, "","",[]))  # Assuming Building is the class for building objects with a name and description attribute


                elif current_attribute_idx == 4:
                    stdscr.addstr(19, 2, "Enter town (comma-separated list):")
                    stdscr.refresh()
                    town_input = stdscr.getstr(20, 2, 60).decode(encoding="utf-8")
                    location.town = town_input.split(",")
                elif current_attribute_idx == 5:
                    stdscr.addstr(19, 2, "Enter name:")
                    stdscr.refresh()
                    file_name = ""
                    while True:
                        key = stdscr.getch()
                        if key == 10:  # Enter key
                            break
                        elif key == 127:  # Backspace key
                            file_name = file_name[:-1]
                        else:
                            file_name += chr(key)
                        stdscr.addstr(20, 2, file_name.ljust(20))  # Display input text
                        stdscr.refresh()
                    save_location(location, file_name+".pkl")
                elif current_attribute_idx == 6:
                    in_menu = False

                stdscr.clear()
                break

def create_enemy(stdscr):
    global npc
    in_menu = True

    while in_menu:
        # Todo: Figure out how to properly initialize the NPC object
        if npc is None:
            #npc = NPC(None, None, None, None, None, None, None, None)
            npc=NPC("", "", None, 0, 0, 0, '', False, 0, [], [], [])

        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Create Enemy"
        stdscr.addstr(0, w//2 - len(title)//2, title)

        # Display current enemy attributes
        stdscr.addstr(2, 2, "Current Enemy Attributes:")
        stdscr.addstr(3, 4, f"Name: {npc.name}")
        stdscr.addstr(4, 4, f"Description: {npc.description}")
        stdscr.addstr(5, 4, f"Strength: {npc.strength}")
        stdscr.addstr(6, 4, f"Dexterity: {npc.dexterity}")
        stdscr.addstr(7, 4, f"Intelligence: {npc.intelligence}")
        stdscr.addstr(8, 4, f"NPC Type: {npc.npc_type}")
        stdscr.addstr(8, 4, f"Hostile?: {npc.hostile}") # Is this boolean?  What type is this expected to be?
        stdscr.addstr(9, 4, f"Dialog: {npc.dialog}")
        stdscr.addstr(10, 4, f"Rumors: {npc.rumors}")
        stdscr.addstr(11, 4, f"Room Rate: {npc.room_rate}")
        stdscr.addstr(12, 4, f"Goods: {npc.goods}")
        stdscr.addstr(13, 4, f"Dialog Trees: {npc.dialog_trees}")

        stdscr.addstr(15, 2, "Select an attribute to edit (Press Enter to confirm):")

        attributes = ["Name", "Description", "Strength", "Dexterity", "Intelligence", "NPC Type", "Hostility", "Dialog", "Rumors", "Room Rate", "Goods", "Dialog Trees", "Save", "Exit"]
        current_attribute_idx = 0

        while True:
            for idx, attribute in enumerate(attributes):
                x = 4
                y = 17 + idx
                if idx == current_attribute_idx:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, attribute)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, attribute)

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_attribute_idx > 0:
                current_attribute_idx -= 1
            elif key == curses.KEY_DOWN and current_attribute_idx < len(attributes) - 1:
                current_attribute_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_attribute_idx == 0:
                    stdscr.addstr(32, 2, "Enter name:")
                    stdscr.refresh()
                    npc.name = ""
                    while True:
                        key = stdscr.getch()
                        if key == 10:  # Enter key
                            break
                        elif key == 127:  # Backspace key
                            npc.name = npc.name[:-1]
                        else:
                            npc.name += chr(key)
                        stdscr.addstr(33, 2, npc.name.ljust(20))  # Display input text
                        stdscr.refresh()
                elif current_attribute_idx == 1:
                    stdscr.addstr(32, 2, "Enter description:")
                    stdscr.refresh()
                    npc.description = ""
                    while True:
                        key = stdscr.getch()
                        if key == 10:  # Enter key
                            break
                        elif key == 127:  # Backspace key
                            npc.description = npc.description[:-1]
                        else:
                            npc.description += chr(key)
                        stdscr.addstr(33, 2, npc.description.ljust(60))  # Display input text
                        stdscr.refresh()
                elif current_attribute_idx == 2:
                    stdscr.addstr(32, 2, "Enter enemy strength:")
                    stdscr.refresh()
                    strength_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
                    stdscr.addstr(34, 2, f"You entered: {strength_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.strength = strength_input.strip()
                
                elif current_attribute_idx == 3:
                    stdscr.addstr(32, 2, "Enter enemy dexterity:")
                    stdscr.refresh()
                    dexterity_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
                    stdscr.addstr(34, 2, f"You entered: {dexterity_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.dexterity = dexterity_input.strip()


                elif current_attribute_idx == 4:
                    stdscr.addstr(32, 2, "Enter enemy intelligence:")
                    stdscr.refresh()
                    intelligence_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
                    stdscr.addstr(34, 2, f"You entered: {intelligence_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.intelligence = intelligence_input.strip()

                elif current_attribute_idx == 5:
                    stdscr.addstr(32, 2, "Enter enemy NPC Type:")
                    stdscr.refresh()
                    npc_type_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
                    stdscr.addstr(34, 2, f"You entered: {npc_type_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.npc_type = npc_type_input.strip()

                elif current_attribute_idx == 6:
                    stdscr.addstr(32, 2, "Enter enemy hostility:")
                    stdscr.refresh()
                    try:
                        hostility_input = int(stdscr.getstr(33, 2, 5).decode(encoding="utf-8"))
                        stdscr.addstr(34, 2, f"You entered: {hostility_input}")
                    except TypeError:
                        stdscr.addstr(34, 2, f"Please enter a valid integer input")
                        continue
                    
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.hostile = hostility_input.strip()
                
                elif current_attribute_idx == 7:
                    stdscr.addstr(32, 2, "Enter enemy dialog as ~ delimited strings:")
                    stdscr.refresh()
                    try:
                        dialog_input = list(stdscr.getstr(33, 2, 320).decode(encoding="utf-8").split('~'))
                        stdscr.addstr(34, 2, f"Parsed dialog input: {dialog_input}")
                    except TypeError:
                        stdscr.addstr(34, 2, f"Unable to parse dialog entered")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.dialog = dialog_input

                elif current_attribute_idx == 8:
                    stdscr.addstr(32, 2, "Enter enemy rumors as ~ delimited strings (keep it appropriate):")
                    stdscr.refresh()
                    rumors_input = list(stdscr.getstr(33, 2, 320).decode(encoding="utf-8").split('~'))
                    stdscr.addstr(34, 2, f"You entered: {rumors_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.rumors = rumors_input

                elif current_attribute_idx == 9:
                    stdscr.addstr(32, 2, "Enter enemy room rate:")
                    stdscr.refresh()
                    try:
                        room_rate_input = int(stdscr.getstr(33, 2, 5).decode(encoding="utf-8"))
                        stdscr.addstr(34, 2, f"You entered: {room_rate_input}")
                    except TypeError:
                        stdscr.addstr(34, 2, f"Please enter integer value")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.room_rate = room_rate_input
                
                elif current_attribute_idx == 10:
                    stdscr.addstr(32, 2, "Enter enemy default goods, delimited by ~:")
                    stdscr.refresh()
                    goods_input = stdscr.getstr(33, 2, 128).decode(encoding="utf-8").split('~')
                    stdscr.addstr(34, 2, f"You entered: {goods_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.goods = goods_input

                elif current_attribute_idx == 11:
                    stdscr.addstr(32, 2, "Enter enemy dialog trees:")
                    stdscr.refresh()
                    dialog_trees_input = stdscr.getstr(33, 2, 320).decode(encoding="utf-8").lower()
                    stdscr.addstr(34, 2, f"You entered: {dialog_trees_input}")
                    stdscr.refresh()
                    stdscr.getstr()
                    npc.dialog_trees = dialog_trees_input

                elif current_attribute_idx == 12:
                    stdscr.addstr(32, 2, "Enter save name for enemy:")
                    stdscr.refresh()
                    file_name = ""
                    while True:
                        key = stdscr.getch()
                        if key == 10:  # Enter key
                            break
                        elif key == 127:  # Backspace key
                            file_name = file_name[:-1]
                        else:
                            file_name += chr(key)
                        stdscr.addstr(34, 2, file_name.ljust(20))  # Display input text
                        stdscr.refresh()
                    save_location(npc, file_name+".pkl")
                elif current_attribute_idx == 13:
                    in_menu = False

                stdscr.clear()
                break

def main(stdscr):
    global location
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    stdscr.clear()
    stdscr.refresh()

    current_row = 0

    while True:
        draw_menu(stdscr, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < 2:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                create_location(stdscr)
            elif current_row == 1:
                create_enemy(stdscr)
            elif current_row == 2:
                break

curses.wrapper(main)
