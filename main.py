"""
Pixel Survivor: Worlds
Main entry point
"""
import pygame
import json
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from game import Game


def load_config():
    """Load game configuration from settings.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.json')
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main game function"""
    # Initialize Pygame
    pygame.init()

    # Load configuration
    config = load_config()
    game_config = config['game']
    player_config = config['player']

    # Create window
    screen_width = game_config['window_width']
    screen_height = game_config['window_height']
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(game_config['title'])

    # Set up FPS clock
    clock = pygame.time.Clock()
    fps = game_config['fps']

    # Create game instance
    game = Game(config, screen_width, screen_height)

    # Colors
    BG_COLOR = (30, 30, 40)  # Dark blue-gray background
    GRID_COLOR = (45, 45, 60)
    TEXT_COLOR = (255, 255, 255)
    HP_BAR_BG = (60, 60, 70)
    HP_BAR_FG = (0, 200, 100)
    HP_BAR_BORDER = (200, 200, 200)

    # Font for debug info
    font = pygame.font.Font(None, 24)
    font_small = pygame.font.Font(None, 18)

    # Game loop
    while game.is_running():
        # Delta time for frame-independent movement
        dt = clock.tick(fps) / 1000.0  # Convert to seconds

        # Handle events
        events = pygame.event.get()
        game.handle_events(events)

        # Get input states
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Update game
        game.update(keys, mouse_pos, dt)

        # Draw everything
        screen.fill(BG_COLOR)

        # Draw grid background
        grid_size = 50
        for x in range(0, screen_width, grid_size):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height), 1)
        for y in range(0, screen_height, grid_size):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y), 1)

        # Draw all game objects (bullets, enemies, player)
        game.draw(screen)

        # Draw crosshair at mouse position
        if not game.is_game_over():
            mx, my = mouse_pos
            crosshair_size = 15
            crosshair_gap = 5
            crosshair_color = (255, 100, 100)
            # Horizontal lines
            pygame.draw.line(screen, crosshair_color,
                            (mx - crosshair_size, my),
                            (mx - crosshair_gap, my), 2)
            pygame.draw.line(screen, crosshair_color,
                            (mx + crosshair_gap, my),
                            (mx + crosshair_size, my), 2)
            # Vertical lines
            pygame.draw.line(screen, crosshair_color,
                            (mx, my - crosshair_size),
                            (mx, my - crosshair_gap), 2)
            pygame.draw.line(screen, crosshair_color,
                            (mx, my + crosshair_gap),
                            (mx, my + crosshair_size), 2)
            # Center dot
            pygame.draw.circle(screen, crosshair_color, (mx, my), 2)

        # Draw health bar (top-left)
        hp_bar_x = 10
        hp_bar_y = 10
        hp_bar_width = 200
        hp_bar_height = 25

        # Background
        pygame.draw.rect(screen, HP_BAR_BG,
                        (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))

        # Foreground (current HP)
        hp_percentage = max(0, game.player.hp) / game.player.max_hp
        current_hp_width = int(hp_bar_width * hp_percentage)

        # Color changes based on HP
        if hp_percentage > 0.6:
            bar_color = (0, 200, 100)  # Green
        elif hp_percentage > 0.3:
            bar_color = (255, 200, 0)  # Yellow
        else:
            bar_color = (255, 50, 50)  # Red

        pygame.draw.rect(screen, bar_color,
                        (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height))

        # Border
        pygame.draw.rect(screen, HP_BAR_BORDER,
                        (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2)

        # HP text
        hp_text = font.render(f"HP: {int(max(0, game.player.hp))}/{game.player.max_hp}", True, TEXT_COLOR)
        text_x = hp_bar_x + hp_bar_width // 2 - hp_text.get_width() // 2
        text_y = hp_bar_y + hp_bar_height // 2 - hp_text.get_height() // 2
        screen.blit(hp_text, (text_x, text_y))

        # Draw stats panel (top-right)
        stats_x = screen_width - 220
        stats_y = 10

        # Stats background
        stats_bg = pygame.Rect(stats_x - 10, stats_y - 5, 210, 90)
        pygame.draw.rect(screen, (20, 20, 30, 200), stats_bg)
        pygame.draw.rect(screen, (100, 100, 120), stats_bg, 2)

        # Stats text
        stats_list = [
            f"Kills: {game.kills}",
            f"Score: {game.score}",
            f"Enemies: {len(game.enemies)}",
            f"Time: {int(game.time_survived)}s"
        ]

        for i, stat in enumerate(stats_list):
            stat_text = font_small.render(stat, True, (200, 200, 200))
            screen.blit(stat_text, (stats_x, stats_y + i * 20))

        # Draw info panel (top-left, below HP)
        info_y = hp_bar_y + hp_bar_height + 15
        phase_text = font.render("Phase 2: Combat!", True, (255, 150, 100))
        screen.blit(phase_text, (10, info_y))

        # FPS (smaller text)
        info_y += 30
        fps_text = font_small.render(f"FPS: {int(clock.get_fps())}", True, (150, 150, 150))
        screen.blit(fps_text, (10, info_y))

        # Draw controls (bottom-left)
        if not game.is_game_over():
            controls_y = screen_height - 120
            controls_title = font.render("Controls:", True, TEXT_COLOR)
            screen.blit(controls_title, (10, controls_y))

            controls_y += 25
            controls_list = [
                "WASD - Move",
                "Mouse - Aim",
                "Left Click / Space - Shoot",
                "ESC - Quit"
            ]
            for control in controls_list:
                ctrl_text = font_small.render(control, True, (200, 200, 200))
                screen.blit(ctrl_text, (10, controls_y))
                controls_y += 20

        # Game Over screen
        if game.is_game_over():
            # Dark overlay
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Game Over title
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
            text_x = screen_width // 2 - game_over_text.get_width() // 2
            text_y = screen_height // 2 - 150
            screen.blit(game_over_text, (text_x, text_y))

            # Final stats
            final_stats = [
                f"Final Score: {game.score}",
                f"Kills: {game.kills}",
                f"Time Survived: {int(game.time_survived)}s"
            ]

            stats_font = pygame.font.Font(None, 36)
            y_offset = screen_height // 2 - 50
            for stat in final_stats:
                stat_text = stats_font.render(stat, True, (255, 255, 255))
                text_x = screen_width // 2 - stat_text.get_width() // 2
                screen.blit(stat_text, (text_x, y_offset))
                y_offset += 40

            # Restart instructions
            restart_text = font.render("Press R to Restart or ESC to Quit", True, (200, 200, 200))
            text_x = screen_width // 2 - restart_text.get_width() // 2
            screen.blit(restart_text, (text_x, screen_height // 2 + 100))

        # Update display
        pygame.display.flip()

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
