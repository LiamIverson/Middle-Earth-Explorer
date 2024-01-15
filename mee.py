import os, random

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
    def __init__(self, name, description, town=False, buildings=[]):
        self.name = name
        self.description = description
        self.connections = {}  # Connection format: {direction: (connected_location, travel_days)}
        self.town = town
        self.buildings = buildings



    def add_connection(self, direction, connected_location, travel_days,encounter_chance=0,travel_description="You travel through the wilderness.",encounters=[]):
        self.connections[direction] = (connected_location, travel_days,encounter_chance,travel_description,encounters)

    def __str__(self):
        return f"{self.name}\n{self.description}"





class Building:
    def __init__(self, name, building_type, description, npcs=[], goods=[], rumors=[]):
        self.name = name
        self.building_type = building_type
        self.description = description
        self.npcs = npcs
        self.goods = goods
        self.rumors = rumors




class Wilderness(Location):
    def __init__(self):
        super().__init__("Wilderness", "An expansive and untamed wilderness.")



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')




def display_gui(player):
    clear_screen()
    print("##############################")
    print("#      Middle-earth Game     #")
    print("##############################\n")
    print(f"Player: {player.name}")

    if player.location:
        print(f"Location: {player.location.name}")
    else:
        print("Location: Unknown")

    print("------------------------------")
    player.display_inventory()
    print(f"Hunger: {player.hunger}/10")
    print(f"Exhaustion: {player.exhaustion}/10")




def intro():
    

    characterCreated = False

    statsSelected = False

    print("Welcome to Middle-earth Adventure!")
    

    while not characterCreated:
        
        player_name = input("What is your name? ")
        
        while(not statsSelected):
            

            clear_screen()
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










def town(location):
    pass



def create_world():
    
    bag_end = Location("Bag End", "The cozy hobbit hole of Bilbo Baggins sitting atop Bag End in the town of Hobbiton.")
    
    buck_land = Location("Buckland", "Home of the Brandybucks and Brandyhall. Here is a near small country bordering the Old Forest")
    
    # Define connections between locations with travel days
    bag_end.add_connection("east", buck_land, 3,50, "You travel East through the rolling hills of the Shire, encountering small woods and winding creeks.", ['Hobbit'])

    return bag_end  # Returning the starting location



def encounter(chance,encounters):
    print("As you travel along the road.")
    if(random.randint(0,100) < chance):
        npc = encounters[random.randint(0,len(encounters)-1)]
        print("You encounter ea " + npc)
        input("What do you do?: ")



def travel(num_days, player, encounter_chance, travel_description,encounters):
    wilderness = Wilderness()

    # Simulate multiple days of travel in the wilderness
    for day_count in range(1, num_days + 1):
        print(f"Day {day_count}: " + travel_description)

        encounter(encounter_chance,encounters)





        #Effects of Travel
        player.hunger += 1
        player.exhaustion += 1


        command = ''

        while(command != "travel"):
            command = input("What do you wish to do?: ").lower()
            if(command == "camp"):
                camp(player,day_count)








def camp(player, day_count):

    display_gui(player)
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

    while True:
        display_gui(player)
        print("\n" + str(current_location))

        # Display available directions and travel time
        directions_and_days = [f"{direction} ({days} days)" for direction, (location, days,encounter_chance,travel_description,encounters) in current_location.connections.items()]
        directions = ", ".join(directions_and_days)
        print(f"Available directions: {directions}")
        player.display_inventory()

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
            
            if(player.location.town):
                town(player.location)
        
        else:
            print("You can't go that way.")

if __name__ == "__main__":
    main()
