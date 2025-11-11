"""
Inventory class - manages player's collected items
"""
from weapon import create_weapon


class Inventory:
    """
    Player inventory system for weapons, powerups, and coins
    """

    def __init__(self):
        """Initialize inventory"""
        # Weapon slots (max 3)
        self.weapons = [
            create_weapon("PISTOL"),  # Start with pistol
            None,
            None
        ]
        self.active_weapon_index = 0
        self.max_weapons = 3

        # Powerups (active buffs)
        self.powerups = []

        # Currency
        self.coins = 0

    def get_active_weapon(self):
        """
        Get currently equipped weapon

        Returns:
            Weapon: Active weapon
        """
        return self.weapons[self.active_weapon_index]

    def switch_weapon(self, index):
        """
        Switch to weapon at index

        Args:
            index (int): Weapon slot index (0-2)

        Returns:
            bool: True if switch successful
        """
        if 0 <= index < self.max_weapons and self.weapons[index] is not None:
            self.active_weapon_index = index
            return True
        return False

    def add_weapon(self, weapon_type):
        """
        Add weapon to inventory

        Args:
            weapon_type (str): Type of weapon to add

        Returns:
            bool: True if added successfully
        """
        # Check if we already have this weapon type
        for i, weapon in enumerate(self.weapons):
            if weapon and weapon.weapon_type == weapon_type:
                # Already have it, just switch to it
                self.active_weapon_index = i
                return True

        # Try to find empty slot
        for i, weapon in enumerate(self.weapons):
            if weapon is None:
                self.weapons[i] = create_weapon(weapon_type)
                self.active_weapon_index = i
                return True

        # No empty slots, replace current weapon
        self.weapons[self.active_weapon_index] = create_weapon(weapon_type)
        return True

    def add_powerup(self, powerup):
        """
        Add and activate powerup

        Args:
            powerup (Powerup): Powerup to add
        """
        self.powerups.append(powerup)

    def update_powerups(self, dt, player):
        """
        Update all active powerups

        Args:
            dt (float): Delta time in seconds
            player: Player object
        """
        # Update all powerups
        active_powerups = []
        for powerup in self.powerups:
            if powerup.update(dt, player):
                active_powerups.append(powerup)

        self.powerups = active_powerups

    def add_coins(self, amount):
        """
        Add coins to inventory

        Args:
            amount (int): Number of coins to add
        """
        self.coins += amount

    def spend_coins(self, amount):
        """
        Spend coins

        Args:
            amount (int): Number of coins to spend

        Returns:
            bool: True if enough coins, False otherwise
        """
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    def get_weapon_display_info(self):
        """
        Get weapon info for UI display

        Returns:
            list: List of weapon info dicts
        """
        weapon_info = []
        for i, weapon in enumerate(self.weapons):
            if weapon:
                info = weapon.get_display_info()
                info['slot'] = i + 1
                info['active'] = (i == self.active_weapon_index)
                weapon_info.append(info)
            else:
                weapon_info.append({
                    'slot': i + 1,
                    'name': 'Empty',
                    'active': False
                })

        return weapon_info

    def get_powerup_display_info(self):
        """
        Get powerup info for UI display

        Returns:
            list: List of active powerup info dicts
        """
        return [p.get_display_info() for p in self.powerups if p.active]

    def update_weapons(self, dt):
        """
        Update all weapon cooldowns

        Args:
            dt (float): Delta time in seconds
        """
        for weapon in self.weapons:
            if weapon:
                weapon.update(dt)
