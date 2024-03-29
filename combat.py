from player import Player
from display import Display as disp

from time import sleep

ATTACK_PROPORTIONALITY_CONSTANT: float = 0.2    # Weapon-less fight strength will be 20% of fighters strength

class Combat:
    def __init__(self, player: Player, enemies: list):
        self.npc_fighters = enemies
        self.player_fighter = player
        self.npc_health = {}
        self.player_health = 0
        self.npc_weapons = []
        self.player_weapons = []
        self.fighting = True   # Start in a combat state
    def __combat_attack(self, fighter):
        """! Fighter carries out a 'bare-hands' attack

        @param fighter  The NPC/player object of the fighter

        @return Number of strength deducted from opponent
        """
        attack_strength = ATTACK_PROPORTIONALITY_CONSTANT * fighter.strength
        print(f'{fighter.name} dealt {attack_strength} points of damage')
        return attack_strength
    def __combat_use_inv(self, fighter, weapon):
        print('ERROR: Not implemented')
        pass
    def __combat_use_skill(self):
        print('ERROR: Not implemented')
        pass
    def __combat_run_away(self):
        print('Running away')
        self.fighting = False
        return True
    def __combat_action(self, action, fighter):
        if action == 1:
            damage = self.__combat_attack(fighter)
            return damage
        elif action == 2:
            pass
        elif action == 3:
            self.__combat_use_skill()
            pass
        elif action == 4:
            self.__combat_run_away()
            pass
        else:
            print('ERROR: Invalid combat action exception caught')
            return False
        
        damage = 0
        return False
    

    def fight(self):
        fighting = self.fighting
        fighters = self.npc_fighters
        player_fighter = self.player_fighter
        
        # Todo: figure out what initial fighter health should be; defaulting to strength for now
        self.player_health = player_fighter.health   
        for fighter in fighters:
            self.npc_health[fighter] = fighter.health

        print('Fight has started')
        while self.fighting:
            sleep(1)
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
                # disp({'player': self.player_fighter.display_stats}) 
                # Start the player turn
                print('COMBAT MENU: What do you want to do?  Enter action number:')
                print('(1)  ATTACK')
                print('(2)  USE INVENTORY ITEM')
                print('(3)  USE SKILL')
                print('(4)  RUN AWAY')
                action = int( input() )
                damage = self.__combat_action(action, self.player_fighter)
                self.npc_health[enemy_fighter] = self.npc_health[enemy_fighter] - damage
                fighter.health = self.npc_health[enemy_fighter]

                if self.npc_health[enemy_fighter] < 0:
                    print(f'{enemy_fighter.name} HAS DIED')
                    fighters.remove(enemy_fighter)
                if self.fighting == False:
                    break

        print('Fight has concluded')
        return True

    


    