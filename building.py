class Building:
    def __init__(self, name, building_type, description, npcs=[]):
        self.name = name
        self.building_type = building_type
        self.description = description
        self.npcs = npcs


    def enter_building(self):
        print(self.description)
        print("Inside you can see ")
        print(self.npcs)

        #choice = input("What do you do?").lower()
        #if(choice == "talk"):
         #   for i in range(self.npcs):
          #      print(str(i) + " - " +str(self.npc[i].name))