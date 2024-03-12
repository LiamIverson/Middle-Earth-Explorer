class DialogTree:
    def __init__(self, dialog_obj):
        self.obj = dialog_obj
        self.action_val = None
        self.run_dialog_tree()



    def run_dialog_tree(self):
        
        # If dialog tree ends without any specified action
        if type(self.obj) == type(''):
            print(self.obj)
        else:
            for key in self.obj:
                print(f'{key}\n')
                i=0
                opt = {}
                if type(self.obj[key]) == type(''):  # Detect action at end of dialog tree
                    self.action_val = self.obj[key]
                    
                else:   # Move through dialog tree
                    for level in self.obj[key]:
                        i = i+1
                        print(f'({i}):  {level}')
                        opt[i] = level
                    selection = int(input('Select a dialog option: '))
                    next_node = self.obj[key][opt[selection]]
                    self.obj = next_node
                    self.run_dialog_tree()