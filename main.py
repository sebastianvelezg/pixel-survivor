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

    # Create window
    screen_width = game_config['window_width']
    screen_height = game_config['window_height']
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(game_config['title'])

    # Create and run game
    game = Game(screen, config)
    game.run()

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
