from anytree import Node, RenderTree


dave_greeting = Node("Yo I'm Dave!  How are you doing today?")
response_option_a = Node("I'm doing well, thank you!", parent=dave_greeting)
dave_reply_option_a = Node("That's good to hear!  Might you be interested in buying some fine wares?", parent=response_option_a)
response_option_b = Node("It's been rough lately, but hanging in there", parent=dave_greeting)
dave_reply_option_b = Node("Sucks to suck; really sounds like a skill issue, buddy", parent=response_option_b)
response_option_c = Node("Go fuck yourself, Dave", parent=dave_greeting)
dave_reply_option_c = Node("I'm gonna kick your ass!", parent=response_option_c)
