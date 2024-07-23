#Name - The items name
#Description - The in game item description
#Item Type - 'Weapon', 'Armor', 'Position'
#Effect - The value, negative or positive, that the item effects on the target
#Effec_stat - The stat whos value is modified by the effect value
#Target - The target of the item, either self, npc or both
#Consumable - Is the item single/fixed use or infinite

class Item:
	def __init__(self, name, description, item_type, effect, effect_stat, target, consumable,slot=None):
		self.name = name
		self.description = description
		self.item_type = item_type
		self.effect = effect
		self.effect_stat = effect_stat
		self.target = target
		self.consumable = consumable
		self.slot = slot