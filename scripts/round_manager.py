"""
Round Manager - handles round-based enemy spawning and progression
"""
import pygame


class RoundManager:
    """
    Manages rounds, enemy spawning waves, and round progression
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize round manager

        Args:
            screen_width (int): Screen width for spawning
            screen_height (int): Screen height for spawning
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Round state
        self.current_round = 1
        self.enemies_per_round = 5
        self.enemies_spawned_this_round = 0
        self.round_active = False
        self.round_complete = False

        # Spawning
        self.spawn_timer = 0
        self.spawn_interval = 1.5  # Spawn enemy every 1.5 seconds during round

        # Difficulty scaling
        self.base_enemy_hp = 30
        self.base_enemy_speed = 80
        self.base_enemy_damage = 10
        self.hp_scale = 1.15  # 15% HP increase per round
        self.speed_scale = 1.05  # 5% speed increase per round
        self.damage_scale = 1.10  # 10% damage increase per round

        # Break between rounds
        self.break_timer = 0
        self.break_duration = 3.0  # 3 seconds between rounds

    def start_round(self):
        """Start a new round"""
        self.round_active = True
        self.round_complete = False
        self.enemies_spawned_this_round = 0
        self.spawn_timer = 0

    def update(self, dt, active_enemies_count):
        """
        Update round manager

        Args:
            dt (float): Delta time in seconds
            active_enemies_count (int): Number of enemies currently alive

        Returns:
            dict or None: Enemy spawn parameters if should spawn, None otherwise
        """
        # If in break between rounds
        if not self.round_active:
            self.break_timer -= dt
            if self.break_timer <= 0:
                self.start_round()
            return None

        # Check if round is complete
        if self.enemies_spawned_this_round >= self.enemies_per_round and active_enemies_count == 0:
            self.complete_round()
            return None

        # Spawn enemies during active round
        if self.enemies_spawned_this_round < self.enemies_per_round:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.enemies_spawned_this_round += 1
                self.spawn_timer = self.spawn_interval

                # Return enemy spawn parameters with scaled difficulty
                return self.get_enemy_stats()

        return None

    def complete_round(self):
        """Complete current round and prepare for next"""
        self.round_complete = True
        self.round_active = False
        self.current_round += 1

        # Increase enemies per round
        self.enemies_per_round += 2  # Add 2 more enemies each round

        # Start break timer
        self.break_timer = self.break_duration

    def get_enemy_stats(self):
        """
        Calculate enemy stats based on current round

        Returns:
            dict: Enemy stats (speed, hp, damage)
        """
        rounds_passed = self.current_round - 1

        return {
            'speed': self.base_enemy_speed * (self.speed_scale ** rounds_passed),
            'hp': int(self.base_enemy_hp * (self.hp_scale ** rounds_passed)),
            'damage': int(self.base_enemy_damage * (self.damage_scale ** rounds_passed))
        }

    def get_round_info(self):
        """
        Get current round information for display

        Returns:
            dict: Round information (round number, enemies remaining, break time)
        """
        enemies_remaining = self.enemies_per_round - self.enemies_spawned_this_round

        return {
            'round': self.current_round,
            'enemies_remaining': max(0, enemies_remaining),
            'in_break': not self.round_active,
            'break_time': max(0, self.break_timer)
        }

    def reset(self):
        """Reset round manager to initial state"""
        self.current_round = 1
        self.enemies_per_round = 5
        self.enemies_spawned_this_round = 0
        self.round_active = False
        self.round_complete = False
        self.spawn_timer = 0
        self.break_timer = 0
