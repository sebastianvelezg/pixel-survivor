"""
SaveManager class - handles saving and loading game data
"""
import json
import os
from datetime import datetime


class SaveManager:
    """
    Manages game save/load functionality with JSON persistence
    """

    def __init__(self, save_directory="saves"):
        """
        Initialize save manager

        Args:
            save_directory (str): Directory to store save files
        """
        self.save_directory = save_directory
        self.save_file = os.path.join(save_directory, "player_progress.json")

        # Ensure save directory exists
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

    def has_save(self):
        """
        Check if a save file exists

        Returns:
            bool: True if save file exists
        """
        return os.path.exists(self.save_file)

    def save_game(self, game_data):
        """
        Save game data to JSON file

        Args:
            game_data (dict): Complete game state to save
                Expected keys:
                - world_number: Current world (1-10)
                - round_number: Current round
                - player: Player data (hp, max_hp, speed, damage)
                - inventory: Inventory data (weapons, coins)
                - kills: Total kill count
                - timestamp: Save timestamp
                - playtime: Total time played in seconds

        Returns:
            bool: True if save successful
        """
        try:
            # Add timestamp and version info
            game_data['save_version'] = '1.0'
            game_data['timestamp'] = datetime.now().isoformat()

            # Write to file with pretty formatting
            with open(self.save_file, 'w') as f:
                json.dump(game_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self):
        """
        Load game data from JSON file

        Returns:
            dict or None: Game data if successful, None otherwise
        """
        if not self.has_save():
            return None

        try:
            with open(self.save_file, 'r') as f:
                game_data = json.load(f)

            # Validate save data has required keys
            required_keys = ['world_number', 'round_number', 'player', 'inventory']
            if not all(key in game_data for key in required_keys):
                print("Save file is corrupted or incomplete")
                return None

            return game_data

        except json.JSONDecodeError as e:
            print(f"Error parsing save file: {e}")
            return None
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def delete_save(self):
        """
        Delete the save file

        Returns:
            bool: True if deletion successful or file didn't exist
        """
        try:
            if self.has_save():
                os.remove(self.save_file)
            return True
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False

    def get_save_info(self):
        """
        Get information about the save file without loading it fully

        Returns:
            dict or None: Save metadata (world, round, timestamp, kills)
        """
        if not self.has_save():
            return None

        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)

            return {
                'world_number': data.get('world_number', 1),
                'round_number': data.get('round_number', 1),
                'timestamp': data.get('timestamp', 'Unknown'),
                'kills': data.get('kills', 0),
                'playtime': data.get('playtime', 0)
            }

        except Exception as e:
            print(f"Error reading save info: {e}")
            return None


def create_save_data(player, inventory, world_manager, round_manager, kills, playtime=0):
    """
    Create a save data dictionary from game objects

    Args:
        player: Player object
        inventory: Inventory object
        world_manager: WorldManager object
        round_manager: RoundManager object
        kills (int): Total kills
        playtime (float): Total playtime in seconds

    Returns:
        dict: Save data dictionary
    """
    # Collect weapon types from inventory
    weapon_types = []
    for weapon in inventory.weapons:
        if weapon:
            weapon_types.append(weapon.weapon_type)
        else:
            weapon_types.append(None)

    # Collect upgrade purchase counts from upgrade shop (if tracking)
    # This would need to be passed in or stored in player/inventory

    save_data = {
        'world_number': world_manager.current_world_index + 1,  # 1-indexed for user
        'round_number': round_manager.current_round,

        'player': {
            'hp': player.hp,
            'max_hp': player.max_hp,
            'speed': player.speed,
            'damage': player.damage,
            'x': player.x,
            'y': player.y
        },

        'inventory': {
            'weapons': weapon_types,
            'active_weapon_index': inventory.active_weapon_index,
            'coins': inventory.coins
        },

        'world_progress': {
            'current_world_index': world_manager.current_world_index,
            'rounds_completed': world_manager.current_world.rounds_completed
        },

        'round_state': {
            'current_round': round_manager.current_round,
            'enemies_per_round': round_manager.enemies_per_round
        },

        'stats': {
            'kills': kills,
            'playtime': playtime
        }
    }

    return save_data


def restore_from_save(save_data, player, inventory, world_manager, round_manager):
    """
    Restore game state from save data

    Args:
        save_data (dict): Loaded save data
        player: Player object to restore
        inventory: Inventory object to restore
        world_manager: WorldManager object to restore
        round_manager: RoundManager object to restore

    Returns:
        int: Total kills from save
    """
    # Restore player
    player_data = save_data.get('player', {})
    player.hp = player_data.get('hp', player.max_hp)
    player.max_hp = player_data.get('max_hp', 100)
    player.speed = player_data.get('speed', 5)
    player.damage = player_data.get('damage', 10)
    player.x = player_data.get('x', player.x)
    player.y = player_data.get('y', player.y)

    # Restore inventory
    from weapon import create_weapon
    inventory_data = save_data.get('inventory', {})
    weapon_types = inventory_data.get('weapons', ["PISTOL", None, None])

    for i, weapon_type in enumerate(weapon_types):
        if weapon_type:
            inventory.weapons[i] = create_weapon(weapon_type)
        else:
            inventory.weapons[i] = None

    inventory.active_weapon_index = inventory_data.get('active_weapon_index', 0)
    inventory.coins = inventory_data.get('coins', 0)

    # Restore world progress
    world_progress = save_data.get('world_progress', {})
    world_index = world_progress.get('current_world_index', 0)
    world_manager.current_world_index = world_index
    world_manager.current_world = world_manager.worlds[world_index]
    world_manager.current_world.rounds_completed = world_progress.get('rounds_completed', 0)

    # Restore round state
    round_state = save_data.get('round_state', {})
    round_manager.current_round = round_state.get('current_round', 1)
    round_manager.enemies_per_round = round_state.get('enemies_per_round', 5)

    # Return stats
    stats = save_data.get('stats', {})
    return stats.get('kills', 0)
