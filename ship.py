"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Draw the player ship, handle movement, and delegate firing.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


class Ship:
    """Represent the player ship and its active shots."""


    def __init__(self, game: "AlienInvasion", arsenal: "Arsenal"):
        """Load the ship sprite and place it at the bottom of the screen."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w, self.settings.ship_h)
            )

        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False
        self.arsenal = arsenal

    def _center_ship(self):
        """Move the ship to the center of the bottom edge."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Advance ship movement and all active shots by one frame."""
        # Update the ship's position based on movement flags
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Move the ship according to the held arrow keys."""
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed

        self.rect.x = self.x

    def draw(self):
        """Draw the active shots and ship on the game screen."""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self, mode=None):
        """Fire the selected mode if the arsenal allows a shot; report success."""
        return self.arsenal.fire_bullet(mode)

    def check_collisions(self, other_group):
        """Recenter the ship and report whether it touched another sprite."""
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
