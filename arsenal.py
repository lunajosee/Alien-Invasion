"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Manage active shots, cooldowns, and offscreen cleanup.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """Hold and update the shots currently in flight."""
    def __init__(self, game: "AlienInvasion"):
        """Create an empty projectile group and allow the first shot immediately."""
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()
        self.next_shot_ms = 0

    def reset(self):
        """Clear every shot and allow an immediate shot in the next wave."""
        self.arsenal.empty()
        self.next_shot_ms = 0

    def update_arsenal(self):
        """Move the shots and clear those that left the screen."""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """Remove shots that have fully passed the top edge."""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self):
        """Draw all active shots."""
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self, mode=None):
        """Create a shot when cooldown and shot limits allow; report success."""
        if len(self.arsenal) >= self.settings.bullet_amount:
            return False

        now = pygame.time.get_ticks()
        if mode is not None and now < self.next_shot_ms:
            return False

        self.arsenal.add(Bullet(self.game, mode))
        if mode is not None:
            self.next_shot_ms = now + self.settings.weapon_modes[mode]['cooldown_ms']
        return True
