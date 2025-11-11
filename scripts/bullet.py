"""
Bullet class - handles projectile behavior
"""
import pygame
import math


class Bullet:
    """
    Projectile fired by player or enemies
    """

    def __init__(self, x, y, angle, speed=10, damage=10, color=(255, 255, 100)):
        """
        Initialize bullet

        Args:
            x (float): Starting x position
            y (float): Starting y position
            angle (float): Direction in radians
            speed (float): Bullet speed
            damage (int): Damage dealt
            color (tuple): RGB color
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.color = color
        self.radius = 4

        # Calculate velocity components
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        # Trail effect
        self.trail = []
        self.max_trail_length = 5

    def update(self, dt):
        """
        Update bullet position

        Args:
            dt (float): Delta time
        """
        # Move bullet
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def is_off_screen(self, screen_width, screen_height, margin=50):
        """
        Check if bullet is off screen

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
            margin (int): Extra margin to check

        Returns:
            bool: True if bullet is off screen
        """
        return (self.x < -margin or
                self.x > screen_width + margin or
                self.y < -margin or
                self.y > screen_height + margin)

    def draw(self, screen):
        """
        Draw bullet with trail effect

        Args:
            screen: Pygame screen surface
        """
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)  # Fade effect
            trail_radius = int(self.radius * alpha)
            trail_color = tuple(int(c * alpha) for c in self.color)
            pygame.draw.circle(screen, trail_color, (int(tx), int(ty)), trail_radius)

        # Draw main bullet
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # Draw glow/outline
        glow_color = (255, 255, 255)
        pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), self.radius + 1, 1)

    def get_rect(self):
        """
        Get collision rectangle

        Returns:
            pygame.Rect: Collision rect
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

    def collides_with(self, rect):
        """
        Check collision with a rectangle

        Args:
            rect (pygame.Rect): Rectangle to check

        Returns:
            bool: True if collision detected
        """
        # Simple circle-rectangle collision
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))

        distance_x = self.x - closest_x
        distance_y = self.y - closest_y

        distance_squared = (distance_x ** 2) + (distance_y ** 2)

        return distance_squared < (self.radius ** 2)
