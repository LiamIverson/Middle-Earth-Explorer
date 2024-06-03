import os, random, pickle, time, re
from display import Display as disp

from player import Player
from location import Location, Town, Wilderness
from npc import NPC
from building import Building
from combat import Combat
from item import Item

game_map = []

regions = []

#The overworld is treated as 2D grid of 100x100 squares for a total of 10k indexes
#For the time being when a location is loaded in its assigned based on its X/Y coordinates
#to the correct index for later reference. World movement operates on 2 systems
#direct node traversal that works with the nested locations and free wondering that lets you travel one day
#in each grid location


over_world = [[0 for _ in range(100)] for _ in range(100)]

region_types = [0,1,2,3,4]

def intro():


    characterCreated = False

    statsSelected = False

    print("Welcome to Middle-earth Adventure!")


    while not characterCreated:

        player_name = input("What is your name? ")

        while(not statsSelected):
            strength = random.randint(3,18)
            intelligence = random.randint(3,18)
            dexterity = random.randint(3,18)

            print("Your current stats are: ")

            print("Strength: " + str(strength))
            print("Intellgience: "+ str(intelligence))
            print("Dexterity: " + str(dexterity))


            choice = input("Do you accept?").lower()

            if(choice == "yes"):
                statsSelected = True

        player = Player(player_name, strength, dexterity, intelligence)
        characterCreated = True


    return player




def load_locations():
    locations = []
    location_files = [f for f in os.listdir("locations") if os.path.isfile(os.path.join("locations", f))]
    for file_name in location_files:
        with open(os.path.join("locations", file_name), "rb") as f:
            location = pickle.load(f)
            locations.append(location)
            if hasattr(location,"overworld_cords"):
                location_overworld_x = int(location.overworld_cords[0])
                location_overworld_y = int(location.overworld_cords[1])
                over_world[location_overworld_x][location_overworld_y] = location
    input()
    return locations



def load_regions(file_path):
    regions = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    region_name = None
    for line in lines:
        line = line.strip()
        if line.startswith('Region'):
            region_name = line
            regions[region_name] = {'coordinates': [], 'location': ''}
        elif line.startswith('Location:'):
            location = line.split(': ')[1]
            if region_name:
                regions[region_name]['location'] = location
        elif line.startswith('Coordinates:'):
            coordinates = re.findall(r'\((\d+),(\d+)\)', line)
            coordinates = [(int(x), int(y)) for x, y in coordinates]
            if region_name:
                regions[region_name]['coordinates'] = coordinates

    return regions


def create_world():

    global regions


    # npc_dave = NPC("Dave","It is a man named Dave.", "Hello my name is Dave.", 20, 20, 20, "Inn_Patron", False, rumors = ['Davey Jones got a big ol cock.'], dialog_trees=[os.path.normpath('resources/dialog/dave.yaml')], room_rate=-1, goods=[])

    # bag_end = Location("Bag End", "The cozy hobbit hole of Bilbo Baggins sitting atop Bag End in the town of Hobbiton.")


    # inn = Building("Golden Perch", "Inn", "A fine Inn eh")
    # brandy_hall = Town("Brandyhall", "A fine town populated by the brandybucks", buildings=[inn], npcs=[])
    # buck_land = Location("Buckland", "Home of the Brandybucks and Brandyhall. Here is a near small country bordering the Old Forest", is_town=True, town=brandy_hall)


    # # Define connectiondi between locations with travel days
    # bag_end.add_connection("east", buck_land, 3,0, "You travel East through the rolling hills of the Shire, encountering small woods and winding creeks.", [])
    # buck_land.add_connection("west", bag_end, 3,0, "You travel West over the Brandywine and into the rolling hill land of the shire.", [])
    
    # Load all locations from files
    all_locations = load_locations()

    #regions = [Location("Plains", "A wide open plain with some smalls hills and tiny clusters of small wood.")]
    
    # Load Regions

    regions = load_regions('regions/regions.txt')

    # Add locations to game map
    for location in all_locations:
        game_map.append(location)
    
    return game_map[0]  # Returning the starting location



def encounter(chance,encounters,player):
    if(random.randint(0,100) < chance):
        player.update_stats()
        disp({'player': player.display_stats})
        print("As you travel along the road.")
        if(len(encounters) > 0):
            #This will need to be updated so that it uses the returned encounter key to look up the actual NPC.
            npc = encounters[random.randint(0,len(encounters)-1)]
            npc.interaction()
            input("What do you do?: ")



