import curses
import curses.textpad
import pickle
import os
import time

from location import Location
from building import Building
from npc import NPC
from item import Item

location = None
npc = None
building = None
item = None

MAX_STR_INPUT_CHARS = 320   # Maximum allowable number of characters of user input
ECHO_PERSIST_DELAY_S = 0.5  # Time (seconds) to display echo'd user input in editor before going back to the attributes menu

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
    - item
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



def modify_attributes(mode: str, attributes: list, stdscr: any, obj_und_edit: any):
    current_attribute_idx = 0
    y_initial_pos = stdscr.getyx()[0]
    while True:
        current_attribute_name = scrollabe_menu(stdscr, attributes)
        if mode == 'location':
            in_menu = location_attribute_modifier(current_attribute_name, stdscr, obj_und_edit)
            stdscr.addstr(40,2,f'{in_menu}')
            return in_menu
        elif mode == 'npc':
            in_menu = npc_attribute_modifier(current_attribute_name, stdscr, obj_und_edit)
            return in_menu
        elif mode == 'building':
            in_menu = building_attribute_modifier(current_attribute_name, stdscr, obj_und_edit)
            return in_menu
        elif mode == 'item':
            in_menu = item_attribute_modifier(current_attribute_name, stdscr, obj_und_edit)
            return in_menu
        else:
            return True
            


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

    menu_items = ["Create Location", "Create Enemy", "Create Building", "Create Item", "Exit"]
    result = scrollabe_menu(stdscr, menu_items, title=True)
    if result == 'Create Location':
        create_location(stdscr)
    elif result == 'Create Enemy':
        create_enemy(stdscr)
    elif result == 'Create Building':
        create_building(stdscr)
    elif result == 'Create Item':
        create_item(stdscr)
    elif result == 'Exit':
        return

def create_location(stdscr):
    location=None

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
        

        in_menu = modify_attributes('location',  attributes, stdscr, location)

        
                
