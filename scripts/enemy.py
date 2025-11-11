"""
Enemy class - handles enemy behavior and AI
"""
import pygame
import math
import random


class Enemy:
    """
    Basic enemy that chases the player
    """

    def __init__(self, x, y, hp=30, speed=2, damage=10):
        """
        Initialize enemy

        Args:
            x (float): Starting x position
            y (float): Starting y position
            hp (int): Health points
            speed (float): Movement speed
            damage (int): Damage dealt to player
        """
        self.x = x
        self.y = y
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.size = 28

        # Visual properties
        self.color = (255, 50, 50)  # Red enemy
        self.border_color = (150, 0, 0)

        # Collision rect
        self.rect = pygame.Rect(self.x - self.size // 2,
                               self.y - self.size // 2,
                               self.size, self.size)

        # Animation
        self.wobble = random.uniform(0, math.pi * 2)

    def move_toward_player(self, player_x, player_y, dt):
        """
        Move enemy toward player position (simple chase AI)

        Args:
            player_x (float): Player x position
            player_y (float): Player y position
            dt (float): Delta time
        """
        # Calculate direction to player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance

            # Move toward player
            self.x += dx * self.speed * dt * 60
            self.y += dy * self.speed * dt * 60

        # Update rect position
        self.rect.x = self.x - self.size // 2
        self.rect.y = self.y - self.size // 2

        # Update wobble animation
        self.wobble += dt * 5

    def take_damage(self, amount):
        """
        Apply damage to enemy

        Args:
            amount (int): Damage amount

        Returns:
            bool: True if enemy is still alive
        """
        self.hp = max(0, self.hp - amount)
        return self.hp > 0

    def attack_player(self, player):
        """
        Deal damage to player on collision

        Args:
            player: Player object

        Returns:
            bool: True if attack was successful
        """
        return player.take_damage(self.damage)

    def draw(self, screen):
        """
        Draw enemy to screen

        Args:
            screen: Pygame screen surface
        """
        # Wobble effect for animation
        wobble_offset = int(math.sin(self.wobble) * 2)

        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect)

        # Draw body
        body_rect = self.rect.copy()
        body_rect.y += wobble_offset
        pygame.draw.rect(screen, self.color, body_rect)

        # Draw border
        pygame.draw.rect(screen, self.border_color, body_rect, 2)

        # Draw eyes (to make it look menacing)
        eye_y = int(self.y - 4 + wobble_offset)
        eye_size = 4
        left_eye_x = int(self.x - 6)
        right_eye_x = int(self.x + 6)

        # White of eyes
        pygame.draw.circle(screen, (255, 255, 255), (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), (right_eye_x, eye_y), eye_size)

        # Pupils
        pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, eye_y), 2)
        pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, eye_y), 2)

        # Draw HP bar above enemy
        self.draw_hp_bar(screen)

    def draw_hp_bar(self, screen):
        """
        Draw HP bar above enemy

        Args:
            screen: Pygame screen surface
        """
        bar_width = self.size
        bar_height = 4
        bar_x = self.rect.x
        bar_y = self.rect.y - 8

        # Background (red)
        pygame.draw.rect(screen, (100, 0, 0),
                        (bar_x, bar_y, bar_width, bar_height))

        # Foreground (current HP - green to red gradient)
        hp_percentage = self.hp / self.max_hp
        current_bar_width = int(bar_width * hp_percentage)

        if hp_percentage > 0.5:
            bar_color = (0, 255, 0)  # Green
        elif hp_percentage > 0.25:
            bar_color = (255, 200, 0)  # Yellow
        else:
            bar_color = (255, 100, 0)  # Orange

        if current_bar_width > 0:
            pygame.draw.rect(screen, bar_color,
                            (bar_x, bar_y, current_bar_width, bar_height))

        # Border
        pygame.draw.rect(screen, (255, 255, 255),
                        (bar_x, bar_y, bar_width, bar_height), 1)

    @staticmethod
    def spawn_at_edge(screen_width, screen_height):
        """
        Spawn enemy at random screen edge

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height

        Returns:
            tuple: (x, y) spawn position
        """
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            return random.randint(0, screen_width), -20
        elif edge == 'bottom':
            return random.randint(0, screen_width), screen_height + 20
        elif edge == 'left':
            return -20, random.randint(0, screen_height)
        else:  # right
            return screen_width + 20, random.randint(0, screen_height)
