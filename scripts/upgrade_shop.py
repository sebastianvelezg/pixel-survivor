"""
UpgradeShop class - between-round upgrade system
"""
import pygame


class Upgrade:
    """
    Represents a single upgrade option
    """

    def __init__(self, name, description, cost, upgrade_type, value):
        """
        Initialize upgrade

        Args:
            name (str): Upgrade name
            description (str): Upgrade description
            cost (int): Coin cost
            upgrade_type (str): Type of upgrade (HP, SPEED, DAMAGE, FIRE_RATE)
            value (int/float): Value to upgrade by
        """
        self.name = name
        self.description = description
        self.cost = cost
        self.upgrade_type = upgrade_type
        self.value = value
        self.purchase_count = 0  # Track how many times purchased


class UpgradeShop:
    """
    Shop for purchasing upgrades between rounds
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize upgrade shop

        Args:
            screen_width (int): Screen width
            screen_height (int): Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

        # Colors
        self.BG_COLOR = (25, 25, 35)
        self.AFFORDABLE_COLOR = (100, 180, 100)
        self.EXPENSIVE_COLOR = (180, 100, 100)
        self.BUTTON_COLOR = (70, 70, 100)
        self.BUTTON_HOVER_COLOR = (100, 100, 150)

        # Define available upgrades
        self.upgrades = [
            Upgrade(
                "Max HP +20",
                "Increase maximum health by 20",
                50,
                "HP",
                20
            ),
            Upgrade(
                "Speed +10%",
                "Move 10% faster",
                40,
                "SPEED",
                0.1
            ),
            Upgrade(
                "Damage +15%",
                "Deal 15% more damage",
                60,
                "DAMAGE",
                0.15
            ),
            Upgrade(
                "Fire Rate +10%",
                "Shoot 10% faster",
                50,
                "FIRE_RATE",
                0.1
            )
        ]

        # Create upgrade buttons
        self._create_upgrade_buttons()

        # Continue button
        self.continue_button_rect = None
        self.continue_button_hovered = False

        # Timer for auto-continue
        self.shop_time_limit = 15.0  # 15 seconds to shop
        self.time_remaining = self.shop_time_limit

    def _create_upgrade_buttons(self):
        """Create button rectangles for each upgrade"""
        button_width = 350
        button_height = 80
        button_spacing = 20

        start_x = (self.screen_width - button_width) // 2
        start_y = 220

        self.upgrade_buttons = []
        for i, upgrade in enumerate(self.upgrades):
            button_rect = pygame.Rect(
                start_x,
                start_y + i * (button_height + button_spacing),
                button_width,
                button_height
            )
            self.upgrade_buttons.append(button_rect)

        # Continue button at bottom
        self.continue_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2,
            self.screen_height - 80,
            200,
            50
        )

    def reset_timer(self):
        """Reset shop timer"""
        self.time_remaining = self.shop_time_limit

    def update(self, dt, mouse_pos):
        """
        Update shop (timer, button hover states)

        Args:
            dt (float): Delta time in seconds
            mouse_pos (tuple): Mouse position

        Returns:
            bool: True if shop time expired
        """
        # Update timer
        self.time_remaining -= dt

        # Update continue button hover
        self.continue_button_hovered = self.continue_button_rect.collidepoint(mouse_pos)

        # Return True if time expired
        return self.time_remaining <= 0

    def handle_click(self, mouse_pos, player, inventory):
        """
        Handle mouse click on upgrades

        Args:
            mouse_pos (tuple): Mouse position
            player: Player object
            inventory: Inventory object

        Returns:
            str: 'continue' if continue button clicked, 'purchased' if upgrade bought, None otherwise
        """
        # Check continue button
        if self.continue_button_rect.collidepoint(mouse_pos):
            return 'continue'

        # Check upgrade buttons
        for i, button_rect in enumerate(self.upgrade_buttons):
            if button_rect.collidepoint(mouse_pos):
                upgrade = self.upgrades[i]

                # Check if player can afford
                if inventory.coins >= upgrade.cost:
                    # Purchase upgrade
                    if self.purchase_upgrade(upgrade, player, inventory):
                        return 'purchased'

        return None

    def purchase_upgrade(self, upgrade, player, inventory):
        """
        Purchase an upgrade

        Args:
            upgrade (Upgrade): Upgrade to purchase
            player: Player object
            inventory: Inventory object

        Returns:
            bool: True if purchase successful
        """
        # Spend coins
        if not inventory.spend_coins(upgrade.cost):
            return False

        # Apply upgrade based on type
        if upgrade.upgrade_type == "HP":
            player.max_hp += upgrade.value
            player.hp = min(player.hp + upgrade.value, player.max_hp)  # Also heal

        elif upgrade.upgrade_type == "SPEED":
            player.speed += player.speed * upgrade.value

        elif upgrade.upgrade_type == "DAMAGE":
            player.damage += int(player.damage * upgrade.value)

        elif upgrade.upgrade_type == "FIRE_RATE":
            # Reduce fire rate cooldowns on all weapons
            for weapon in inventory.weapons:
                if weapon:
                    weapon.fire_rate *= (1 - upgrade.value)  # Reduce cooldown

        # Track purchase
        upgrade.purchase_count += 1

        return True

    def draw(self, screen, player, inventory, world_manager):
        """
        Draw upgrade shop

        Args:
            screen: Pygame screen surface
            player: Player object
            inventory: Inventory object
            world_manager: WorldManager object
        """
        # Semi-transparent background overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(230)
        overlay.fill(self.BG_COLOR)
        screen.blit(overlay, (0, 0))

        # Title
        title_text = self.title_font.render("UPGRADE SHOP", True, (100, 200, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(title_text, title_rect)

        # Coins display
        coins_text = self.font.render(f"Coins: {inventory.coins}", True, (255, 215, 0))
        coins_rect = coins_text.get_rect(center=(self.screen_width // 2, 140))
        screen.blit(coins_text, coins_rect)

        # World info
        world_info = world_manager.get_current_world_info()
        world_text = self.small_font.render(
            f"{world_info['name']} - Round {world_info['rounds_completed']}",
            True,
            (150, 150, 150)
        )
        world_rect = world_text.get_rect(center=(self.screen_width // 2, 170))
        screen.blit(world_text, world_rect)

        # Draw upgrade buttons
        mouse_pos = pygame.mouse.get_pos()

        for i, (upgrade, button_rect) in enumerate(zip(self.upgrades, self.upgrade_buttons)):
            # Determine if affordable
            can_afford = inventory.coins >= upgrade.cost
            color = self.AFFORDABLE_COLOR if can_afford else self.EXPENSIVE_COLOR

            # Check hover
            hovered = button_rect.collidepoint(mouse_pos)
            if hovered and can_afford:
                color = (120, 200, 120)
            elif hovered:
                color = (200, 120, 120)

            # Draw button background
            pygame.draw.rect(screen, color, button_rect)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)

            # Draw upgrade name
            name_text = self.font.render(upgrade.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(
                centerx=button_rect.centerx,
                top=button_rect.top + 10
            )
            screen.blit(name_text, name_rect)

            # Draw description
            desc_text = self.small_font.render(upgrade.description, True, (200, 200, 200))
            desc_rect = desc_text.get_rect(
                centerx=button_rect.centerx,
                top=button_rect.top + 40
            )
            screen.blit(desc_text, desc_rect)

            # Draw cost
            cost_color = (255, 215, 0) if can_afford else (150, 100, 100)
            cost_text = self.small_font.render(f"Cost: {upgrade.cost} coins", True, cost_color)
            cost_rect = cost_text.get_rect(
                centerx=button_rect.centerx,
                bottom=button_rect.bottom - 5
            )
            screen.blit(cost_text, cost_rect)

            # Show purchase count
            if upgrade.purchase_count > 0:
                count_text = self.small_font.render(
                    f"(x{upgrade.purchase_count})",
                    True,
                    (150, 150, 150)
                )
                count_rect = count_text.get_rect(
                    left=button_rect.right + 10,
                    centery=button_rect.centery
                )
                screen.blit(count_text, count_rect)

        # Draw continue button
        continue_color = self.BUTTON_HOVER_COLOR if self.continue_button_hovered else self.BUTTON_COLOR
        pygame.draw.rect(screen, continue_color, self.continue_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.continue_button_rect, 2)

        continue_text = self.font.render("Continue", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=self.continue_button_rect.center)
        screen.blit(continue_text, continue_text_rect)

        # Draw timer
        timer_color = (255, 100, 100) if self.time_remaining < 5 else (200, 200, 200)
        timer_text = self.small_font.render(
            f"Shop closes in: {self.time_remaining:.1f}s",
            True,
            timer_color
        )
        timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height - 120))
        screen.blit(timer_text, timer_rect)

        # Player stats preview (left side)
        self._draw_stats_preview(screen, player)

    def _draw_stats_preview(self, screen, player):
        """
        Draw player stats preview

        Args:
            screen: Pygame screen surface
            player: Player object
        """
        stats_x = 30
        stats_y = 220

        stats_title = self.font.render("Your Stats:", True, (100, 200, 255))
        screen.blit(stats_title, (stats_x, stats_y))

        stats = [
            f"Max HP: {player.max_hp}",
            f"Current HP: {int(player.hp)}",
            f"Speed: {player.speed:.1f}",
            f"Damage: {player.damage}"
        ]

        y_offset = stats_y + 40
        for stat in stats:
            stat_text = self.small_font.render(stat, True, (200, 200, 200))
            screen.blit(stat_text, (stats_x, y_offset))
            y_offset += 30
