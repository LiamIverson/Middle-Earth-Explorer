import os, random
from display import Display as disp

class Player:
    def __init__(self, name, strength, dexterity, intelligence):
        self.name = name
        self.location = None
        self.inventory = {'food': 10}  # Starting with 10 units of food
        self.hunger = 0
        self.exhaustion = 0
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

    def move(self, new_location):
        self.location = new_location

    def consume_food(self, amount):
        if self.inventory['food'] >= amount:
            self.inventory['food'] -= amount
            self.hunger -= amount  # Decrease hunger when consuming food
            return True
        else:
            print("Not enough food! You should find some.")
            return False


    def player_rest(self):
        print("You sleep and recover some energy")

        self.exhaustion -= 1

    def add_food(self, amount):
        self.inventory['food'] += amount

    def display_inventory(self):
        print(f"Inventory: Food - {self.inventory['food']} units")



class Location:
    def __init__(self, name, description, is_town=False, buildings=[], town=[] ):
        self.name = name
        self.description = description
        self.connections = {}  # Connection format: {direction: (connected_location, travel_days)}
        self.is_town = is_town
        self.buildings = buildings
        self.town = town



    def add_connection(self, direction, connected_location, travel_days,encounter_chance=0,travel_description="You travel through the wilderness.",encounters=[]):
        self.connections[direction] = (connected_location, travel_days,encounter_chance,travel_description,encounters)

    def __str__(self):
        return f"{self.name}\n{self.description}"


    def in_town(self):
        print("Within the town there are these buildings.")
        print(self.buildings)
        input()





class NPC:
    def __init__(self, name, description, dialog, strength,dexterity, intelligence, npc_type, hostile, room_rate = 0,rumors=[], goods = [], dialog_trees = []):

        self.name = name
        self.description = description
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.npc_type = npc_type
        self.hostile = hostile
        self.dialog =  dialog
        self.rumors = rumors
        self.room_rate = room_rate
        self.goods = goods
        self.dialog_trees = dialog_trees


    def interaction(self):
        print(self.description)
        if(self.hostile):
            pass
            #combat

        else:
            print(self.dialog)
            if(self.npc_type == "Innkeeper"):
                inn_keeper()
            elif(self.npc_type == "Merchant"):
                merchant()
            elif(self.npc_type == "Blacksmith"):
                blacksmith()
            elif(self.npc_type == "Inn_Patron"):
                self.patron()

            elif(self.npc_type == "Complex_Character"):
                self.complex_character(self)




    def inn_keeper(self):
        pass

    def merchant(self):
        pass

    def blacksmith(self):
        pass

    def patron(self):
        pass

    def complex_character(self):
        pass



    #Example of a dialog tree with reward
    #{"The big apple is over there.":{"type":"charisma","value":15, "reward":{}}}


class Building:
    def __init__(self, name, building_type, description, npcs=[]):
        self.name = name
        self.building_type = building_type
        self.description = description
        self.npcs = npcs


    def enter_building(self):
        print(description)
        print("Inside you can see ")
        print(self.npcs)

        #choice = input("What do you do?").lower()
        #if(choice == "talk"):
         #   for i in range(self.npcs):
          #      print(str(i) + " - " +str(self.npc[i].name))



class Town:


    def __init__(self, Location, name, buildings, npcs):
        self.location = Location
        self.name = name
        self.buildings = buildings
        self.nps = npcs



    def enter_town():
        print("You enter the town of " + self.name)
        print("The town contains these buildings " + self.buildings)


    def add_building(building):
        self.buildings.append(building)

class Wilderness(Location):
    def __init__(self):
        super().__init__("Wilderness", "An expansive and untamed wilderness.")


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
        #disp({'player': player})


    return player









def create_world():





    npc_dave = NPC("Dave","It is a man named Dave.", "Hello my name is Dave.", 20, 20, 20, "Inn_Patron", False, rumors = ['Davey Jones got a big ol cock.'])


    bag_end = Location("Bag End", "The cozy hobbit hole of Bilbo Baggins sitting atop Bag End in the town of Hobbiton.")


    inn = Building("Golden Perch", "Inn","A fine Inn eh")
    brandy_hall = Town("Brandyhall", "A fine town populated by the brandybucks", buildings=[inn], npcs=[])
    buck_land = Location("Buckland", "Home of the Brandybucks and Brandyhall. Here is a near small country bordering the Old Forest", is_town=True, town=brandy_hall)


    # Define connectiondi between locations with travel days
    bag_end.add_connection("east", buck_land, 3,100, "You travel East through the rolling hills of the Shire, encountering small woods and winding creeks.", [])

    return bag_end  # Returning the starting location



def encounter(chance,encounters,player):
    disp({'player': player})
    print("As you travel along the road.")
    if(random.randint(0,100) < chance):
        if(len(encounters) > 0):
            npc = encounters[random.randint(0,len(encounters)-1)]
            npc.interaction()
            input("What do you do?: ")



def travel(num_days, player, encounter_chance, travel_description,encounters):
    wilderness = Wilderness()

    # Simulate multiple days of travel in the wilderness
    for day_count in range(1, num_days + 1):
        print(f"Day {day_count}: " + travel_description)

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
    disp({'player': player})
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





def main():
    player = intro()
    current_location = create_world()
    player.location = current_location
    while True:
        disp({'player': player})
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
