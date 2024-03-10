import os, random
from display import Display as disp

from player import Player
from location import Location, Town, Wilderness
from npc import NPC
from building import Building

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









def create_world():

    global npc_dave # Temporarily made dave global so we can encounter with him as a test


    npc_dave = NPC("Dave","It is a man named Dave.", "Hello my name is Dave.", 20, 20, 20, "Inn_Patron", False, rumors = ['Davey Jones got a big ol cock.'], dialog_trees=['resources/dialog/dave.yaml'])


    bag_end = Location("Bag End", "The cozy hobbit hole of Bilbo Baggins sitting atop Bag End in the town of Hobbiton.")


    inn = Building("Golden Perch", "Inn", "A fine Inn eh")
    brandy_hall = Town("Brandyhall", "A fine town populated by the brandybucks", buildings=[inn], npcs=[])
    buck_land = Location("Buckland", "Home of the Brandybucks and Brandyhall. Here is a near small country bordering the Old Forest", is_town=True, town=brandy_hall)


    # Define connectiondi between locations with travel days
    bag_end.add_connection("east", buck_land, 3,0, "You travel East through the rolling hills of the Shire, encountering small woods and winding creeks.", [])
    buck_land.add_connection("west", bag_end, 3,0, "You travel West over the Brandywine and into the rolling hill land of the shire.", [])
    return bag_end  # Returning the starting location



def encounter(chance,encounters,player):
    player.update_stats()
    disp({'player': player.display_stats})        
    print(f"As you travel along the road.")
    #if(random.randint(0,100) < chance):
    if True:    # Force encounter as test case
        if(len(encounters) > 0):
            #npc = encounters[random.randint(0,len(encounters)-1)]
            npc = encounters[0] # Pick one static case of an encounter as a test
            npc.interaction()
            input("What do you do?: ")



def travel(num_days, player, encounter_chance, travel_description,encounters):
    wilderness = Wilderness()

    # Simulate multiple days of travel in the wilderness
    for day_count in range(1, num_days + 1):
        print(f"Day {day_count}: " + travel_description)
        encounters=[npc_dave]   # We will force an encounter with Dave as a test case
        encounter(encounter_chance,encounters, player)

        #Effects of Travel
        player.hunger += 1
        player.exhaustion += 1


        command = ''

        while(command != "travel"):
            command = input("What do you wish to do?: ").lower()
            if(command == "camp"):
                camp(player,day_count)








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
    while True:
        player.update_stats()
        disp({'player': player.display_stats})        # ToDo: Don't pass 'player' here, pass stats object
        print("\n" + str(current_location))


        # Display available directions and travel time
        directions_and_days = [f"{direction} ({days} days)" for direction, (location, days,encounter_chance,travel_description,encounters) in current_location.connections.items()]
        directions = ", ".join(directions_and_days)
        print(f"Available directions: {directions}")
        #player.display_inventory()


        if(player.location.town):
            player.location.in_town()


        direction = input("Where do you want to go? (Type 'quit' to exit) ").lower()

        if direction == 'quit':
            print("Thanks for playing!")
            break

        if direction in current_location.connections:
            connected_location, travel_days, encounter_chance, travel_description,encounters = current_location.connections[direction]

            travel(travel_days, player, encounter_chance, travel_description,encounters)  # Simulate multiple days of travel

            current_location = connected_location

            player.location = current_location

            print(f"You have arrived at {current_location.name}. It took {travel_days} days.")


        else:
            print("You can't go that way.")

if __name__ == "__main__":
    main()
