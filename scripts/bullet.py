"""
Bullet class - handles projectiles fired by player
"""
import pygame
import math


class Bullet:
    """
    Projectile fired by the player
    """

    def __init__(self, x, y, angle, speed=400, damage=10):
        """
        Initialize bullet

        Args:
            x (float): Starting x position
            y (float): Starting y position
            angle (float): Direction angle in radians
            speed (float): Bullet speed in pixels/second
            damage (int): Damage dealt to enemies
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage

        # Visual properties
        self.radius = 4
        self.color = (255, 255, 100)  # Yellow bullet

        # Calculate velocity components
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        # Create rect for collision
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                self.radius * 2, self.radius * 2)

    def update(self, dt):
        """
        Update bullet position

        Args:
            dt (float): Delta time in seconds
        """
        # Move bullet
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Update rect
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def is_off_screen(self, screen_width, screen_height):
        """
        Check if bullet is off screen

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height

        Returns:
            bool: True if bullet is outside screen bounds
        """
        return (self.x < -10 or self.x > screen_width + 10 or
                self.y < -10 or self.y > screen_height + 10)

    def draw(self, screen):
        """
        Draw bullet to screen

        Args:
            screen: Pygame screen surface
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw a small glow effect
        pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(self.y)), self.radius - 1)
