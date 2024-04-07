from player import Player
from display import Display as disp
from item import Item

from time import sleep

ATTACK_PROPORTIONALITY_CONSTANT: float = 0.2    # Weapon-less fight strength will be 20% of fighters strength

class Combat:
    def __init__(self, player: Player, enemies: list):
        """! Configure fight attributes """
        self.npc_fighters = enemies
        self.player_fighter = player
        self.npc_health = {}
        self.player_health = 0
        self.npc_weapons = []
        self.player_weapons = []
        self.fighting = True   # Start in a combat state

    def __combat_attack(self, fighter: Player) -> float:
        """! Fighter carries out a 'bare-hands' attack

        @param fighter  The player object of the fighter

        @return Number of health deducted from opponent
        """
        attack_strength = ATTACK_PROPORTIONALITY_CONSTANT * fighter.strength
        print(f'{fighter.name} dealt {attack_strength} points of damage')
        return attack_strength
    
    def __combat_use_inv(self, fighter: Player, weapon: str) -> float:
        """! Fighter carries out an attack with their weapon

        Current implementation finds all weapons in the player's live
        inventory and lets them choose whatever weapon they want to
        attack with

        @param fighter  The player object of the fighter
        @param weapon   The name of currently equipped weapon

        @return Number of health deducted from opponent
        """
        
        avail_weapons = {}

        for inv_location in fighter.inventory:
            item = fighter.inventory[inv_location]
            if type(item) is Item:
                if item.item_type == 'Weapon':
                    print(f'Found weapon {item.name} in player inventory')
                    avail_weapons[item.name.lower()] = item

        weapon_selection = input('Which weapon will you attack with?  (Enter weapon name): ').lower()
        weapon = avail_weapons[weapon_selection]

        if weapon.item_type == 'Weapon':
            damage = abs(weapon.effect)
            return damage
        else:
            print('ERROR: Object equipped is not a weapon')
        pass

    def __combat_use_skill(self):
        print('ERROR: Not implemented')
        pass

    def __combat_run_away(self) -> bool:
        """! Fighter runs away and fight ends

        @return Success status
        """
        print('Running away')
        self.fighting = False
        return True
    
    def __combat_action(self, action, fighter):
        """! Process fighter action input from player

        @return Damage or 'False' if no damage/error
        """
        if action == 1: # ATTACK
            damage = self.__combat_attack(fighter)
            return damage
        elif action == 2:   # USE WEAPON
            damage = self.__combat_use_inv(fighter, fighter.inventory)
            return damage
        elif action == 3:   # USE SKILL
            damage = self.__combat_use_skill()
            pass
        elif action == 4:   # RUN AWAY
            self.__combat_run_away()
            pass
        else:
            print('ERROR: Invalid combat action exception caught')
            return False
        
        damage = 0
        return False
    

    def fight(self) -> bool:
        """! Combat routine

        @return Completion status
        """
        fighters = self.npc_fighters
        player_fighter = self.player_fighter
        
        self.player_health = player_fighter.health   
        for fighter in fighters:
            self.npc_health[fighter] = fighter.health

        print('Fight has started')
        while self.fighting:
            # Briefly allow display of outcome of previous move
            sleep(1)

            # Update stats & refresh screen
            player_fighter.update_stats()
            disp({'player': self.player_fighter.display_stats}) 

            # Start the enemy turn
            for enemy_fighter in fighters:
                damage = self.__combat_action(1, enemy_fighter)
                self.player_health = self.player_health - damage
                player_fighter.health = self.player_health
                if self.player_health < 0:
                    print(f'{player_fighter.name} HAS DIED')
                    return True
                else:
                    pass

                # Start the player turn
                print('COMBAT MENU: What do you want to do?  Enter action number:')
                print('(1)  ATTACK')
                print('(2)  USE INVENTORY ITEM')
                print('(3)  USE SKILL')
                print('(4)  RUN AWAY')
                action = int( input() )
                damage = self.__combat_action(action, self.player_fighter)
                self.npc_health[enemy_fighter] = self.npc_health[enemy_fighter] - damage
                print(f'YOU DEALT {damage} POINTS OF DAMAGE TO {enemy_fighter.name}')
                fighter.health = self.npc_health[enemy_fighter]

                if self.npc_health[enemy_fighter] < 0:
                    print(f'{enemy_fighter.name} HAS DIED')
                    fighters.remove(enemy_fighter)
                    if len(fighters) <= 0:
                        self.fighting = False
                if self.fighting == False:
                    break

        print('Fight has concluded')
        return True

    


    