class Location:
    def __init__(self, name, description, is_town=False, buildings=[], town=[], encounter_chance=0.0,encounters=[],overworld_cords=[0,0]):
        self.name = name
        self.description = description
        self.connections = {}  # Connection format: {direction: (connected_location, travel_days)}
        self.is_town = is_town
        self.buildings = buildings
        self.overworld_cords = overworld_cords
        self.encounter_chance= encounter_chance
        self.encounters = encounters



    def add_connection(self, direction, connected_location, travel_days,encounter_chance=0,travel_description="You travel through the wilderness.",encounters=[]):
        self.connections[direction] = (connected_location, travel_days,encounter_chance,travel_description,encounters)

    def __str__(self):
        return f"{self.name}\n{self.description}"


    def enter_town(self):
        
        print("You enter the town of " + self.name)
        print("The town contains these buildings ")
        
        for i in self.buildings:
            print(i.name)
        
        building_name = ""

        while(building_name != "exit"):
            building_name = input("Enter the name of the building you wish to visit, or 'exit' to leave.").lower()
            for i in self.buildings:
                if(building_name == i.name.lower()):
                    i.enter_building()


    def add_building(building):
        self.buildings.append(building)

class Town:


    def __init__(self, npcs, town_encounters):
        self.nps = npcs
        self.town_encounters = town_encounters



    def enter_town(self):
        print("You enter the town of " + self.name)
        print("The town contains these buildings ")
        for i in self.buildings:
            print(i.name)
        building_name = ""
        while(building_name != "exit"):
            building_name = input("Enter the name of the building you wish to visit, or 'exit' to leave.").lower()
            for i in self.buildings:
                if(building_name == i.name.lower()):
                    i.enter_building()


    def add_building(building):
        self.buildings.append(building)



class Wilderness(Location):
    def __init__(self):
        super().__init__("Wilderness", "An expansive and untamed wilderness.")