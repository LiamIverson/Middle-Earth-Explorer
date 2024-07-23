class Player:
    def __init__(self, name, strength, dexterity, intelligence):
        self.name = name
        self.location = None
        self.inventory = {'food': 10, 'wood':0, 'gold':0, "legs":None, "chest":None,"head":None, "backpack":[]}  # Starting with 10 units of food
        self.health = 20
        self.hunger = 0
        self.exhaustion = 0
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.display_stats = {}
        self.overworld_x = 0
        self.overworld_y = 0

    def move(self, new_location):
        self.location = new_location



    def add_item_backpack(self,item):
        self.inventory["backpack"].append(item)

    def remove_item_backpack(self,item):
        self.inventory["backpack"].remove(item)

    #Pass item object along with the slot keyword to equip.
    #Must already be present in inventory
    def equip_item(self,item,position):
        if item in self.inventory["backpack"]:
            self.inventory[position] = item
    
    def use_item(self,item):
        #To Do. Implement logic for use. This might be mostly handled outside the class in contextual functions
        pass


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

    def update_stats(self):
        self.display_stats['Name'] = self.name
        if self.location != None:
            self.display_stats['Location'] = self.location.name
        self.display_stats['Inventory'] = self.inventory
        self.display_stats['Hunger'] = self.hunger
        self.display_stats['Health'] = self.health
        self.display_stats["Overworld X"] = self.overworld_x
        self.display_stats["Overworld Y"] = self.overworld_y
