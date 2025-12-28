import random
import json
import os
import time


class PermanentUpgrades:
    """Manages permanent upgrades bought with gold"""
    
    def __init__(self):
        self.bomb_slots = 0
        self.bomb_damage = 0
        self.max_health = 0
        self.damage_reduction = 0
        self.explosion_range = 0
        
    def to_dict(self):
        return {
            'bomb_slots': self.bomb_slots,
            'bomb_damage': self.bomb_damage,
            'max_health': self.max_health,
            'damage_reduction': self.damage_reduction,
            'explosion_range': self.explosion_range
        }
    
    def from_dict(self, data):
        self.bomb_slots = data.get('bomb_slots', 0)
        self.bomb_damage = data.get('bomb_damage', 0)
        self.max_health = data.get('max_health', 0)
        self.damage_reduction = data.get('damage_reduction', 0)
        self.explosion_range = data.get('explosion_range', 0)

  
class Player:
    def __init__(self):
        self.max_hp = 100
        self.hp = 100
        self.gold = 0
        self.score = 0

    
        self.temp_upgrades = {
            "bomb_damage": 0,
            "bomb_range": 0,
            "bomb_slots": 0,
            "damage_reduction": 0
        }


  self.perm_upgrades = {
            "bomb_damage": 0,
            "bomb_range": 0,
            "bomb_slots": 0,
            "damage_reduction": 0
        }

    def reset_temp_upgrades(self):
        for k in self.temp_upgrades:
            self.temp_upgrades[k] = 0

    def is_dead(self):
        return self.hp <= 0




class Upgrade:
    """Represents a single upgrade option"""
    
    def __init__(self, name, description, effect_func):
        self.name = name
        self.description = description
        self.effect_func = effect_func
    
    def apply(self, player_stats):
        self.effect_func(player_stats)




class Enemy:
    def __init__(self, hp):
        self.hp = hp

    def take_damage(self, dmg):
        self.hp -= dmg
        return self.hp <= 0




class WaveManager:
    """Manages wave progression and enemy spawning"""
    
    def __init__(self):
        self.current_wave = 0
        self.max_waves = 10
        self.enemies_per_wave = 5
        self.enemies_killed = 0
        self.total_enemies_in_wave = self.enemies_per_wave
        
    def start_new_wave(self):
        self.current_wave += 1
        self.enemies_killed = 0
        self.total_enemies_in_wave = self.enemies_per_wave
        return self.current_wave
    
    def enemy_killed(self):
        self.enemies_killed += 1
        return self.is_wave_complete()
    
    def is_wave_complete(self):
        return self.enemies_killed >= self.total_enemies_in_wave
    
    def is_game_won(self):
        return self.current_wave >= self.max_waves
    
    def get_enemy_hp_multiplier(self):
        return 1 + (self.current_wave - 1) * 0.3
    
    def get_remaining_enemies(self):
        return self.total_enemies_in_wave - self.enemies_killed


def handle_wave_clear(player, wave_manager):
    print("Wave cleared!")

    player.score += 100 * wave_manager.wave

    if wave_manager.wave >= wave_manager.max_waves:
        show_victory_screen(player, wave_manager.wave)
        return False  # game ends

    # Select upgrade (simulated)
    apply_upgrade(player)

    # Unfreeze game & start next wave
    wave_manager.next_wave()
    wave_manager.spawn_wave()
    return True




def create_enemies(wave):
    base_hp = 40
    hp = base_hp + (wave * 15)
    return [{"hp": hp} for _ in range(ENEMIES_PER_WAVE)]




def choose_upgrade():
    print("\nChoose an upgrade:")
    print("1. +1 Bomb Damage")
    print("2. +1 Bomb Range")

    choice = input("Enter choice: ")

    if choice == "1":
        player["temp_upgrades"]["bomb_damage"] += 1
        print("Bomb Damage upgraded!")
    elif choice == "2":
        player["temp_upgrades"]["bomb_range"] += 1
        print("Bomb Range upgraded!")





def show_victory():
    print("\n🏆 YOU WON THE GAME 🏆")
    print("You cleared all 10 waves!")
    print(f"Final Score: {player['score']}")



def handle_game_over(player, wave):
    gold_earned = wave * 10
    player.gold += gold_earned

    print("\n💀 GAME OVER 💀")
    print(f"Waves Cleared: {wave}")
    print(f"Score: {player.score}")
    print(f"Gold Earned: {gold_earned}")

    # Reset wave-based upgrades
    player.reset_temp_upgrades()

    input("Press ENTER to return to Main Menu...")




def shop():
    print("\n--- SHOP ---")
    print(f"Gold: {player['gold']}")
    print("1. Permanent Bomb Damage (+1) - 50 Gold")
    print("2. Back")

    choice = input("Choose: ")

    if choice == "1" and player["gold"] >= 50:
        player["gold"] -= 50
        player["perm_upgrades"]["bomb_damage"] += 1
        print("Permanent Bomb Damage Purchased!")




def main_menu():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Start Game")
        print("2. Shop")
        print("3. Endless Mode")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            run_game()
        elif choice == "2":
            permanent_shop()
        elif choice == "3":
            endless_mode()
        elif choice == "4":
            break




def endless_mode(player):
    print("\n--- ENDLESS MODE ---")
    wave = 1

    while not player.is_dead():
        enemy = Enemy(50 + wave * 5)
        enemy.take_damage(999)  # simulate kill
        player.score += 50
        wave += 1

    handle_game_over(player, wave)





if __name__ == "__main__":
    main_menu()
