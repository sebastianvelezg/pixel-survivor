"""
Player class - handles player attributes and behavior
"""
import pygame
import math


class Player:
    """
    Player character with WASD movement and mouse aiming
    """

    def __init__(self, x, y, config):
        """
        Initialize player

        Args:
            x (int): Starting x position
            y (int): Starting y position
            config (dict): Player configuration from settings.json
        """
        self.x = x
        self.y = y
        self.speed = config.get('speed', 5)
        self.max_hp = config.get('max_hp', 100)
        self.hp = self.max_hp
        self.damage = config.get('damage', 10)

        # Powerup state
        self.has_shield = False
        self.is_invincible = False

        # Visual properties
        self.size = 32  # 32x32 pixel square for now
        self.color = (0, 150, 255)  # Blue player
        self.angle = 0  # Angle in radians (0 = facing right)

        # Movement
        self.rect = pygame.Rect(self.x - self.size // 2,
                                self.y - self.size // 2,
                                self.size, self.size)

    def update(self, keys, mouse_pos, screen_width, screen_height, dt):
        """
        Update player position and rotation

        Args:
            keys: Pygame key pressed states
            mouse_pos (tuple): Mouse x, y position
            screen_width (int): Screen width for boundary checking
            screen_height (int): Screen height for boundary checking
            dt (float): Delta time for frame-independent movement
        """
        # WASD movement
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        # Apply movement with delta time
        self.x += dx * self.speed * dt * 60  # Multiply by 60 for 60 FPS baseline
        self.y += dy * self.speed * dt * 60

        # Boundary checking - keep player within screen
        half_size = self.size // 2
        self.x = max(half_size, min(screen_width - half_size, self.x))
        self.y = max(half_size, min(screen_height - half_size, self.y))

        # Update rect position
        self.rect.x = self.x - half_size
        self.rect.y = self.y - half_size

        # Rotate player to face mouse cursor
        mouse_x, mouse_y = mouse_pos
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.atan2(dy, dx)

    def draw(self, screen):
        """
        Draw player to screen

        Args:
            screen: Pygame screen surface
        """
        # Change color based on powerup state
        draw_color = self.color
        if self.is_invincible:
            draw_color = (255, 255, 100)  # Yellow when invincible
        elif self.has_shield:
            draw_color = (100, 255, 255)  # Cyan when shielded

        # Draw body (blue square)
        pygame.draw.rect(screen, draw_color, self.rect)

        # Draw shield indicator
        if self.has_shield and not self.is_invincible:
            shield_rect = pygame.Rect(
                self.rect.x - 4,
                self.rect.y - 4,
                self.rect.width + 8,
                self.rect.height + 8
            )
            pygame.draw.rect(screen, (100, 255, 255), shield_rect, 2)

        # Draw direction indicator (line showing where player is facing)
        end_x = self.x + math.cos(self.angle) * self.size
        end_y = self.y + math.sin(self.angle) * self.size
        pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (end_x, end_y), 3)

        # Draw center dot
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

    def take_damage(self, amount):
        """
        Apply damage to player

        Args:
            amount (int): Damage amount

        Returns:
            bool: True if player is still alive
        """
        # Invincibility blocks all damage
        if self.is_invincible:
            return True

        # Shield blocks first hit
        if self.has_shield:
            self.has_shield = False  # Shield breaks after one hit
            return True

        self.hp = max(0, self.hp - amount)
        return self.hp > 0

    def heal(self, amount):
        """
        Heal player

        Args:
            amount (int): Heal amount
        """
        self.hp = min(self.max_hp, self.hp + amount)