def create_enemy(stdscr):
    global npc
    in_menu = True

    while in_menu:
        # Todo: Figure out how to properly initialize the NPC object
        if npc is None:
            #npc = NPC(None, None, None, None, None, None, None, None)
            npc=NPC("", "", None, 0, 0, 0, 0, 0, '', False, 0, [], [], [])

        # Replace curses calls with abstractions
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Create Enemy"
        stdscr.addstr(0, w//2 - len(title)//2, title)

        # Display current enemy attributes
        try:
            # Todo: Replace addstr calls with abstraction for appending lines
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
        
        in_menu = modify_attributes('npc', attributes, stdscr, npc)


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
        
        curses_append_line(stdscr, f"Name: {building.name}")
        curses_append_line(stdscr, f"Building Type: {building.building_type}")
        curses_append_line(stdscr, f"Description: {building.description}")
        curses_append_line(stdscr, f"NPCs in Building: {building.npcs}")

        stdscr.addstr(16, 2, "Select an attribute to edit (Press Enter to confirm):")

        attributes = ["Name", "Building Type", "Description", "NPCs in Building", "Save", "Exit"]
       
        in_menu = modify_attributes('building', attributes, stdscr, building)


def create_item(stdscr):
    global item
    in_menu = True

    while in_menu:
        if item is None:
            item=Item("", "", "", "", "", "", "")

        # Replace curses calls with abstractions
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Create Item"
        stdscr.addstr(0, w//2 - len(title)//2, title)

        # Display current item attributes
        stdscr.addstr(2, 2, "Current Item Attributes:")
        
        curses_append_line(stdscr, f"Name: {item.name}")
        curses_append_line(stdscr, f"Description: {item.description}")
        curses_append_line(stdscr, f"Item Type: {item.item_type}")
        curses_append_line(stdscr, f"Item Effect: {item.effect}")
        curses_append_line(stdscr, f"Item Effect Stat: {item.effect_stat}")
        curses_append_line(stdscr, f"Item Target: {item.target}")
        curses_append_line(stdscr, f"Item Consumable Status: {item.consumable}")

        stdscr.addstr(16, 2, "Select an attribute to edit (Press Enter to confirm):")

        attributes = ["Name", "Description", "Item Type", "Effect", "Effect Stat", "Target", "Consumable", "Save", "Exit"]
       
        in_menu = modify_attributes('item', attributes, stdscr, item)

def location_attribute_modifier(current_attribute_name: str, stdscr: any, location: Location):
    y = get_y_pos(stdscr)
    if current_attribute_name == 'Name':
        location_name_input = curses_editor_input(stdscr, "Enter Location Name:")
        location.name = location_name_input

    elif current_attribute_name == 'Description':
        location_description_input = curses_editor_input(stdscr, "Enter Location Description:")
        location.description = location_description_input

    elif current_attribute_name == 'Is Town':
        stdscr.addstr(y+1, 2, "Is town? (t/f, Press Enter):")
        stdscr.refresh()
        is_town_input = stdscr.getstr(y+2, 2, 5).decode(encoding="utf-8").lower()
        stdscr.addstr(y+3, 2, f"You entered: {is_town_input}")
        stdscr.refresh()
        stdscr.getstr()
        location.is_town = is_town_input.strip().lower() == "t"
    
    elif current_attribute_name == 'Buildings':
        building_input = curses_editor_input(stdscr, f"Enter name of building to attach to location {location.name}")
        
        building_name = building_input
        locations_folder = 'locations'

        try:
            with open(os.path.join(locations_folder, building_name+'.pkl'), 'rb') as file:
                building_object = pickle.load(file)
                location.buildings.append(building_object)
        except FileNotFoundError:
            stdscr.move(y+1,2)
            stdscr.clrtobot()
            stdscr.addstr(y+1, 2, f"Error: path {locations_folder}/{building_name}.pkl not found...")
            stdscr.refresh()
            time.sleep(1)
            return
            

    elif current_attribute_name == 'Save':
        save_handler('location', stdscr, location)
        location.name = ''
        location.description = ''
        location.is_town = False
        location.buildings = []
        location.connections = {}
        location.overworld_cords = []
        location.encounters = []

    elif current_attribute_name == 'Connections':
        # Enter functionality to add connections
        direction_input = curses_editor_input(stdscr, "Enter connection direction (e.g., North, South, East, West):", suppress_echo=True)

        stdscr.move(get_y_pos(stdscr)-2, get_x_pos(stdscr))
        stdscr.clrtobot()
        stdscr.move(get_y_pos(stdscr)-1, get_x_pos(stdscr))
        curses_append_line(stdscr, "Select connected location:", increment=False, indent=False)
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

        selected_location = scrollabe_menu(stdscr, locations)

        stdscr.addstr(y+1, 2, f"Connected location: {selected_location}")
        stdscr.clrtobot()
        stdscr.refresh()


        travel_days_input = curses_editor_input(stdscr, "Enter travel days:", clean=True)
        travel_description_input = curses_editor_input(stdscr, "Enter travel description:")

        # Assuming you have a method to add connections in your Location class
        location.add_connection(direction_input.lower().strip(), selected_location, int(travel_days_input), int(0),travel_description_input)

        stdscr.clear()

    elif current_attribute_name == 'Overworld Coords':
        coord_input = curses_editor_input(stdscr, "Enter overworld coordinates (comma-separated tuple):")
        location_cords = coord_input.split(",")
        location.overworld_cords = location_cords

    elif current_attribute_name == 'Encounters':
        npc_input = curses_editor_input(stdscr, "Enter NPC to add:")
        if npc_input == "clear":
            location.encounters = []
        else:
            location.encounters.append(npc_input)

    elif current_attribute_name == 'Exit':
        stdscr.clear()
        return False
    
    stdscr.clear()
    return True


def npc_attribute_modifier(current_attribute_name: str, stdscr: any, npc: NPC):

    if current_attribute_name == 'Name':
        npc_name_input = curses_editor_input(stdscr, "Enter NPC name:")
        npc.name = npc_name_input

    elif current_attribute_name == 'Description':
        npc_description_input = curses_editor_input(stdscr, "Enter NPC description:")
        npc.description = npc_description_input

    elif current_attribute_name == 'Strength':
        strength_input = curses_editor_input(stdscr, "Enter enemy strength:")
        npc.strength = strength_input.strip()
    
    elif current_attribute_name == 'Dexterity':
        dexterity_input = curses_editor_input(stdscr, "Enter enemy dexterity:")
        npc.dexterity = dexterity_input.strip()

    elif current_attribute_name == 'Intelligence':
        intelligence_input = curses_editor_input(stdscr, "Enter enemy intelligence:")
        npc.intelligence = intelligence_input.strip()

    elif current_attribute_name == 'Constitution':
        constitution_input = curses_editor_input(stdscr, "Enter enemy constitution:")
        npc.constitution = constitution_input.strip()

    elif current_attribute_name == 'Charisma':
        charisma_input = curses_editor_input(stdscr, "Enter enemy charisma:")
        npc.charisma = charisma_input.strip()

    elif current_attribute_name == 'NPC Type':
        npc_type_input = curses_editor_input(stdscr, "Enter enemy NPC Type:")
        npc.npc_type = npc_type_input.strip()

    elif current_attribute_name == 'Hostility':
        hostility_input = curses_editor_input(stdscr, "Is NPC hostile?  (yes/no):", suppress_echo=True)
        if hostility_input == 'yes':
            npc.hostile = True
            curses_append_line(stdscr, "NPC is hostile")
        elif hostility_input == 'no':
            npc.hostile = False
            curses_append_line(stdscr, "NPC is non-hostile")
        else:
            curses_append_line(stdscr, "Please enter a valid input (yes/no)")
        
        stdscr.refresh()
        stdscr.getstr()
        
    
    elif current_attribute_name == 'Dialog':
        dialog_input = curses_editor_input(stdscr, "Enter enemy dialog as ~ delimited strings:")
        npc.dialog = dialog_input.split('~')

    elif current_attribute_name == 'Rumors':
        rumors_input = curses_editor_input(stdscr, "Enter enemy rumors as ~ delimited strings:")
        npc.rumors = rumors_input.split('~')

    elif current_attribute_name == 'Room Rate':
        room_rate_input = curses_editor_input(stdscr, "Enter enemy room rate:")
        npc.room_rate = room_rate_input
    
    elif current_attribute_name == 'Goods':
        goods_input = curses_editor_input(stdscr, "Enter enemy default goods, delimited by ~:")
        npc.goods = goods_input.split('~')

    elif current_attribute_name == 'Dialog Trees':
        dialog_trees_input = curses_editor_input(stdscr, "Enter enemy dialog trees:")
        npc.dialog_trees = dialog_trees_input

    elif current_attribute_name == 'Save':
        save_handler('npc', stdscr, npc)

    elif current_attribute_name == 'Exit':
        stdscr.clear()
        return False

    stdscr.clear()
    return True


def building_attribute_modifier(current_attribute_name: str, stdscr: any, building: Building):
    if current_attribute_name == 'Name':
        building_name_input = curses_editor_input(stdscr, "Enter Building Name:")
        building.name = building_name_input.strip()

    elif current_attribute_name == 'Building Type':
        building_type_input = curses_editor_input(stdscr, "Enter Building Type:")
        building.building_type = building_type_input.strip()

    elif current_attribute_name == 'Description':
        description_input = curses_editor_input(stdscr, "Enter Building Description:")
        building.description = description_input.strip()

    elif current_attribute_name == 'NPCs in Building':
        npcs_input = curses_editor_input(stdscr, "Enter NPCs in building as ~ delimited strings:")
        building.npcs = npcs_input.split('~')
        
    elif current_attribute_name == 'Save':
        save_handler('building', stdscr, building)

    elif current_attribute_name == 'Exit':
        stdscr.clear()
        return False
    
    stdscr.clear()
    return True

def item_attribute_modifier(current_attribute_name: str, stdscr: any, item: Item):

    if current_attribute_name == 'Name':
        item_name_input = curses_editor_input(stdscr, "Enter Item Name:")
        item.name = item_name_input

    elif current_attribute_name == 'Description':
        item_description_input = curses_editor_input(stdscr, "Enter Item Description:")
        item.description = item_description_input

    elif current_attribute_name == 'Item Type':
        item_type_input = curses_editor_input(stdscr, "Enter item type ('Weapon', 'Armor', 'Position')")
        item.item_type = item_type_input

    elif current_attribute_name == 'Effect':
        item_effect_input = curses_editor_input(stdscr, "Enter Item Effect:")
        item.effect = item_effect_input

    elif current_attribute_name == 'Effect Stat':
        item_effect_stat_input = curses_editor_input(stdscr, "Enter the Correlated Player Stat:")
        item.effect_stat = item_effect_stat_input

    elif current_attribute_name == 'Target':
        item_target_input = curses_editor_input(stdscr, "The target of the item ('player', 'npc', 'both')")
        item.target = item_target_input

    elif current_attribute_name == 'Consumable':
        item_consumable_input = curses_editor_input(stdscr, "Is the item single/fixed use or infinite?")
        item.consumable = item_consumable_input

    elif current_attribute_name == 'Save':
        save_handler('item', stdscr, item)

    elif current_attribute_name == 'Exit':
        stdscr.clear()
        return False
    
    stdscr.clear()
    return True

"""! Scrollable menus

@param stdscr The curses window object

@return The selected menu object
"""
def scrollabe_menu(stdscr: any, menu_objects: any, title=False):
    # Display a menu to select menu 
    if title == False:
        init_y = get_y_pos(stdscr)+1
        #init_x = get_x_pos(stdscr)
        init_x = 2
    else:
        h, w = stdscr.getmaxyx()
        init_x = w//2
        init_y = h//2 - len(menu_objects)//2
    current_y = init_y
    selected_object = None
    
    prev_y = None  # Initialize prev_y
    while True:
        # Clear the previous y position if it's set
        if prev_y is not None:
            stdscr.move(prev_y, 2)
            stdscr.clrtoeol()

        # Redraw the list of objects with the selection cursor
        for idx, displayed_object in enumerate(menu_objects):
            y_cur_idx = init_y + idx
            x = init_x
            if title == True:
                x = init_x - len(displayed_object)//2
            if y_cur_idx == current_y:
                stdscr.attron(curses.A_REVERSE)

                try:
                    stdscr.addstr(y_cur_idx, x, displayed_object.name)
                except AttributeError:
                    stdscr.addstr(y_cur_idx, x, displayed_object)
                stdscr.attroff(curses.A_REVERSE)
            else:
                try:
                    stdscr.addstr(y_cur_idx, x, displayed_object.name)
                except AttributeError:
                    stdscr.addstr(y_cur_idx, x, displayed_object)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_y > init_y:
            prev_y = current_y  # Set prev_y before moving the cursor
            current_y -= 1
        elif key == curses.KEY_DOWN and current_y < init_y + len(menu_objects) - 1:
            prev_y = current_y  # Set prev_y before moving the cursor
            current_y += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_object = menu_objects[current_y - init_y]
            break
    return selected_object

"""! Abstraction to get most recently
     written line from the curses
     window object

@param stdscr The curses window object

@return Current integer cursor line number
"""


"""! Abstraction to get current character
     position within a line of the curses
     window object

@param stdscr The curses window object

@return Current integer cursor position
"""
def get_x_pos(stdscr: any) -> int:
    return int(stdscr.getyx()[1])

"""! Abstraction to get most recently
     written line from the curses
     window object

@param stdscr The curses window object

@return Current integer cursor line number
"""
def get_y_pos(stdscr: any) -> int:
    return int(stdscr.getyx()[0])

"""! Abstraction to write new-line using curses
     Appends text on new line after most recently
     written line

@param stdscr    The curses window object
@param out_str   The string to be appended to the screen
@param increment Write string on next line?

@return Success status (True/False)
"""
def curses_append_line(stdscr: any, out_str: str, increment=True, indent=True) -> bool:
    try:
        y = get_y_pos(stdscr)
        if increment == True:
            y=y+1
        if indent == True:
            x=4
        else:
            x=2
        stdscr.addstr(y, x, out_str)
        return True
    except:
        return False

"""! Abstraction to prompt user and store response

@param stdscr  The curses window object
@param prompt  The question/prompt that the user is responding to
@param suppress_echo  Don't echo back to user what they typed
@param clean   Remove the prompt/response from screen after we're done

@return Raw user input decoded as a utf-8 string
"""
def curses_editor_input(stdscr: any, prompt: str, suppress_echo=False, clean=False) -> str:
    y = get_y_pos(stdscr)
    x = get_x_pos(stdscr)
    stdscr.addstr(y+1, 2, prompt)
    stdscr.refresh()
    curses.echo()
    user_input = stdscr.getstr(y+2, 2, MAX_STR_INPUT_CHARS).decode(encoding="utf-8")
    if suppress_echo == False:  # Echo user input
        stdscr.addstr(y+3, 2, f"You entered: {user_input}")
        stdscr.refresh()
        # stdscr.getstr()
        time.sleep(ECHO_PERSIST_DELAY_S)
    if clean == True:
        stdscr.move(y,x)
        stdscr.clrtobot()
    return user_input

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

curses.wrapper(main)
