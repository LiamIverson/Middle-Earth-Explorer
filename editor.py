import curses
import curses.textpad
import pickle
import os
import time

from location import Location
from building import Building
from npc import NPC

location = None
npc = None
building = None

MAX_STR_INPUT_CHARS = 320

def save_pkl(mode: str, obj_to_save: any, filename: str):
    folder = f'{mode}s'
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(f'{folder}/{filename}', 'wb') as file:
        pickle.dump(obj_to_save, file)

def save_handler(mode: str, stdscr: any, obj_to_save: any):
    """
    Mode shall be one of the following:
    - building
    - location
    - npc
    """
    try:
        stdscr.addstr(35, 2, f"Enter save name for {mode}:")
    except:
        pass
    stdscr.refresh()
    save_name = ""
    curses.echo()
    save_name = stdscr.getstr(36, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8")
    stdscr.refresh()
    stdscr.move(35,2)
    stdscr.deleteln()
    stdscr.addstr(35, 2, f"Saving {mode} as: {save_name}.pkl")
    
    stdscr.refresh()
    time.sleep(1)
    save_pkl(mode, obj_to_save, save_name+".pkl")

def get_y_pos(stdscr: any) -> int:
    return int(stdscr.getyx()[0])

def modify_attributes(mode: str, attributes: list, stdscr: any):
    current_attribute_idx = 0
    y_initial_pos = stdscr.getyx()[0]
    while True:
        
        for idx, attribute in enumerate(attributes):
            x = 4
            y = y_initial_pos + 1 + idx
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
            if mode == 'location':
                in_menu = location_attribute_modifier(current_attribute_idx, stdscr)
                return in_menu
            elif mode == 'npc':
                in_menu = npc_attribute_modifier(current_attribute_idx, stdscr)
                return in_menu
            elif mode == 'building':
                in_menu = building_attribute_modifier(current_attribute_idx, stdscr)
                return in_menu
            


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
        stdscr.addstr(7, 4, f"Connections: {location.connections}")
        stdscr.addstr(8, 4, f"Overworld Coords: {location.overworld_cords}")
        stdscr.addstr(9,4, f"Encounters: {location.encounters}")
    else:
        stdscr.addstr(2, 2, "No location created yet.")

    menu_items = ["Create Location", "Create Enemy", "Create Building", "Exit"]
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
        stdscr.addstr(7, 4, f"Connections: {location.connections}")
        stdscr.addstr(8, 4, f"Overworld Coords: {location.overworld_cords}")
        stdscr.addstr(9,4, f"Encounters: {location.encounters}")

        stdscr.addstr(11,2, "Select an attribute to edit (Press Enter to confirm):")

        attributes = ["Name", "Description", "Is Town", "Buildings", "Save", "Connections","Overworld Coords", "Encounters", "Exit"]
        

        in_menu = modify_attributes('location',  attributes, stdscr)

        
                
def create_enemy(stdscr):
    global npc
    in_menu = True

    while in_menu:
        # Todo: Figure out how to properly initialize the NPC object
        if npc is None:
            #npc = NPC(None, None, None, None, None, None, None, None)
            npc=NPC("", "", None, 0, 0, 0, 0, 0, '', False, 0, [], [], [])

        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Create Enemy"
        stdscr.addstr(0, w//2 - len(title)//2, title)

        # Display current enemy attributes
        try:
            stdscr.addstr(2, 2, "Current Enemy Attributes:")
            stdscr.addstr(3, 4, f"Name: {npc.name}")
            stdscr.addstr(4, 4, f"Description: {npc.description}")
            stdscr.addstr(5, 4, f"Strength: {npc.strength}")
            stdscr.addstr(6, 4, f"Dexterity: {npc.dexterity}")
            stdscr.addstr(7, 4, f"Intelligence: {npc.intelligence}")
            stdscr.addstr(8, 4, f"Constitution: {npc.constitution}")
            stdscr.addstr(9, 4, f"Charisma: {npc.charisma}")
            stdscr.addstr(10, 4, f"NPC Type: {npc.npc_type}")
            stdscr.addstr(11, 4, f"Hostile?: {npc.hostile}") # Is this boolean?  What type is this expected to be?
            stdscr.addstr(12, 4, f"Dialog: {npc.dialog}")
            stdscr.addstr(13, 4, f"Rumors: {npc.rumors}")
            stdscr.addstr(14, 4, f"Room Rate: {npc.room_rate}")
            stdscr.addstr(15, 4, f"Goods: {npc.goods}")
            stdscr.addstr(15, 4, f"Dialog Trees: {npc.dialog_trees}")

            stdscr.addstr(17, 2, "Select an attribute to edit (Press Enter to confirm):")
        except:
            continue

        attributes = ["Name", "Description", "Strength", "Dexterity", "Intelligence", "Constitution", "Charisma", "NPC Type", "Hostility", "Dialog", "Rumors", "Room Rate", "Goods", "Dialog Trees", "Save", "Exit"]
        
        in_menu = modify_attributes('npc', attributes, stdscr)


def create_building(stdscr):
    global building
    in_menu = True

    while in_menu:
        if building is None:
            building=Building('', '', '', [])

        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Create Building"
        stdscr.addstr(0, w//2 - len(title)//2, title)

        # Display current building attributes
        stdscr.addstr(2, 2, "Current Building Attributes:")
        stdscr.addstr(3, 4, f"Name: {building.name}")
        stdscr.addstr(4, 4, f"Building Type: {building.building_type}")
        stdscr.addstr(5, 4, f"Description: {building.description}")
        stdscr.addstr(6, 4, f"NPCs in Building: {building.npcs}")

        stdscr.addstr(16, 2, "Select an attribute to edit (Press Enter to confirm):")

        attributes = ["Name", "Building Type", "Description", "NPCs in Building", "Save", "Exit"]
       
        in_menu = modify_attributes('building', attributes, stdscr)

def location_attribute_modifier(current_attribute_idx: int, stdscr: any):
    y = get_y_pos(stdscr)
    if current_attribute_idx == 0:
        stdscr.addstr(y+1, 2, "Enter name:")
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
            stdscr.addstr(y+2, 2, location.name.ljust(20))  # Display input text
            stdscr.refresh()
    elif current_attribute_idx == 1:
        stdscr.addstr(y+1, 2, "Enter description:")
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
            stdscr.addstr(y+2, 2, location.description.ljust(60))  # Display input text
            stdscr.refresh()
    elif current_attribute_idx == 2:
        stdscr.addstr(21, 2, "Is town (True/False) Press Enter:")
        stdscr.refresh()
        is_town_input = stdscr.getstr(22, 2, 5).decode(encoding="utf-8").lower()
        stdscr.addstr(21, 2, f"You entered: {is_town_input}")
        stdscr.refresh()
        stdscr.getstr()
        location.is_town = is_town_input.strip().lower() == "t"
    
    elif current_attribute_idx == 3:
        stdscr.addstr(21, 2, "Enter building name: ")
        stdscr.refresh()
        building_input = ""
        
        while True:
            stdscr.addstr(22, 2, building_input)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_BACKSPACE:
                building_input = building_input[:-1]
            else:
                building_input += chr(key)
        
        
        building_name = building_input
        locations_folder = 'locations'

        try:
            with open(os.path.join(locations_folder, building_name+'.pkl'), 'rb') as file:
                building_object = pickle.load(file)
                location.buildings.append(building_object)
        except FileNotFoundError:
            stdscr.move(21,2)
            stdscr.clrtobot()
            stdscr.addstr(21, 2, f"Error: path {locations_folder}/{building_name}.pkl not found...")
            stdscr.refresh()
            time.sleep(1)
            return
            

    elif current_attribute_idx == 4:
        save_handler('location', stdscr, location)
    
    elif current_attribute_idx == 5:
        # Enter functionality to add connections
        stdscr.addstr(21, 2, "Enter connection direction (e.g., North, South, East, West):")
        stdscr.refresh()
        direction_input = ""
        while True:
            stdscr.addstr(22, 2, direction_input)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_BACKSPACE:
                direction_input = direction_input[:-1]
            else:
                direction_input += chr(key)
            stdscr.addstr(21, 2, direction_input.ljust(60))  # Display input text
            stdscr.refresh()

        stdscr.addstr(21, 2, "Select connected location:")
        stdscr.refresh()
        # Define the folder where the location files are stored
        locations_folder = "locations"

        # Load all location objects
        locations = []
        for file_name in os.listdir(locations_folder):
            if file_name.endswith('.pkl'):
                with open(os.path.join(locations_folder, file_name), 'rb') as file:
                    location_obj = pickle.load(file)
                    locations.append(location_obj)

        # Display a menu to select a location
        current_y = 22
        selected_location = None
        
        prev_y = None  # Initialize prev_y
        while True:
            # Clear the previous y position if it's set
            if prev_y is not None:
                stdscr.move(prev_y, 2)
                stdscr.clrtoeol()

            # Redraw the list of locations with the selection cursor
            for idx, displayed_location in enumerate(locations):
                y = 22 + idx
                if y == current_y:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, 2, displayed_location.name)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 2, displayed_location.name)

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_y > 22:
                prev_y = current_y  # Set prev_y before moving the cursor
                current_y -= 1
            elif key == curses.KEY_DOWN and current_y < 22 + len(locations) - 1:
                prev_y = current_y  # Set prev_y before moving the cursor
                current_y += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_location = locations[current_y - 22]
                break

        stdscr.addstr(21, 2, f"Connected location: {selected_location}")
        stdscr.refresh()

        stdscr.addstr(23, 2, "Enter travel days:")
        stdscr.refresh()
        travel_days_input = ""
        while True:
            stdscr.addstr(24, 2, travel_days_input)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_BACKSPACE:
                travel_days_input = travel_days_input[:-1]
            else:
                travel_days_input += chr(key)
            stdscr.addstr(24, 2, travel_days_input.ljust(60))  # Display input text
            stdscr.refresh()

        stdscr.addstr(25, 2, "Enter travel description:")
        stdscr.refresh()
        travel_description_input = ""
        stdscr.refresh()
        curses.echo()
        travel_description_input = stdscr.getstr(26, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8")
        stdscr.refresh()

        # Assuming you have a method to add connections in your Location class
        location.add_connection(direction_input.lower().strip(), selected_location, int(travel_days_input), int(0),travel_description_input)

        stdscr.clear()

    elif current_attribute_idx == 6:
        stdscr.addstr(21, 2, "Enter overworld coordinates (comma-separated tuple):")
        stdscr.refresh()
        coord_input = ""
        stdscr.refresh()
        curses.echo()
        coord_input = stdscr.getstr(26, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8")
        location_cords = coord_input.split(",")
        location.overworld_cords = location_cords

    elif current_attribute_idx == 7:
        stdscr.addstr(21, 2, "Enter NPC to add.")
        stdscr.refresh()
        npc_input = ""
        stdscr.refresh()
        curses.echo()
        npc_input = stdscr.getstr(26, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8")
        if npc_input == "clear":
            location.encounters = []
        else:
            location.encounters.append(npc_input)
    elif current_attribute_idx == 8:
        stdscr.clear()
        return False


def npc_attribute_modifier(current_attribute_idx: int, stdscr: any):
    if current_attribute_idx == 0:
        try:
            stdscr.addstr(32, 2, "Enter name:")
        except:
            pass
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
            try:
                stdscr.addstr(33, 2, npc.name.ljust(20))  # Display input text
            except:
                pass
            stdscr.refresh()
    elif current_attribute_idx == 1:
        try:
            stdscr.addstr(32, 2, "Enter description:")
        except:
            pass
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
            try:
                stdscr.addstr(33, 2, npc.description.ljust(60))  # Display input text
            except:
                pass
            stdscr.refresh()
    elif current_attribute_idx == 2:
        try:
            stdscr.addstr(32, 2, "Enter enemy strength:")
        except:
            pass
        stdscr.refresh()
        strength_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
        try:
            stdscr.addstr(34, 2, f"You entered: {strength_input}")
        except:
            pass
        stdscr.refresh()
        stdscr.getstr()
        npc.strength = strength_input.strip()
    
    elif current_attribute_idx == 3:
        try:
            stdscr.addstr(32, 2, "Enter enemy dexterity:")
        except:
            pass
        stdscr.refresh()
        dexterity_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
        try:
            stdscr.addstr(34, 2, f"You entered: {dexterity_input}")
        except:
            pass
        stdscr.refresh()
        stdscr.getstr()
        npc.dexterity = dexterity_input.strip()


    elif current_attribute_idx == 4:
        try:
            stdscr.addstr(32, 2, "Enter enemy intelligence:")
        except:
            pass
        stdscr.refresh()
        intelligence_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
        try:
            stdscr.addstr(34, 2, f"You entered: {intelligence_input}")
        except:
            pass
        stdscr.refresh()
        stdscr.getstr()
        npc.intelligence = intelligence_input.strip()
    elif current_attribute_idx == 5:
        try:
            stdscr.addstr(32, 2, "Enter enemy constitution:")
        except:
            pass
        stdscr.refresh()
        constitution_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
        try:
            stdscr.addstr(34, 2, f"You entered: {constitution_input}")
        except:
            pass
        stdscr.refresh()
        stdscr.getstr()
        npc.constitution = constitution_input.strip()
    elif current_attribute_idx == 6:
        try:
            stdscr.addstr(32, 2, "Enter enemy charisma:")
        except:
            pass
        stdscr.refresh()
        charisma_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
        try:
            stdscr.addstr(34, 2, f"You entered: {charisma_input}")
        except:
            pass
        stdscr.refresh()
        stdscr.getstr()
        npc.charisma = charisma_input.strip()

    elif current_attribute_idx == 7:
        try:
            stdscr.addstr(32, 2, "Enter enemy NPC Type:")
        except:
            pass
        stdscr.refresh()
        npc_type_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
        try:
            stdscr.addstr(34, 2, f"You entered: {npc_type_input}")
        except:
            pass
        stdscr.refresh()
        stdscr.getstr()
        npc.npc_type = npc_type_input.strip()

    elif current_attribute_idx == 8:
        try:
            stdscr.addstr(32, 2, "Is NPC hostile?  (yes/no):")
        except:
            pass
        stdscr.refresh()

        hostility_input = stdscr.getstr(33, 2, 5).decode(encoding="utf-8").lower()
        if hostility_input == 'yes':
            npc.hostile = True
            try:
                stdscr.addstr(34, 2, f"NPC is hostile")
            except:
                pass
        elif hostility_input == 'no':
            npc.hostile = False
            try:
                stdscr.addstr(34, 2, f"NPC is non-hostile")
            except:
                pass
        else:
            try:
                stdscr.addstr(34, 2, f"Please enter a valid input (yes/no)")
            except:
                pass
        
        stdscr.refresh()
        stdscr.getstr()
        
    
    elif current_attribute_idx == 9:
        try:
            stdscr.addstr(32, 2, "Enter enemy dialog as ~ delimited strings:")
        except:
            pass
        stdscr.refresh()
        try:
            dialog_input = list(stdscr.getstr(33, 2, 320).decode(encoding="utf-8").split('~'))
            try:
                stdscr.addstr(34, 2, f"Parsed dialog input: {dialog_input}")
            except:
                pass

        except TypeError:
            try:
                stdscr.addstr(34, 2, f"Unable to parse dialog entered")
            except:
                pass
        stdscr.refresh()
        stdscr.getstr()
        npc.dialog = dialog_input

    elif current_attribute_idx == 10:
        try:
            stdscr.addstr(32, 2, "Enter enemy rumors as ~ delimited strings (keep it appropriate):")
        except:
            pass
        stdscr.refresh()

        rumors_input = list(stdscr.getstr(33, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8").split('~'))
        try:
            stdscr.addstr(34, 2, f"You entered: {rumors_input}")
        except:
            pass

        stdscr.refresh()
        stdscr.getstr()
        npc.rumors = rumors_input

    elif current_attribute_idx == 11:
        try:
            stdscr.addstr(32, 2, "Enter enemy room rate:")
        except:
            pass
        stdscr.refresh()
        try:
            room_rate_input = int(stdscr.getstr(33, 2, 5).decode(encoding="utf-8"))
            try:
                stdscr.addstr(34, 2, f"You entered: {room_rate_input}")
            except:
                pass
        except TypeError:
            try:
                stdscr.addstr(34, 2, f"Please enter integer value")
            except:
                pass
        stdscr.refresh()
        stdscr.getstr()
        npc.room_rate = room_rate_input
    
    elif current_attribute_idx == 12:
        try:
            stdscr.addstr(32, 2, "Enter enemy default goods, delimited by ~:")
        except:
            pass
        stdscr.refresh()

        goods_input = stdscr.getstr(33, 2, 128).decode(encoding="utf-8").split('~')
        try:
            stdscr.addstr(34, 2, f"You entered: {goods_input}")
        except:
            pass

        stdscr.refresh()
        stdscr.getstr()
        npc.goods = goods_input

    elif current_attribute_idx == 13:
        try:
            stdscr.addstr(32, 2, "Enter enemy dialog trees:")
        except:
            pass
        stdscr.refresh()

        dialog_trees_input = stdscr.getstr(33, 2, 320).decode(encoding="utf-8").lower()
        try:
            stdscr.addstr(34, 2, f"You entered: {dialog_trees_input}")
        except:
            pass
        stdscr.refresh()
        stdscr.getstr()
        npc.dialog_trees = dialog_trees_input

    elif current_attribute_idx == 14:
        save_handler('npc', stdscr, npc)

    elif current_attribute_idx == 15:
        stdscr.clear()
        return False


def building_attribute_modifier(current_attribute_idx, stdscr):
    y = get_y_pos(stdscr)
    if current_attribute_idx == 0:
        stdscr.addstr(y+1, 2, "Enter Building Name:")
        stdscr.refresh()
        curses.echo()
        building_name_input = stdscr.getstr(y+2, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8").lower()
        stdscr.addstr(y+3, 2, f"You entered: {building_name_input}")
        stdscr.refresh()
        time.sleep(1)
        building.name = building_name_input.strip()
    elif current_attribute_idx == 1:
        stdscr.addstr(17, 2, "Enter Building Type:")
        stdscr.refresh()
        curses.echo()
        building_type_input = stdscr.getstr(18, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8").lower()
        stdscr.addstr(19, 2, f"You entered: {building_type_input}")
        stdscr.refresh()
        stdscr.getstr()
        building.building_type = building_type_input.strip()
    elif current_attribute_idx == 2:
        stdscr.addstr(17, 2, "Enter Description:")
        stdscr.refresh()
        description_input = stdscr.getstr(18, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8").lower()
        stdscr.addstr(19, 2, f"You entered: {description_input}")
        stdscr.refresh()
        stdscr.getstr()
        building.description = description_input.strip()
    
    elif current_attribute_idx == 3:
        stdscr.addstr(17, 2, "Enter NPCs in building as ~ delimited strings:")
        stdscr.refresh()
        curses.echo()
        npcs_input = stdscr.getstr(18, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8").lower()
        stdscr.addstr(19, 2, f"You entered: {npcs_input}")
        stdscr.refresh()
        stdscr.getstr()
        building.npcs = npcs_input.split('~')

    elif current_attribute_idx == 4:
        save_handler('building', stdscr, building)
    elif current_attribute_idx == 5:
        stdscr.clear()
        return False
    stdscr.clear()
    return True

                

def main(stdscr):
    os.system(f'mode 200,60')
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
        elif key == curses.KEY_DOWN and current_row < 3:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                create_location(stdscr)
            elif current_row == 1:
                create_enemy(stdscr)
            elif current_row == 2:
                create_building(stdscr)
            elif current_row == 3:
                break

curses.wrapper(main)
