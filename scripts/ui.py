"""
UI classes - HUD, menus, and user interface elements
"""
import pygame


class HUD:
    """
    Heads-Up Display - shows game information during play
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize HUD

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts
        self.large_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

        # Colors
        self.TEXT_COLOR = (255, 255, 255)
        self.HEALTH_HIGH = (0, 255, 0)
        self.HEALTH_MED = (255, 255, 0)
        self.HEALTH_LOW = (255, 0, 0)

    def draw_health_bar(self, screen, player):
        """
        Draw player health bar

        Args:
            screen: Pygame screen surface
            player: Player object
        """
        bar_width = 200
        bar_height = 24
        bar_x = 10
        bar_y = 10

        # Background (dark red)
        pygame.draw.rect(screen, (80, 0, 0),
                        (bar_x, bar_y, bar_width, bar_height))

        # HP fill (color changes based on health)
        hp_percentage = max(0, player.hp / player.max_hp)
        if hp_percentage > 0.5:
            hp_color = self.HEALTH_HIGH
        elif hp_percentage > 0.25:
            hp_color = self.HEALTH_MED
        else:
            hp_color = self.HEALTH_LOW

        pygame.draw.rect(screen, hp_color,
                        (bar_x, bar_y, int(bar_width * hp_percentage), bar_height))

        # Border
        pygame.draw.rect(screen, self.TEXT_COLOR,
                        (bar_x, bar_y, bar_width, bar_height), 2)

        # HP text
        hp_text = self.small_font.render(f"HP: {int(player.hp)}/{player.max_hp}",
                                         True, self.TEXT_COLOR)
        screen.blit(hp_text, (bar_x + 5, bar_y + 3))

    def draw_weapon_display(self, screen, inventory):
        """
        Draw weapon inventory display

        Args:
            screen: Pygame screen surface
            inventory: Inventory object
        """
        weapon_info = inventory.get_weapon_display_info()
        weapon_y = self.screen_height - 100

        for info in weapon_info:
            slot_text = f"[{info['slot']}] "

            if info.get('name') != 'Empty':
                # Active weapon is bright, others are dimmed
                color = info['color'] if info['active'] else (100, 100, 100)
                weapon_label = self.small_font.render(
                    f"{slot_text}{info['name']}",
                    True,
                    color
                )

                # Add cooldown indicator
                if info['active'] and not info.get('ready', True):
                    weapon_label_str = f"{slot_text}{info['name']} (reloading...)"
                    weapon_label = self.small_font.render(weapon_label_str, True, color)
            else:
                weapon_label = self.small_font.render(
                    f"{slot_text}Empty",
                    True,
                    (80, 80, 80)
                )

            screen.blit(weapon_label, (10, weapon_y))
            weapon_y += 25

    def draw_powerup_timers(self, screen, inventory):
        """
        Draw active powerup timers

        Args:
            screen: Pygame screen surface
            inventory: Inventory object
        """
        powerup_info = inventory.get_powerup_display_info()
        powerup_y = self.screen_height - 100

        for info in powerup_info:
            # Create text with time remaining
            powerup_text = self.small_font.render(
                f"{info['name']}: {info['time_remaining']:.1f}s",
                True,
                info['color']
            )

            # Draw with slight glow effect
            text_x = self.screen_width - 220
            screen.blit(powerup_text, (text_x, powerup_y))

            # Draw progress bar
            bar_width = 100
            bar_height = 4
            bar_x = self.screen_width - 220
            bar_y = powerup_y + 20

            progress = info['time_remaining'] / info['duration']
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, info['color'],
                           (bar_x, bar_y, int(bar_width * progress), bar_height))

            powerup_y += 30

    def draw_round_info(self, screen, world_manager, round_manager):
        """
        Draw world and round information

        Args:
            screen: Pygame screen surface
            world_manager: WorldManager object
            round_manager: RoundManager object
        """
        world_info = world_manager.get_current_world_info()
        round_info = round_manager.get_round_info()

        # World name (top-center)
        world_text = self.large_font.render(
            f"{world_info['name']}",
            True,
            world_manager.get_accent_color()
        )
        world_rect = world_text.get_rect(center=(self.screen_width // 2, 20))
        screen.blit(world_text, world_rect)

        # Round info below world name
        if round_info['in_break']:
            round_text = self.small_font.render(
                f"Next Round in {round_info['break_time']:.1f}s",
                True,
                (255, 200, 100)
            )
        else:
            total_rounds = world_info['rounds_completed'] + world_info['rounds_remaining']
            round_text = self.small_font.render(
                f"Round {round_info['round']} - Progress: {world_info['rounds_completed']}/{total_rounds}",
                True,
                self.TEXT_COLOR
            )

        round_rect = round_text.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(round_text, round_rect)

    def draw_coin_count(self, screen, coins):
        """
        Draw coin count

        Args:
            screen: Pygame screen surface
            coins (int): Number of coins
        """
        coins_text = self.small_font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coins_text, (self.screen_width - 120, 105))

    def draw_kill_count(self, screen, kills):
        """
        Draw kill count

        Args:
            screen: Pygame screen surface
            kills (int): Number of kills
        """
        kills_text = self.small_font.render(f"Kills: {kills}", True, self.TEXT_COLOR)
        screen.blit(kills_text, (self.screen_width - 120, 15))

    def draw_enemy_count(self, screen, active_enemies, enemies_remaining):
        """
        Draw enemy count information

        Args:
            screen: Pygame screen surface
            active_enemies (int): Number of active enemies
            enemies_remaining (int): Number of enemies left to spawn
        """
        # Active enemies
        enemy_text = self.small_font.render(
            f"Enemies: {active_enemies}",
            True,
            self.TEXT_COLOR
        )
        screen.blit(enemy_text, (self.screen_width - 150, 45))

        # Enemies remaining to spawn
        if enemies_remaining > 0:
            remaining_text = self.small_font.render(
                f"Spawning: {enemies_remaining}",
                True,
                (255, 100, 100)
            )
            screen.blit(remaining_text, (self.screen_width - 180, 75))

    def draw_all(self, screen, player, inventory, world_manager, round_manager, kills, enemy_count):
        """
        Draw complete HUD

        Args:
            screen: Pygame screen surface
            player: Player object
            inventory: Inventory object
            world_manager: WorldManager object
            round_manager: RoundManager object
            kills (int): Kill count
            enemy_count (int): Active enemy count
        """
        self.draw_health_bar(screen, player)
        self.draw_weapon_display(screen, inventory)
        self.draw_powerup_timers(screen, inventory)
        self.draw_round_info(screen, world_manager, round_manager)
        self.draw_coin_count(screen, inventory.coins)
        self.draw_kill_count(screen, kills)

        round_info = round_manager.get_round_info()
        self.draw_enemy_count(screen, enemy_count, round_info['enemies_remaining'])


class Button:
    """
    Clickable button for menus
    """

    def __init__(self, x, y, width, height, text, color=(100, 100, 200), hover_color=(150, 150, 255)):
        """
        Initialize button

        Args:
            x (int): X position (center)
            y (int): Y position (center)
            width (int): Button width
            height (int): Button height
            text (str): Button text
            color (tuple): Normal button color
            hover_color (tuple): Hover button color
        """
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)
        self.hovered = False

    def update(self, mouse_pos):
        """
        Update button hover state

        Args:
            mouse_pos (tuple): Mouse position
        """
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        """
        Draw button

        Args:
            screen: Pygame screen surface
        """
        # Draw button background
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Draw text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        """
        Check if button was clicked

        Args:
            mouse_pos (tuple): Mouse position
            mouse_click (bool): Mouse button state

        Returns:
            bool: True if clicked
        """
        return self.rect.collidepoint(mouse_pos) and mouse_click


class MainMenu:
    """
    Main menu screen
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize main menu

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Save info
        self.has_save = False
        self.save_info = None

        # Buttons (positioned based on whether save exists)
        self._create_buttons()

    def _create_buttons(self):
        """Create menu buttons based on save state"""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        if self.has_save:
            # Show Continue, New Game, Quit
            self.continue_button = Button(center_x, center_y + 20, 220, 60, "Continue")
            self.new_game_button = Button(center_x, center_y + 100, 220, 60, "New Game")
            self.quit_button = Button(center_x, center_y + 180, 220, 60, "Quit")
        else:
            # Show Play, Quit
            self.continue_button = None
            self.new_game_button = Button(center_x, center_y + 20, 200, 60, "Play")
            self.quit_button = Button(center_x, center_y + 100, 200, 60, "Quit")

    def set_save_state(self, has_save, save_info=None):
        """
        Update menu based on save file existence

        Args:
            has_save (bool): Whether a save file exists
            save_info (dict): Save file information (world, round, etc.)
        """
        self.has_save = has_save
        self.save_info = save_info
        self._create_buttons()

    def update(self, mouse_pos):
        """
        Update menu

        Args:
            mouse_pos (tuple): Mouse position
        """
        if self.has_save and self.continue_button:
            self.continue_button.update(mouse_pos)
        self.new_game_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)

    def handle_click(self, mouse_pos):
        """
        Handle mouse click

        Args:
            mouse_pos (tuple): Mouse position

        Returns:
            str: Action to take ('continue', 'new_game', 'quit', or None)
        """
        if self.has_save and self.continue_button:
            if self.continue_button.is_clicked(mouse_pos, True):
                return 'continue'

        if self.new_game_button.is_clicked(mouse_pos, True):
            return 'new_game'
        elif self.quit_button.is_clicked(mouse_pos, True):
            return 'quit'
        return None

    def draw(self, screen):
        """
        Draw main menu

        Args:
            screen: Pygame screen surface
        """
        # Background
        screen.fill((20, 20, 30))

        # Title
        title_text = self.title_font.render("Pixel Survivor", True, (100, 200, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = self.subtitle_font.render("Worlds", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)

        # Save info (if exists)
        if self.has_save and self.save_info:
            save_text = self.small_font.render(
                f"Saved: World {self.save_info.get('world_number', '?')} - Round {self.save_info.get('round_number', '?')}",
                True,
                (100, 255, 100)
            )
            save_rect = save_text.get_rect(center=(self.screen_width // 2, 240))
            screen.blit(save_text, save_rect)

        # Instructions
        info_font = pygame.font.Font(None, 24)
        controls = [
            "WASD - Move",
            "Mouse - Aim",
            "Click/Space - Shoot",
            "1/2/3 - Switch Weapons"
        ]

        y_offset = 280 if not self.has_save else 270
        for control in controls:
            control_text = info_font.render(control, True, (150, 150, 150))
            control_rect = control_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(control_text, control_rect)
            y_offset += 25

        # Buttons
        if self.has_save and self.continue_button:
            self.continue_button.draw(screen)
        self.new_game_button.draw(screen)
        self.quit_button.draw(screen)


class PauseMenu:
    """
    Pause menu overlay
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize pause menu

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Font
        self.title_font = pygame.font.Font(None, 64)

        # Buttons
        center_x = screen_width // 2
        center_y = screen_height // 2

        self.resume_button = Button(center_x, center_y + 20, 200, 60, "Resume")
        self.main_menu_button = Button(center_x, center_y + 100, 200, 60, "Main Menu")

    def update(self, mouse_pos):
        """
        Update pause menu

        Args:
            mouse_pos (tuple): Mouse position
        """
        self.resume_button.update(mouse_pos)
        self.main_menu_button.update(mouse_pos)

    def handle_click(self, mouse_pos):
        """
        Handle mouse click

        Args:
            mouse_pos (tuple): Mouse position

        Returns:
            str: Action to take ('resume', 'main_menu', or None)
        """
        if self.resume_button.is_clicked(mouse_pos, True):
            return 'resume'
        elif self.main_menu_button.is_clicked(mouse_pos, True):
            return 'main_menu'
        return None

    def draw(self, screen):
        """
        Draw pause menu

        Args:
            screen: Pygame screen surface
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Title
        title_text = self.title_font.render("PAUSED", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(self.screen_width // 2,
                                                  self.screen_height // 2 - 80))
        screen.blit(title_text, title_rect)

        # Buttons
        self.resume_button.draw(screen)
        self.main_menu_button.draw(screen)


class GameOverMenu:
    """
    Game over screen
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize game over menu

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)

        # Buttons
        center_x = screen_width // 2
        center_y = screen_height // 2

        self.retry_button = Button(center_x, center_y + 80, 200, 60, "Retry")
        self.main_menu_button = Button(center_x, center_y + 160, 200, 60, "Main Menu")

    def update(self, mouse_pos):
        """
        Update game over menu

        Args:
            mouse_pos (tuple): Mouse position
        """
        self.retry_button.update(mouse_pos)
        self.main_menu_button.update(mouse_pos)

    def handle_click(self, mouse_pos):
        """
        Handle mouse click

        Args:
            mouse_pos (tuple): Mouse position

        Returns:
            str: Action to take ('retry', 'main_menu', or None)
        """
        if self.retry_button.is_clicked(mouse_pos, True):
            return 'retry'
        elif self.main_menu_button.is_clicked(mouse_pos, True):
            return 'main_menu'
        return None

    def draw(self, screen, kills, world_info, round_info):
        """
        Draw game over menu

        Args:
            screen: Pygame screen surface
            kills (int): Final kill count
            world_info (dict): World information
            round_info (dict): Round information
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Title
        title_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(self.screen_width // 2,
                                                  self.screen_height // 2 - 120))
        screen.blit(title_text, title_rect)

        # Stats
        stats = [
            f"Kills: {kills}",
            f"World: {world_info['name']}",
            f"Round: {round_info['round']}"
        ]

        y_offset = self.screen_height // 2 - 40
        for stat in stats:
            stat_text = self.font.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 40

        # Buttons
        self.retry_button.draw(screen)
        self.main_menu_button.draw(screen)
