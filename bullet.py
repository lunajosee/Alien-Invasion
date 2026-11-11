"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Create and move shots with the selected weapon properties.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """Represent a projectile with a size, speed, and damage value."""
    def __init__(self, game: "AlienInvasion", mode=None):
        """Load a shot for the selected mode and place it at the ship nose."""
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings
        self.mode = mode

        if mode is None:
            size = (self.settings.bullet_w, self.settings.bullet_h)
            self.speed = self.settings.bullet_speed
            self.damage = 1
        else:
            weapon = self.settings.weapon_modes[mode]
            size = weapon['size']
            self.speed = weapon['speed']
            self.damage = weapon['damage']

        image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(image, size)

        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Move the projectile upward one frame."""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the projectile at its current position."""
        self.screen.blit(self.image, self.rect)
        if self.mode == "power":
            pygame.draw.rect(self.screen, (250, 200, 77), self.rect, 1, border_radius=5)
