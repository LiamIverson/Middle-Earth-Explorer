from dialog_tree import DialogTree
import yaml

class NPC:
    def __init__(self, name: str, description: str, dialog: None, strength: int, dexterity: int, intelligence: int, constitution:int, charisma:int, hostile: bool, room_rate: int, rumors: list, goods: list, dialog_trees: list):

        self.name = name
        self.description = description
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.constitution = constitution
        self.charisma = charisma
        self.hostile = hostile
        self.dialog =  dialog
        self.rumors = rumors
        self.room_rate = room_rate
        self.goods = goods
        self.dialog_trees = dialog_trees
        self.health = 20    # Arbitrarily starting with 20 units of health for testing


    def interaction(self):
        print(self.description)
        
        # Use the first dialog tree as a test case
        with open(self.dialog_trees[0], 'r') as interaction_test:
            dialog_obj_test = yaml.safe_load(interaction_test)

        dialog = DialogTree(dialog_obj_test)
        return dialog.action_val

        if(self.hostile):
            pass
            #combat

        else:
            
            #print(self.dialog)
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



    #Example of a dialog tree with reward
    #{"The big apple is over there.":{"type":"charisma","value":15, "reward":{}}}