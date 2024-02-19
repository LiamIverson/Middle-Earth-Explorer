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