def march(player):
    direction = input("Enter direction of march: ").lower()
    direction_dict = {'north':(0,1),"south":(0,-1),"west":(-1,0),"east":(1,0)}
    direction_mod = direction_dict[direction]

    player.overworld_x = int(player.overworld_x) + direction_mod[0]
    player.overworld_y = int(player.overworld_y) + direction_mod[1]

    overworld_location = over_world[player.overworld_x][player.overworld_y]
    overworld_coords = (player.overworld_x, player.overworld_y)

    player.hunger += 1
    player.exhaustion += 1
    
    #Updates this to use the new region logic

    for i in regions:
        if overworld_coords in i["coordinates"]:
            # Get the location name
            location_name = i["location"]
            
            # Construct the file path
            file_path = f"generic_location/{location_name}.pkl"
            
            # Load the object from the .pkl file
            with open(file_path, 'rb') as file:
                location_object = pickle.load(file)
            
            # Return the loaded location object
            return location_object
            
    return Location("Plains", "A wide open plain with some smalls hills and tiny clusters of small wood.")

    # if overworld_location in region_types:
    #     return regions[overworld_location]
    # else:
    #     return overworld_location


def travel(num_days, player, encounter_chance, travel_description,encounters,direction,connected_location):
    wilderness = Wilderness()
    direction = direction.lower()

    direction_dict = {'north':(0,1),"south":(0,-1),"west":(-1,0),"east":(1,0)}
    direction_mod = direction_dict[direction]
    
    # Simulate multiple days of travel in the wilderness

    destination = connected_location

    for day_count in range(1, num_days + 1):
        print(f"Day {day_count}: " + travel_description)
        
        player.overworld_x += direction_mod[0]
        player.overworld_y += direction_mod[1]

        encounter(encounter_chance,encounters, player)

        overworld_location = over_world[player.overworld_x][player.overworld_y]

        if(overworld_location != 0):
            if(overworld_location in regions):
                pass
            else:
                destination = overworld_location
            break





        #Effects of Travel
        player.hunger += 1
        player.exhaustion += 1


        command = ''

        while(command != "travel"):
            command = input("What do you wish to do?: ").lower()
            if(command == "camp"):
                camp(player,day_count)

    return destination




def camp(player, day_count):
    player.update_stats()
    disp({'player': player.display_stats})        # ToDo: Don't pass 'player' here, pass stats object
    print("You set up camp for the night around a roaring fire.")

    # Camp actions

    action = ''

    while(action != "continue"):

        action = input("What do you want to do at camp? (Type 'eat' to consume food, 'continue' to proceed) ").lower()

        if action == 'eat':
            food_to_consume = int(input("How many units of food do you want to consume? "))
            if player.consume_food(food_to_consume):
                print(f"You consume {food_to_consume} units of food.")
            else:
                print("Not enough food! You should find some.")

        elif action == 'rest':
            player.player_rest()

    print("You break camp and continue on your journey.")





def main():
    player = intro()
    current_location = create_world()
    player.location = current_location
    player.overworld_x = current_location.overworld_cords[0]
    player.overworld_y = current_location.overworld_cords[1]



    while True:
        player.update_stats()
        disp({'player': player.display_stats})        # ToDo: Don't pass 'player' here, pass stats object
        print("\n" + str(current_location))


        # Display available directions and travel time
        directions_and_days_and_name = [f"{direction} ({days} days) - {location.name}" for direction, (location, days,encounter_chance,travel_description,encounters) in current_location.connections.items()]
        directions = ", ".join(directions_and_days_and_name)
        print(f"Available directions: {directions}")
        #player.display_inventory()

        if(player.location.town):
            player.location.in_town()
        else:
            encounter_chance = current_location.encounter_chance
            encounters =  current_location.encounters
            encounter(encounter_chance,encounters, player)


        

        direction = input("Where do you want to go? (Type 'quit' to exit) ").lower()

        if direction == 'quit':
            print("Thanks for playing!")
            break
        elif direction == 'march':
            current_location = march(player)
        elif direction in current_location.connections:
            connected_location, travel_days, encounter_chance, travel_description,encounters = current_location.connections[direction]

            current_location =  travel(travel_days, player, encounter_chance, travel_description,encounters, direction, connected_location)  # Simulate multiple days of travel
            #If a location on the overworld is encountered when traveling, the travel function exits and returns that as the current location
            #Otherwise it will return the connected location as the default after you arrive
            #Travel should be thought off as 'fast travel'. Marching is more generic travel.

            player.location = current_location

            print(f"You have arrived at {current_location.name}. It took {travel_days} days.")
        else:
            print("You can't go that way.")
            time.sleep(1)
            
if __name__ == "__main__":
    main()
