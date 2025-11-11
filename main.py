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

from player import Player


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

    # Create player at center of screen
    player = Player(screen_width // 2, screen_height // 2, player_config)

    # Colors
    BG_COLOR = (30, 30, 40)  # Dark blue-gray background
    TEXT_COLOR = (255, 255, 255)

    # Font for debug info
    font = pygame.font.Font(None, 24)

    # Game loop
    running = True
    while running:
        # Delta time for frame-independent movement
        dt = clock.tick(fps) / 1000.0  # Convert to seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Get input states
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Update player
        player.update(keys, mouse_pos, screen_width, screen_height, dt)

        # Draw everything
        screen.fill(BG_COLOR)

        # Draw player
        player.draw(screen)

        # Draw UI - Phase 1 debug info
        info_text = [
            f"Phase 1: Player Movement Test",
            f"Position: ({int(player.x)}, {int(player.y)})",
            f"HP: {player.hp}/{player.max_hp}",
            f"FPS: {int(clock.get_fps())}",
            "",
            "Controls:",
            "WASD - Move",
            "Mouse - Aim",
            "ESC - Quit"
        ]

        y_offset = 10
        for line in info_text:
            text_surface = font.render(line, True, TEXT_COLOR)
            screen.blit(text_surface, (10, y_offset))
            y_offset += 25

        # Update display
        pygame.display.flip()

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
