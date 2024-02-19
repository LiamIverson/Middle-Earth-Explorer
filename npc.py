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