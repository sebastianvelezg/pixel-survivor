"""
Game class - main game manager and brain of everything
"""
import pygame
import time
from player import Player
from bullet import Bullet
from enemy import Enemy, spawn_enemy_at_edge
from round_manager import RoundManager
from world import WorldManager
from inventory import Inventory
from ui import HUD, MainMenu, PauseMenu, GameOverMenu
from upgrade_shop import UpgradeShop
from save_manager import SaveManager, create_save_data, restore_from_save


class GameState:
    """Game state enum"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    SHOP = "shop"
    GAME_OVER = "game_over"


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
        self.state = GameState.MENU

        # Clock
        self.clock = pygame.time.Clock()

        # Save manager
        self.save_manager = SaveManager()

        # UI Components
        self.hud = HUD(self.screen_width, self.screen_height)
        self.main_menu = MainMenu(self.screen_width, self.screen_height)
        self.pause_menu = PauseMenu(self.screen_width, self.screen_height)
        self.game_over_menu = GameOverMenu(self.screen_width, self.screen_height)
        self.upgrade_shop = UpgradeShop(self.screen_width, self.screen_height)

        # Check for save file and update menu
        self._update_menu_save_state()

        # Game session data (initialized when starting new game)
        self.player = None
        self.bullets = []
        self.enemies = []
        self.drops = []
        self.inventory = None
        self.world_manager = None
        self.round_manager = None
        self.kills = 0
        self.round_complete_flag = False
        self.session_start_time = None
        self.total_playtime = 0

    def _update_menu_save_state(self):
        """Update main menu based on save file existence"""
        has_save = self.save_manager.has_save()
        save_info = self.save_manager.get_save_info() if has_save else None
        self.main_menu.set_save_state(has_save, save_info)

    def start_new_game(self, delete_save=True):
        """
        Initialize a new game session

        Args:
            delete_save (bool): Whether to delete existing save file
        """
        # Delete save if requested
        if delete_save:
            self.save_manager.delete_save()
            self._update_menu_save_state()

        # Create player at center
        self.player = Player(
            self.screen_width // 2,
            self.screen_height // 2,
            self.config['player']
        )

        # Game objects
        self.bullets = []
        self.enemies = []
        self.drops = []
        self.kills = 0
        self.round_complete_flag = False
        self.session_start_time = time.time()
        self.total_playtime = 0

        # Inventory system
        self.inventory = Inventory()

        # World and Round Management
        self.world_manager = WorldManager(self.config['worlds'])
        self.round_manager = RoundManager(self.screen_width, self.screen_height)
        self.round_manager.start_round()  # Start first round

        # Change state to playing
        self.state = GameState.PLAYING

    def load_saved_game(self):
        """Load game from save file"""
        save_data = self.save_manager.load_game()

        if not save_data:
            print("Failed to load save file")
            # Fall back to new game
            self.start_new_game(delete_save=False)
            return

        # Initialize game objects first
        self.player = Player(
            self.screen_width // 2,
            self.screen_height // 2,
            self.config['player']
        )
        self.bullets = []
        self.enemies = []
        self.drops = []
        self.round_complete_flag = False
        self.session_start_time = time.time()

        # Inventory and managers
        self.inventory = Inventory()
        self.world_manager = WorldManager(self.config['worlds'])
        self.round_manager = RoundManager(self.screen_width, self.screen_height)

        # Restore state from save
        self.kills = restore_from_save(
            save_data,
            self.player,
            self.inventory,
            self.world_manager,
            self.round_manager
        )

        # Restore playtime
        self.total_playtime = save_data.get('stats', {}).get('playtime', 0)

        # Start the current round
        self.round_manager.start_round()

        # Change state to playing
        self.state = GameState.PLAYING

    def save_game(self):
        """Save current game state"""
        if not self.player or not self.inventory:
            return False

        # Calculate playtime
        if self.session_start_time:
            session_time = time.time() - self.session_start_time
            playtime = self.total_playtime + session_time
        else:
            playtime = self.total_playtime

        # Create save data
        save_data = create_save_data(
            self.player,
            self.inventory,
            self.world_manager,
            self.round_manager,
            self.kills,
            playtime
        )

        # Save to file
        success = self.save_manager.save_game(save_data)

        if success:
            # Update menu state
            self._update_menu_save_state()

        return success

    def handle_events(self):
        """Handle pygame events"""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # ESC key behavior depends on state
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.MENU:
                        self.running = False

                # Gameplay controls (only during PLAYING state)
                if self.state == GameState.PLAYING:
                    # Shoot with spacebar
                    if event.key == pygame.K_SPACE:
                        self.try_shoot()

                    # Weapon switching (1, 2, 3 keys)
                    if event.key == pygame.K_1:
                        self.inventory.switch_weapon(0)
                    elif event.key == pygame.K_2:
                        self.inventory.switch_weapon(1)
                    elif event.key == pygame.K_3:
                        self.inventory.switch_weapon(2)

            # Mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.state == GameState.MENU:
                        action = self.main_menu.handle_click(mouse_pos)
                        if action == 'continue':
                            self.load_saved_game()
                        elif action == 'new_game':
                            self.start_new_game(delete_save=True)
                        elif action == 'quit':
                            self.running = False

                    elif self.state == GameState.PLAYING:
                        self.try_shoot()

                    elif self.state == GameState.PAUSED:
                        action = self.pause_menu.handle_click(mouse_pos)
                        if action == 'resume':
                            self.state = GameState.PLAYING
                        elif action == 'main_menu':
                            # Save game before returning to menu
                            self.save_game()
                            self.state = GameState.MENU

                    elif self.state == GameState.GAME_OVER:
                        action = self.game_over_menu.handle_click(mouse_pos)
                        if action == 'retry':
                            self.start_new_game(delete_save=True)
                        elif action == 'main_menu':
                            self.state = GameState.MENU

                    elif self.state == GameState.SHOP:
                        result = self.upgrade_shop.handle_click(mouse_pos, self.player, self.inventory)
                        if result == 'continue':
                            # Save game before continuing
                            self.save_game()
                            # Continue to next round
                            self.round_manager.start_round()
                            self.state = GameState.PLAYING
                            self.round_complete_flag = False

    def try_shoot(self):
        """Attempt to shoot a bullet"""
        if not self.player or not self.inventory:
            return

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
        # Update based on state
        if self.state == GameState.MENU:
            mouse_pos = pygame.mouse.get_pos()
            self.main_menu.update(mouse_pos)

        elif self.state == GameState.PLAYING:
            self.update_gameplay(dt)

        elif self.state == GameState.PAUSED:
            mouse_pos = pygame.mouse.get_pos()
            self.pause_menu.update(mouse_pos)

        elif self.state == GameState.GAME_OVER:
            mouse_pos = pygame.mouse.get_pos()
            self.game_over_menu.update(mouse_pos)

        elif self.state == GameState.SHOP:
            mouse_pos = pygame.mouse.get_pos()
            # Update shop and check if time expired
            if self.upgrade_shop.update(dt, mouse_pos):
                # Time expired, save and continue to next round
                self.save_game()
                self.round_manager.start_round()
                self.state = GameState.PLAYING
                self.round_complete_flag = False

    def update_gameplay(self, dt):
        """Update gameplay logic"""
        # Update inventory (weapons and powerups)
        self.inventory.update_weapons(dt)
        self.inventory.update_powerups(dt, self.player)

        # Update player
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.player.update(keys, mouse_pos, self.screen_width, self.screen_height, dt)

        # Check if player died
        if self.player.hp <= 0:
            self.state = GameState.GAME_OVER
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

        # Check if round is complete
        round_info = self.round_manager.get_round_info()
        if round_info['enemies_remaining'] == 0 and len(self.enemies) == 0:
            if not round_info['in_break'] and not self.round_complete_flag:
                # Round just completed
                self.round_complete_flag = True

                # Complete round in world manager
                advanced_world = self.world_manager.complete_round()

                # Open upgrade shop
                self.upgrade_shop.reset_timer()
                self.state = GameState.SHOP

                if advanced_world:
                    # Advanced to next world - reset round manager
                    self.round_manager.reset()

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
        if self.state == GameState.MENU:
            self.main_menu.draw(self.screen)

        elif self.state == GameState.PLAYING:
            self.draw_gameplay()

        elif self.state == GameState.PAUSED:
            # Draw gameplay in background
            self.draw_gameplay()
            # Draw pause menu on top
            self.pause_menu.draw(self.screen)

        elif self.state == GameState.GAME_OVER:
            # Draw gameplay in background
            self.draw_gameplay()
            # Draw game over menu on top
            world_info = self.world_manager.get_current_world_info()
            round_info = self.round_manager.get_round_info()
            self.game_over_menu.draw(self.screen, self.kills, world_info, round_info)

        elif self.state == GameState.SHOP:
            # Draw gameplay in background
            self.draw_gameplay()
            # Draw upgrade shop on top
            self.upgrade_shop.draw(self.screen, self.player, self.inventory, self.world_manager)

        # Update display
        pygame.display.flip()

    def draw_gameplay(self):
        """Draw the main gameplay view"""
        # Clear screen with world-specific background color
        bg_color = self.world_manager.get_background_color()
        self.screen.fill(bg_color)

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
        self.hud.draw_all(
            self.screen,
            self.player,
            self.inventory,
            self.world_manager,
            self.round_manager,
            self.kills,
            len(self.enemies)
        )

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
