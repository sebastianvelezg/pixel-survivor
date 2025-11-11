"""
Drop class - handles items that spawn in the world
"""
import pygame
import random
import math


class Drop:
    """
    Item drop that can be picked up by the player
    """

    # Drop types
    HEALTH_SMALL = "HEALTH_SMALL"
    HEALTH_MEDIUM = "HEALTH_MEDIUM"
    HEALTH_LARGE = "HEALTH_LARGE"
    WEAPON = "WEAPON"
    POWERUP = "POWERUP"
    COIN = "COIN"

    def __init__(self, x, y, drop_type, value=None):
        """
        Initialize drop

        Args:
            x (float): X position
            y (float): Y position
            drop_type (str): Type of drop
            value: Additional value (weapon type, powerup type, etc.)
        """
        self.x = x
        self.y = y
        self.drop_type = drop_type
        self.value = value

        # Visual properties
        self.size = 16
        self.pickup_radius = 25  # Player pickup range
        self.alive = True

        # Floating animation
        self.float_offset = 0
        self.float_speed = 2.0

        # Lifetime
        self.lifetime = 30.0  # Despawn after 30 seconds
        self.blink_time = 5.0  # Start blinking in last 5 seconds

        # Set color and heal amount based on type
        if drop_type == self.HEALTH_SMALL:
            self.color = (100, 255, 100)  # Light green
            self.heal_amount = 20
            self.name = "Small Health"

        elif drop_type == self.HEALTH_MEDIUM:
            self.color = (50, 200, 50)  # Green
            self.heal_amount = 40
            self.name = "Medium Health"

        elif drop_type == self.HEALTH_LARGE:
            self.color = (0, 255, 0)  # Bright green
            self.heal_amount = 75
            self.name = "Large Health"

        elif drop_type == self.WEAPON:
            self.color = (255, 180, 50)  # Orange
            self.name = f"Weapon: {value}"

        elif drop_type == self.POWERUP:
            self.color = (255, 100, 255)  # Magenta
            self.name = f"Powerup: {value}"

        elif drop_type == self.COIN:
            self.color = (255, 215, 0)  # Gold
            self.coin_value = value if value else 1
            self.name = f"Coin ({self.coin_value})"

        else:
            self.color = (200, 200, 200)
            self.name = "Unknown"

        # Create rect for collision
        self.rect = pygame.Rect(x - self.size // 2, y - self.size // 2,
                                self.size, self.size)

    def update(self, dt):
        """
        Update drop (floating animation, lifetime)

        Args:
            dt (float): Delta time in seconds
        """
        if not self.alive:
            return

        # Floating animation
        self.float_offset += self.float_speed * dt
        visual_y = self.y + math.sin(self.float_offset) * 3

        # Update rect position
        self.rect.y = visual_y - self.size // 2

        # Lifetime countdown
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def can_pickup(self, player_x, player_y):
        """
        Check if player is close enough to pick up

        Args:
            player_x (float): Player x position
            player_y (float): Player y position

        Returns:
            bool: True if within pickup radius
        """
        distance = math.hypot(player_x - self.x, player_y - self.y)
        return distance < self.pickup_radius

    def apply_to_player(self, player, inventory):
        """
        Apply drop effect to player

        Args:
            player: Player object
            inventory: Inventory object

        Returns:
            bool: True if successfully applied
        """
        if self.drop_type == self.HEALTH_SMALL:
            player.heal(self.heal_amount)
            return True

        elif self.drop_type == self.HEALTH_MEDIUM:
            player.heal(self.heal_amount)
            return True

        elif self.drop_type == self.HEALTH_LARGE:
            player.heal(self.heal_amount)
            return True

        elif self.drop_type == self.WEAPON:
            inventory.add_weapon(self.value)
            return True

        elif self.drop_type == self.POWERUP:
            from powerup import create_powerup
            powerup = create_powerup(self.value)
            inventory.add_powerup(powerup)
            return True

        elif self.drop_type == self.COIN:
            inventory.add_coins(self.coin_value)
            return True

        return False

    def draw(self, screen):
        """
        Draw drop to screen

        Args:
            screen: Pygame screen surface
        """
        if not self.alive:
            return

        # Blink effect when about to despawn
        if self.lifetime < self.blink_time:
            blink_speed = 5.0
            if int(self.lifetime * blink_speed) % 2 == 0:
                return

        # Draw drop as colored square
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw border
        border_color = tuple(max(0, c - 50) for c in self.color)
        pygame.draw.rect(screen, border_color, self.rect, 2)

        # Draw inner glow
        inner_rect = pygame.Rect(
            self.rect.x + 4,
            self.rect.y + 4,
            self.rect.width - 8,
            self.rect.height - 8
        )
        glow_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.rect(screen, glow_color, inner_rect)


def create_random_drop(x, y):
    """
    Create a random drop based on rarity table

    Args:
        x (float): X position
        y (float): Y position

    Returns:
        Drop: Random drop or None
    """
    # Rarity roll (0-100)
    roll = random.random() * 100

    # Common (60%): Small health or coins
    if roll < 60:
        if random.random() < 0.7:
            return Drop(x, y, Drop.HEALTH_SMALL)
        else:
            coin_value = random.randint(1, 3)
            return Drop(x, y, Drop.COIN, value=coin_value)

    # Uncommon (30%): Medium health or basic weapons
    elif roll < 90:
        if random.random() < 0.6:
            return Drop(x, y, Drop.HEALTH_MEDIUM)
        else:
            weapon_type = random.choice(["PISTOL", "SHOTGUN"])
            return Drop(x, y, Drop.WEAPON, value=weapon_type)

    # Rare (9%): Powerups, coins, or advanced weapons
    elif roll < 99:
        choice = random.random()
        if choice < 0.4:
            powerup_type = random.choice(["SPEED", "DAMAGE", "SHIELD"])
            return Drop(x, y, Drop.POWERUP, value=powerup_type)
        elif choice < 0.7:
            coin_value = random.randint(5, 10)
            return Drop(x, y, Drop.COIN, value=coin_value)
        else:
            weapon_type = random.choice(["RIFLE", "PLASMA_GUN"])
            return Drop(x, y, Drop.WEAPON, value=weapon_type)

    # Legendary (1%): Large health or best weapons
    else:
        if random.random() < 0.5:
            return Drop(x, y, Drop.HEALTH_LARGE)
        else:
            weapon_type = random.choice(["RIFLE", "PLASMA_GUN"])
            return Drop(x, y, Drop.WEAPON, value=weapon_type)
