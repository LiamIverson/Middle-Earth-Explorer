import yaml

YAML_PATH = 'resources/dialog/dave.yaml'


def run_dialog_tree(dialog_obj_node):
    
    if type(dialog_obj_node) == type(''):
        print(dialog_obj_node)
    else:
        for key in dialog_obj_node:
            print(f'{key}\n')
            i=0
            opt = {}
            if type(dialog_obj_node[key]) == type(''):
                print(f'(1)  {dialog_obj_node[key]}')
            else:
                for level in dialog_obj_node[key]:
                    i = i+1
                    print(f'({i}):  {level}')
                    opt[i] = level
                selection = int(input('Select a dialog option: '))
                next_node = dialog_obj_node[key][opt[selection]]
                run_dialog_tree(next_node)




with open(YAML_PATH, 'r') as dave_dialog_file:
    dave_dialog_obj = yaml.safe_load(dave_dialog_file)

#print(dave_dialog_obj)
run_dialog_tree(dave_dialog_obj)

#print(get_dict_depth(dave_dialog_obj))

# from anytree import Node, RenderTree


# dave_greeting = Node("Yo I'm Dave!  How are you doing today?")
# response_option_a = Node("I'm doing well, thank you!", parent=dave_greeting)
# dave_reply_option_a = Node("That's good to hear!  Might you be interested in buying some fine wares?", parent=response_option_a)
# response_option_b = Node("It's been rough lately, but hanging in there", parent=dave_greeting)
# dave_reply_option_b = Node("Sucks to suck; really sounds like a skill issue, buddy", parent=response_option_b)
# response_option_c = Node("Go fuck yourself, Dave", parent=dave_greeting)
# dave_reply_option_c = Node("I'm gonna kick your ass!", parent=response_option_c)
