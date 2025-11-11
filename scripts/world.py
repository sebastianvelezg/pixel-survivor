"""
World class - manages world data and progression
"""
import pygame


class World:
    """
    Manages world state, progression, and world-specific properties
    """

    def __init__(self, world_data):
        """
        Initialize world

        Args:
            world_data (dict): World configuration from settings.json
        """
        self.world_id = world_data['world']
        self.name = f"World {self.world_id}"
        self.description = f"Complete {world_data['rounds']} rounds to progress"
        self.rounds_to_complete = world_data['rounds']

        # Generate theme colors based on world ID
        base_hue = (self.world_id - 1) * 36  # Different color per world
        self.bg_color = self._generate_bg_color(self.world_id)
        self.accent_color = self._generate_accent_color(self.world_id)

        # Enemy modifiers for this world
        self.enemy_hp_multiplier = world_data['enemy_health_multiplier']
        self.enemy_speed_multiplier = world_data['enemy_speed_multiplier']
        self.enemy_damage_multiplier = world_data.get('enemy_damage_multiplier', 1.0)

        # Progression tracking
        self.rounds_completed = 0
        self.is_complete = False

    def _generate_bg_color(self, world_id):
        """Generate background color based on world ID"""
        colors = [
            (30, 30, 40),      # World 1 - Dark blue
            (40, 25, 35),      # World 2 - Dark purple
            (25, 35, 25),      # World 3 - Dark green
            (40, 30, 20),      # World 4 - Dark brown
            (35, 35, 40),      # World 5 - Dark gray
            (40, 20, 20),      # World 6 - Dark red
            (20, 30, 40),      # World 7 - Deep blue
            (35, 25, 40),      # World 8 - Purple
            (40, 40, 25),      # World 9 - Olive
            (25, 25, 35),      # World 10 - Dark slate
        ]
        return colors[(world_id - 1) % len(colors)]

    def _generate_accent_color(self, world_id):
        """Generate accent color based on world ID"""
        colors = [
            (100, 200, 255),   # World 1 - Cyan
            (200, 100, 255),   # World 2 - Purple
            (100, 255, 100),   # World 3 - Green
            (255, 180, 100),   # World 4 - Orange
            (200, 200, 255),   # World 5 - Light blue
            (255, 100, 100),   # World 6 - Red
            (100, 180, 255),   # World 7 - Sky blue
            (255, 100, 200),   # World 8 - Pink
            (255, 255, 100),   # World 9 - Yellow
            (180, 180, 255),   # World 10 - Lavender
        ]
        return colors[(world_id - 1) % len(colors)]

    def complete_round(self):
        """
        Mark a round as completed and check if world is complete

        Returns:
            bool: True if world is now complete
        """
        self.rounds_completed += 1

        if self.rounds_completed >= self.rounds_to_complete:
            self.is_complete = True
            return True

        return False

    def get_progress_percentage(self):
        """
        Get completion progress as percentage

        Returns:
            float: Progress percentage (0-100)
        """
        return (self.rounds_completed / self.rounds_to_complete) * 100

    def apply_enemy_modifiers(self, base_stats):
        """
        Apply world-specific modifiers to enemy stats

        Args:
            base_stats (dict): Base enemy stats (hp, speed, damage)

        Returns:
            dict: Modified enemy stats
        """
        return {
            'hp': int(base_stats['hp'] * self.enemy_hp_multiplier),
            'speed': base_stats['speed'] * self.enemy_speed_multiplier,
            'damage': int(base_stats['damage'] * self.enemy_damage_multiplier)
        }

    def get_info(self):
        """
        Get world information for display

        Returns:
            dict: World information (name, progress, rounds remaining)
        """
        return {
            'id': self.world_id,
            'name': self.name,
            'description': self.description,
            'rounds_completed': self.rounds_completed,
            'rounds_remaining': self.rounds_to_complete - self.rounds_completed,
            'progress': self.get_progress_percentage(),
            'is_complete': self.is_complete
        }

    def reset(self):
        """Reset world progress"""
        self.rounds_completed = 0
        self.is_complete = False


class WorldManager:
    """
    Manages progression through multiple worlds
    """

    def __init__(self, worlds_config):
        """
        Initialize world manager

        Args:
            worlds_config (list): List of world configurations from settings.json
        """
        self.worlds = [World(world_data) for world_data in worlds_config]
        self.current_world_index = 0
        self.current_world = self.worlds[0]

    def complete_round(self):
        """
        Complete a round in current world and check progression

        Returns:
            bool: True if advanced to next world
        """
        world_complete = self.current_world.complete_round()

        if world_complete:
            return self.advance_to_next_world()

        return False

    def advance_to_next_world(self):
        """
        Advance to next world

        Returns:
            bool: True if advanced successfully, False if no more worlds
        """
        if self.current_world_index < len(self.worlds) - 1:
            self.current_world_index += 1
            self.current_world = self.worlds[self.current_world_index]
            return True

        return False

    def get_current_world_info(self):
        """
        Get current world information

        Returns:
            dict: Current world info
        """
        return self.current_world.get_info()

    def is_all_worlds_complete(self):
        """
        Check if all worlds are complete

        Returns:
            bool: True if all worlds completed
        """
        return self.current_world_index == len(self.worlds) - 1 and self.current_world.is_complete

    def apply_enemy_modifiers(self, base_stats):
        """
        Apply current world's enemy modifiers

        Args:
            base_stats (dict): Base enemy stats

        Returns:
            dict: Modified stats for current world
        """
        return self.current_world.apply_enemy_modifiers(base_stats)

    def get_background_color(self):
        """
        Get current world's background color

        Returns:
            tuple: RGB color tuple
        """
        return self.current_world.bg_color

    def get_accent_color(self):
        """
        Get current world's accent color

        Returns:
            tuple: RGB color tuple
        """
        return self.current_world.accent_color

    def reset(self):
        """Reset all worlds"""
        for world in self.worlds:
            world.reset()
        self.current_world_index = 0
        self.current_world = self.worlds[0]
