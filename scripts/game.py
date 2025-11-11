"""
Game class - main game manager and core logic
"""
import pygame
import random
from scripts.player import Player
from scripts.bullet import Bullet
from scripts.enemy import Enemy


class Game:
    """
    Main game manager - handles game loop, collisions, spawning, and game states
    """

    def __init__(self, config, screen_width, screen_height):
        """
        Initialize game

        Args:
            config (dict): Game configuration
            screen_width (int): Screen width
            screen_height (int): Screen height
        """
        self.config = config
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Game state
        self.running = True
        self.game_over = False
        self.paused = False

        # Create player
        player_config = config['player']
        self.player = Player(screen_width // 2, screen_height // 2, player_config)

        # Game objects
        self.bullets = []
        self.enemies = []

        # Shooting
        self.shoot_cooldown = 0.2  # Seconds between shots
        self.last_shoot_time = 0

        # Enemy spawning
        self.spawn_timer = 0
        self.spawn_interval = 2.0  # Spawn enemy every 2 seconds
        self.max_enemies = 10  # Max enemies on screen

        # Stats
        self.kills = 0
        self.score = 0
        self.time_survived = 0

        # Damage cooldown (prevents instant death from multiple hits)
        self.damage_cooldown = 0.5  # Seconds of invincibility after hit
        self.last_damage_time = -10

    def handle_events(self, events):
        """
        Handle game events

        Args:
            events: Pygame events list
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    # Restart game
                    self.__init__(self.config, self.screen_width, self.screen_height)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.shoot()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot()

    def shoot(self):
        """
        Fire a bullet from player position in direction of mouse
        """
        current_time = pygame.time.get_ticks() / 1000.0

        if current_time - self.last_shoot_time >= self.shoot_cooldown:
            # Create bullet at player position, aimed at player angle
            bullet = Bullet(
                self.player.x,
                self.player.y,
                self.player.angle,
                speed=12,
                damage=self.player.damage
            )
            self.bullets.append(bullet)
            self.last_shoot_time = current_time

    def spawn_enemies(self, dt):
        """
        Spawn enemies at screen edges

        Args:
            dt (float): Delta time
        """
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_interval and len(self.enemies) < self.max_enemies:
            # Spawn enemy at random edge
            x, y = Enemy.spawn_at_edge(self.screen_width, self.screen_height)
            enemy = Enemy(x, y, hp=30, speed=2, damage=10)
            self.enemies.append(enemy)
            self.spawn_timer = 0

    def update(self, keys, mouse_pos, dt):
        """
        Update all game objects

        Args:
            keys: Pygame key states
            mouse_pos: Mouse position tuple
            dt (float): Delta time
        """
        if self.game_over or self.paused:
            return

        # Update time survived
        self.time_survived += dt

        # Update player
        self.player.update(keys, mouse_pos, self.screen_width, self.screen_height, dt)

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update(dt)

            # Remove bullets that are off screen
            if bullet.is_off_screen(self.screen_width, self.screen_height):
                self.bullets.remove(bullet)

        # Update enemies
        for enemy in self.enemies:
            enemy.move_toward_player(self.player.x, self.player.y, dt)

        # Spawn new enemies
        self.spawn_enemies(dt)

        # Check collisions
        self.check_collisions()

        # Check game over
        if self.player.hp <= 0:
            self.game_over = True

    def check_collisions(self):
        """
        Check all collision types
        """
        # Bullets vs Enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.collides_with(enemy.rect):
                    # Damage enemy
                    if not enemy.take_damage(bullet.damage):
                        # Enemy died
                        self.enemies.remove(enemy)
                        self.kills += 1
                        self.score += 100

                    # Remove bullet
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

        # Enemies vs Player
        current_time = pygame.time.get_ticks() / 1000.0

        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                # Only damage if cooldown expired
                if current_time - self.last_damage_time >= self.damage_cooldown:
                    enemy.attack_player(self.player)
                    self.last_damage_time = current_time

    def draw(self, screen):
        """
        Draw all game objects

        Args:
            screen: Pygame screen surface
        """
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)

        # Draw player
        self.player.draw(screen)

        # If game over, we'll draw that in main.py

    def is_running(self):
        """Check if game is still running"""
        return self.running

    def is_game_over(self):
        """Check if game is over"""
        return self.game_over
