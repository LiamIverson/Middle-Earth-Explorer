import curses
import pickle
import os

from location import Location
from building import Building

location = None


def save_location(location, filename):
    with open('locations/'+filename, 'wb') as file:
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
        stdscr.addstr(8, 4, f"Connections: {location.connections}")
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
        stdscr.addstr(8, 4, f"Connections: {location.connections}")

        stdscr.addstr(9, 2, "Select an attribute to edit (Press Enter to confirm):")

        attributes = ["Name", "Description", "Is Town", "Buildings", "Town", "Save", "Connections", "Exit"]
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
                    # Enter functionality to add connections
                    stdscr.addstr(19, 2, "Enter connection direction (e.g., North, South, East, West):")
                    stdscr.refresh()
                    direction_input = ""
                    while True:
                        stdscr.addstr(20, 2, direction_input)
                        stdscr.refresh()
                        key = stdscr.getch()
                        if key == curses.KEY_ENTER or key in [10, 13]:
                            break
                        elif key == curses.KEY_BACKSPACE:
                            direction_input = direction_input[:-1]
                        else:
                            direction_input += chr(key)
                        stdscr.addstr(20, 2, direction_input.ljust(60))  # Display input text
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
                    while True:
                        stdscr.addstr(24, 2, travel_description_input)
                        stdscr.refresh()
                        key = stdscr.getch()
                        if key == curses.KEY_ENTER or key in [10, 13]:
                            break
                        elif key == curses.KEY_BACKSPACE:
                            travel_description_input = travel_description_input[:-1]
                        else:
                            travel_description_input += chr(key)
                        stdscr.addstr(24, 2, travel_description_input.ljust(60))  # Display input text
                        stdscr.refresh()

                    # Assuming you have a method to add connections in your Location class
                    location.add_connection(direction_input.lower().strip(), selected_location, int(travel_days_input), int(0),travel_description_input)

                    stdscr.clear()
                elif current_attribute_idx == 7:
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
