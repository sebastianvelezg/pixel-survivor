"""
Weapon class - defines weapon stats and behavior
"""
import math
from bullet import Bullet


class Weapon:
    """
    Base weapon class with different types and behaviors
    """

    def __init__(self, weapon_type="PISTOL"):
        """
        Initialize weapon

        Args:
            weapon_type (str): Type of weapon (PISTOL, SHOTGUN, RIFLE, PLASMA_GUN)
        """
        self.weapon_type = weapon_type
        self.cooldown_timer = 0

        # Set weapon-specific stats
        if weapon_type == "PISTOL":
            self.name = "Pistol"
            self.damage = 10
            self.fire_rate = 0.15  # Seconds between shots
            self.bullet_speed = 400
            self.bullet_count = 1
            self.spread_angle = 0
            self.color = (255, 255, 100)  # Yellow

        elif weapon_type == "SHOTGUN":
            self.name = "Shotgun"
            self.damage = 8
            self.fire_rate = 0.8  # Slow fire rate
            self.bullet_speed = 350
            self.bullet_count = 5  # Shoots 5 bullets
            self.spread_angle = 0.3  # Spread in radians
            self.color = (255, 150, 50)  # Orange

        elif weapon_type == "RIFLE":
            self.name = "Rifle"
            self.damage = 25
            self.fire_rate = 0.5  # Medium fire rate
            self.bullet_speed = 600
            self.bullet_count = 1
            self.spread_angle = 0
            self.color = (100, 255, 100)  # Green

        elif weapon_type == "PLASMA_GUN":
            self.name = "Plasma Gun"
            self.damage = 15
            self.fire_rate = 0.25
            self.bullet_speed = 450
            self.bullet_count = 2  # Shoots 2 bullets
            self.spread_angle = 0.1
            self.color = (150, 100, 255)  # Purple

        else:
            # Default to pistol
            self.name = "Pistol"
            self.damage = 10
            self.fire_rate = 0.15
            self.bullet_speed = 400
            self.bullet_count = 1
            self.spread_angle = 0
            self.color = (255, 255, 100)

    def update(self, dt):
        """
        Update weapon cooldown

        Args:
            dt (float): Delta time in seconds
        """
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

    def can_fire(self):
        """
        Check if weapon can fire

        Returns:
            bool: True if cooldown is finished
        """
        return self.cooldown_timer <= 0

    def shoot(self, x, y, angle):
        """
        Create bullets when firing

        Args:
            x (float): Starting x position
            y (float): Starting y position
            angle (float): Direction angle in radians

        Returns:
            list: List of Bullet objects
        """
        if not self.can_fire():
            return []

        bullets = []

        if self.bullet_count == 1:
            # Single bullet
            bullet = Bullet(x, y, angle, speed=self.bullet_speed, damage=self.damage)
            bullet.color = self.color
            bullets.append(bullet)

        else:
            # Multiple bullets with spread
            for i in range(self.bullet_count):
                # Calculate spread offset
                offset = (i - (self.bullet_count - 1) / 2) * self.spread_angle
                bullet_angle = angle + offset

                bullet = Bullet(x, y, bullet_angle, speed=self.bullet_speed, damage=self.damage)
                bullet.color = self.color
                bullets.append(bullet)

        # Reset cooldown
        self.cooldown_timer = self.fire_rate

        return bullets

    def get_display_info(self):
        """
        Get weapon info for UI display

        Returns:
            dict: Weapon display information
        """
        return {
            'name': self.name,
            'damage': self.damage,
            'fire_rate': self.fire_rate,
            'color': self.color,
            'ready': self.can_fire()
        }


def create_weapon(weapon_type):
    """
    Factory function to create weapons

    Args:
        weapon_type (str): Type of weapon to create

    Returns:
        Weapon: New weapon instance
    """
    return Weapon(weapon_type)
