"""
Powerup class - defines powerup effects
"""


class Powerup:
    """
    Temporary buff that enhances player abilities
    """

    def __init__(self, powerup_type, duration=10.0):
        """
        Initialize powerup

        Args:
            powerup_type (str): Type of powerup (SPEED, DAMAGE, SHIELD, INVINCIBILITY)
            duration (float): How long the powerup lasts in seconds
        """
        self.powerup_type = powerup_type
        self.duration = duration
        self.time_remaining = duration
        self.active = False

        # Set powerup-specific properties
        if powerup_type == "SPEED":
            self.name = "Speed Boost"
            self.speed_multiplier = 1.5
            self.damage_multiplier = 1.0
            self.shield = False
            self.invincible = False
            self.color = (100, 200, 255)  # Light blue

        elif powerup_type == "DAMAGE":
            self.name = "Damage Boost"
            self.speed_multiplier = 1.0
            self.damage_multiplier = 2.0
            self.shield = False
            self.invincible = False
            self.color = (255, 100, 100)  # Red

        elif powerup_type == "SHIELD":
            self.name = "Shield"
            self.speed_multiplier = 1.0
            self.damage_multiplier = 1.0
            self.shield = True
            self.invincible = False
            self.color = (100, 255, 255)  # Cyan
            self.duration = 15.0  # Shield lasts longer
            self.time_remaining = 15.0

        elif powerup_type == "INVINCIBILITY":
            self.name = "Invincibility"
            self.speed_multiplier = 1.0
            self.damage_multiplier = 1.5
            self.shield = False
            self.invincible = True
            self.color = (255, 255, 100)  # Yellow
            self.duration = 5.0  # Shorter duration
            self.time_remaining = 5.0

        else:
            # Default powerup
            self.name = "Unknown"
            self.speed_multiplier = 1.0
            self.damage_multiplier = 1.0
            self.shield = False
            self.invincible = False
            self.color = (200, 200, 200)

    def activate(self, player):
        """
        Activate powerup effect on player

        Args:
            player: Player object
        """
        self.active = True

        # Apply speed boost
        if self.speed_multiplier != 1.0:
            player.base_speed = player.speed
            player.speed *= self.speed_multiplier

        # Apply damage boost
        if self.damage_multiplier != 1.0:
            player.base_damage = player.damage
            player.damage = int(player.damage * self.damage_multiplier)

        # Apply shield
        if self.shield:
            player.has_shield = True

        # Apply invincibility
        if self.invincible:
            player.is_invincible = True

    def update(self, dt, player):
        """
        Update powerup timer

        Args:
            dt (float): Delta time in seconds
            player: Player object

        Returns:
            bool: True if powerup is still active
        """
        if not self.active:
            return False

        self.time_remaining -= dt

        if self.time_remaining <= 0:
            self.deactivate(player)
            return False

        return True

    def deactivate(self, player):
        """
        Remove powerup effect from player

        Args:
            player: Player object
        """
        self.active = False

        # Remove speed boost
        if self.speed_multiplier != 1.0 and hasattr(player, 'base_speed'):
            player.speed = player.base_speed

        # Remove damage boost
        if self.damage_multiplier != 1.0 and hasattr(player, 'base_damage'):
            player.damage = player.base_damage

        # Remove shield
        if self.shield:
            player.has_shield = False

        # Remove invincibility
        if self.invincible:
            player.is_invincible = False

    def get_display_info(self):
        """
        Get powerup info for UI display

        Returns:
            dict: Powerup display information
        """
        return {
            'name': self.name,
            'time_remaining': self.time_remaining,
            'duration': self.duration,
            'color': self.color,
            'active': self.active
        }


def create_powerup(powerup_type):
    """
    Factory function to create powerups

    Args:
        powerup_type (str): Type of powerup to create

    Returns:
        Powerup: New powerup instance
    """
    return Powerup(powerup_type)
