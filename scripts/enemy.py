"""
Enemy class - handles enemy behavior and AI
"""
import pygame
import math
import random


class Enemy:
    """
    Enemy that chases and attacks the player
    """

    def __init__(self, x, y, speed=80, hp=30, damage=10):
        """
        Initialize enemy

        Args:
            x (float): Starting x position
            y (float): Starting y position
            speed (float): Movement speed in pixels/second
            hp (int): Health points
            damage (int): Damage dealt to player on collision
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.damage = damage

        # Visual properties
        self.size = 28
        self.color = (255, 50, 50)  # Red enemy
        self.alive = True

        # Create rect for collision
        self.rect = pygame.Rect(x - self.size // 2, y - self.size // 2,
                                self.size, self.size)

        # Collision cooldown to prevent instant multi-hits
        self.attack_cooldown = 0
        self.attack_rate = 1.0  # Can attack once per second

    def update(self, player_pos, dt):
        """
        Update enemy position - chase player

        Args:
            player_pos (tuple): Player's (x, y) position
            dt (float): Delta time in seconds
        """
        if not self.alive:
            return

        # Calculate direction to player
        player_x, player_y = player_pos
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        # Move toward player if not too close
        if distance > 1:
            # Normalize direction and apply movement
            dx /= distance
            dy /= distance
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

        # Update rect position
        self.rect.x = self.x - self.size // 2
        self.rect.y = self.y - self.size // 2

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def take_damage(self, amount):
        """
        Apply damage to enemy

        Args:
            amount (int): Damage amount

        Returns:
            bool: True if enemy died from this damage
        """
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def drop_loot(self):
        """
        Generate random loot drop on death

        Returns:
            Drop or None: Random drop based on rarity
        """
        from drop import create_random_drop
        import random

        # 70% chance to drop something
        if random.random() < 0.7:
            return create_random_drop(self.x, self.y)

        return None

    def can_attack(self):
        """
        Check if enemy can attack (cooldown finished)

        Returns:
            bool: True if enemy can attack
        """
        return self.attack_cooldown <= 0

    def attack_player(self, player):
        """
        Attack player on collision

        Args:
            player: Player object

        Returns:
            bool: True if attack was successful
        """
        if self.can_attack() and self.alive:
            player.take_damage(self.damage)
            self.attack_cooldown = self.attack_rate
            return True
        return False

    def draw(self, screen):
        """
        Draw enemy to screen

        Args:
            screen: Pygame screen surface
        """
        if not self.alive:
            return

        # Draw body (red square)
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw darker border
        pygame.draw.rect(screen, (180, 30, 30), self.rect, 2)

        # Draw HP bar above enemy
        if self.hp < self.max_hp:
            bar_width = self.size
            bar_height = 4
            bar_x = self.rect.x
            bar_y = self.rect.y - 8

            # Background (red)
            pygame.draw.rect(screen, (100, 0, 0),
                           (bar_x, bar_y, bar_width, bar_height))

            # Foreground (green) based on HP percentage
            hp_percentage = self.hp / self.max_hp
            pygame.draw.rect(screen, (0, 255, 0),
                           (bar_x, bar_y, int(bar_width * hp_percentage), bar_height))


def spawn_enemy_at_edge(screen_width, screen_height, speed=80, hp=30, damage=10):
    """
    Spawn an enemy at a random edge of the screen

    Args:
        screen_width (int): Screen width
        screen_height (int): Screen height
        speed (float): Enemy speed
        hp (int): Enemy health
        damage (int): Enemy damage

    Returns:
        Enemy: New enemy instance
    """
    edge = random.choice(['top', 'bottom', 'left', 'right'])

    if edge == 'top':
        x = random.randint(0, screen_width)
        y = -20
    elif edge == 'bottom':
        x = random.randint(0, screen_width)
        y = screen_height + 20
    elif edge == 'left':
        x = -20
        y = random.randint(0, screen_height)
    else:  # right
        x = screen_width + 20
        y = random.randint(0, screen_height)

    return Enemy(x, y, speed, hp, damage)
