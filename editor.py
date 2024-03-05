import curses
import pickle


from location import Location


location = None


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
                    location.buildings = buildings_input.split(",")

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
