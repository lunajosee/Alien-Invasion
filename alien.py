"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Track alien health and display armored targets.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame


class Alien(pygame.sprite.Sprite):
    """An alien with one hit point, or two when protected by armor."""

    def __init__(self, fleet, x, y, armored=False):
        """Place the alien in the fleet and set its health and point value."""
        super().__init__()
        self.screen = fleet.game.screen
        self.image = fleet.alien_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.armored = armored
        self.health = 2 if armored else 1
        self.points = fleet.settings.alien_points * (2 if armored else 1)

    def take_hit(self, damage):
        """Subtract projectile damage and report whether the alien was destroyed."""
        self.health -= damage
        if self.health > 0:
            return False
        self.kill()
        return True

    def move(self, dx, dy):
        """Move by the fleet's shared offset, keeping fractional positions."""
        self.x += dx
        self.y += dy
        self.rect.topleft = (round(self.x), round(self.y))

    def draw_alien(self):
        """Draw the sprite and show a gold shield while armor is intact."""
        self.screen.blit(self.image, self.rect)
        if self.armored:
            color = (250, 200, 77) if self.health == 2 else (200, 120, 70)
            width = 3 if self.health == 2 else 1
            pygame.draw.rect(self.screen, color, self.rect, width, border_radius=6)
