"""
Game class - main game manager and brain of everything
"""
import pygame
from player import Player
from bullet import Bullet
from enemy import Enemy, spawn_enemy_at_edge
from round_manager import RoundManager
from world import WorldManager
from inventory import Inventory


class Game:
    """
    Main game manager - handles game loop, collision detection, and game states
    """

    def __init__(self, screen, config):
        """
        Initialize game

        Args:
            screen: Pygame screen surface
            config (dict): Game configuration from settings.json
        """
        self.screen = screen
        self.config = config
        self.screen_width = config['game']['window_width']
        self.screen_height = config['game']['window_height']
        self.fps = config['game']['fps']

        # Game state
        self.running = True
        self.game_over = False
        self.kills = 0

        # Create player at center
        self.player = Player(
            self.screen_width // 2,
            self.screen_height // 2,
            config['player']
        )

        # Game objects
        self.bullets = []
        self.enemies = []
        self.drops = []

        # Inventory system
        self.inventory = Inventory()

        # World and Round Management
        self.world_manager = WorldManager(config['worlds'])
        self.round_manager = RoundManager(self.screen_width, self.screen_height)
        self.round_manager.start_round()  # Start first round

        # Colors
        self.TEXT_COLOR = (255, 255, 255)

        # Font
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

        # Clock
        self.clock = pygame.time.Clock()

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Shoot with spacebar
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.try_shoot()

                # Weapon switching (1, 2, 3 keys)
                if not self.game_over:
                    if event.key == pygame.K_1:
                        self.inventory.switch_weapon(0)
                    elif event.key == pygame.K_2:
                        self.inventory.switch_weapon(1)
                    elif event.key == pygame.K_3:
                        self.inventory.switch_weapon(2)

            # Shoot with left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Left click
                    self.try_shoot()

    def try_shoot(self):
        """Attempt to shoot a bullet"""
        # Use weapon from inventory
        weapon = self.inventory.get_active_weapon()
        if weapon:
            new_bullets = weapon.shoot(self.player.x, self.player.y, self.player.angle)
            self.bullets.extend(new_bullets)

    def update(self, dt):
        """
        Update all game objects

        Args:
            dt (float): Delta time in seconds
        """
        if self.game_over:
            return

        # Update inventory (weapons and powerups)
        self.inventory.update_weapons(dt)
        self.inventory.update_powerups(dt, self.player)

        # Update player
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.player.update(keys, mouse_pos, self.screen_width, self.screen_height, dt)

        # Check if player died
        if self.player.hp <= 0:
            self.game_over = True
            return

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update(dt)
            # Remove bullets that are off screen
            if bullet.is_off_screen(self.screen_width, self.screen_height):
                self.bullets.remove(bullet)

        # Update enemies
        player_pos = (self.player.x, self.player.y)
        for enemy in self.enemies:
            enemy.update(player_pos, dt)

        # Update drops
        for drop in self.drops[:]:
            drop.update(dt)
            # Remove expired drops
            if not drop.alive:
                self.drops.remove(drop)
            # Check for pickup
            elif drop.can_pickup(self.player.x, self.player.y):
                if drop.apply_to_player(self.player, self.inventory):
                    self.drops.remove(drop)
                    # Activate powerup if it was added
                    if drop.drop_type == "POWERUP" and self.inventory.powerups:
                        self.inventory.powerups[-1].activate(self.player)

        # Check collisions
        self.check_collisions()

        # Remove dead enemies
        alive_enemies = [e for e in self.enemies if e.alive]
        self.enemies = alive_enemies

        # Update round manager and spawn enemies
        enemy_stats = self.round_manager.update(dt, len(self.enemies))
        if enemy_stats:
            # Apply world modifiers to enemy stats
            modified_stats = self.world_manager.apply_enemy_modifiers(enemy_stats)

            # Spawn enemy with modified stats
            enemy = spawn_enemy_at_edge(
                self.screen_width,
                self.screen_height,
                speed=modified_stats['speed'],
                hp=modified_stats['hp'],
                damage=modified_stats['damage']
            )
            self.enemies.append(enemy)

        # Check if round/world is complete
        round_info = self.round_manager.get_round_info()
        if round_info['enemies_remaining'] == 0 and len(self.enemies) == 0:
            if not round_info['in_break']:
                # Round complete - check world progression
                advanced_world = self.world_manager.complete_round()
                if advanced_world:
                    # Advanced to next world - reset round manager
                    self.round_manager.reset()
                    self.round_manager.start_round()

    def check_collisions(self):
        """Check all collision between game objects"""
        # Bullets hit enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    # Enemy takes damage (with player damage modifier from powerups)
                    damage = bullet.damage
                    if enemy.take_damage(damage):
                        self.kills += 1
                        # Enemy died - drop loot
                        drop = enemy.drop_loot()
                        if drop:
                            self.drops.append(drop)
                    # Remove bullet
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

        # Enemies hit player
        for enemy in self.enemies:
            if enemy.alive and self.player.rect.colliderect(enemy.rect):
                enemy.attack_player(self.player)

    def draw(self):
        """Draw all game objects to screen"""
        # Clear screen with world-specific background color
        bg_color = self.world_manager.get_background_color()
        self.screen.fill(bg_color)

        if not self.game_over:
            # Draw drops (behind everything)
            for drop in self.drops:
                drop.draw(self.screen)

            # Draw player
            self.player.draw(self.screen)

            # Draw bullets
            for bullet in self.bullets:
                bullet.draw(self.screen)

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Draw HUD
            self.draw_hud()

        else:
            # Draw game over screen
            self.draw_game_over()

        # Update display
        pygame.display.flip()

    def draw_hud(self):
        """Draw heads-up display"""
        # HP Bar (top-left)
        bar_width = 200
        bar_height = 24
        bar_x = 10
        bar_y = 10

        # Background
        pygame.draw.rect(self.screen, (80, 0, 0),
                        (bar_x, bar_y, bar_width, bar_height))

        # HP fill
        hp_percentage = max(0, self.player.hp / self.player.max_hp)
        hp_color = (0, 255, 0) if hp_percentage > 0.5 else (255, 255, 0) if hp_percentage > 0.25 else (255, 0, 0)
        pygame.draw.rect(self.screen, hp_color,
                        (bar_x, bar_y, int(bar_width * hp_percentage), bar_height))

        # HP border
        pygame.draw.rect(self.screen, self.TEXT_COLOR,
                        (bar_x, bar_y, bar_width, bar_height), 2)

        # HP text
        hp_text = self.small_font.render(f"HP: {int(self.player.hp)}/{self.player.max_hp}",
                                         True, self.TEXT_COLOR)
        self.screen.blit(hp_text, (bar_x + 5, bar_y + 3))

        # World and Round info (top-center)
        world_info = self.world_manager.get_current_world_info()
        round_info = self.round_manager.get_round_info()

        world_text = self.font.render(f"{world_info['name']}", True, self.world_manager.get_accent_color())
        world_rect = world_text.get_rect(center=(self.screen_width // 2, 20))
        self.screen.blit(world_text, world_rect)

        # Round info below world name
        if round_info['in_break']:
            round_text = self.small_font.render(
                f"Next Round in {round_info['break_time']:.1f}s",
                True, (255, 200, 100)
            )
        else:
            round_text = self.small_font.render(
                f"Round {round_info['round']} - {world_info['rounds_completed']}/{world_info['rounds_completed'] + world_info['rounds_remaining']}",
                True, self.TEXT_COLOR
            )
        round_rect = round_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(round_text, round_rect)

        # Kills (top-right)
        kills_text = self.small_font.render(f"Kills: {self.kills}", True, self.TEXT_COLOR)
        self.screen.blit(kills_text, (self.screen_width - 120, 15))

        # Enemy count
        enemy_text = self.small_font.render(f"Enemies: {len(self.enemies)}",
                                           True, self.TEXT_COLOR)
        self.screen.blit(enemy_text, (self.screen_width - 150, 45))

        # Enemies remaining in round
        if round_info['enemies_remaining'] > 0:
            remaining_text = self.small_font.render(
                f"Spawning: {round_info['enemies_remaining']}",
                True, (255, 100, 100)
            )
            self.screen.blit(remaining_text, (self.screen_width - 180, 75))

        # Weapon display (bottom-left)
        weapon_info = self.inventory.get_weapon_display_info()
        weapon_y = self.screen_height - 100
        for info in weapon_info:
            slot_text = f"[{info['slot']}] "
            if info.get('name') != 'Empty':
                color = info['color'] if info['active'] else (150, 150, 150)
                weapon_label = self.small_font.render(
                    f"{slot_text}{info['name']}",
                    True,
                    color
                )
            else:
                weapon_label = self.small_font.render(
                    f"{slot_text}Empty",
                    True,
                    (100, 100, 100)
                )
            self.screen.blit(weapon_label, (10, weapon_y))
            weapon_y += 25

        # Powerup timers (bottom-right)
        powerup_info = self.inventory.get_powerup_display_info()
        powerup_y = self.screen_height - 100
        for info in powerup_info:
            powerup_text = self.small_font.render(
                f"{info['name']}: {info['time_remaining']:.1f}s",
                True,
                info['color']
            )
            self.screen.blit(powerup_text, (self.screen_width - 200, powerup_y))
            powerup_y += 25

        # Coins display (under kills)
        coins_text = self.small_font.render(f"Coins: {self.inventory.coins}", True, (255, 215, 0))
        self.screen.blit(coins_text, (self.screen_width - 120, 105))

        # Phase 4 label
        phase_text = self.small_font.render("Phase 4: Loot & Inventory", True, (100, 200, 255))
        self.screen.blit(phase_text, (10, self.screen_height - 30))

    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.font.render("GAME OVER!", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(self.screen_width // 2,
                                                     self.screen_height // 2 - 60))
        self.screen.blit(game_over_text, text_rect)

        # Final score
        score_text = self.font.render(f"Kills: {self.kills}", True, self.TEXT_COLOR)
        score_rect = score_text.get_rect(center=(self.screen_width // 2,
                                                  self.screen_height // 2))
        self.screen.blit(score_text, score_rect)

        # Instructions
        restart_text = self.small_font.render("Press ESC to quit", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2,
                                                     self.screen_height // 2 + 60))
        self.screen.blit(restart_text, restart_rect)

    def run(self):
        """Main game loop"""
        while self.running:
            # Delta time
            dt = self.clock.tick(self.fps) / 1000.0

            # Handle events
            self.handle_events()

            # Update game
            self.update(dt)

            # Draw everything
            self.draw()

        return self.running
