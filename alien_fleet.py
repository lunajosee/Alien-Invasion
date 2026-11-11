"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Create each wave and resolve movement and projectile hits.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame

from alien import Alien


class AlienFleet:
    """Spawn, move, and resolve projectile hits for each wave."""

    def __init__(self, game):
        """Load one shared alien sprite and start with an empty fleet."""
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = 1
        image = pygame.image.load(str(self.settings.alien_file)).convert_alpha()
        self.alien_image = pygame.transform.scale(
            image, (self.settings.alien_w, self.settings.alien_h)
        )

    def create_fleet(self, wave):
        """Replace the previous wave with two rows of normal and armored aliens."""
        self.fleet.empty()
        self.fleet_direction = 1
        columns = 8
        step_x = self.settings.alien_w + 30
        step_y = self.settings.alien_h + 22
        width = (columns - 1) * step_x + self.settings.alien_w
        start_x = (self.settings.screen_w - width) // 2
        for row in range(2):
            for column in range(columns):
                armored = (row + column + wave) % 3 == 0
                alien = Alien(
                    self, start_x + column * step_x, 125 + row * step_y, armored
                )
                self.fleet.add(alien)

    def update_fleet(self):
        """Move as a group, reversing once and dropping once at either wall."""
        if not self.fleet:
            return
        dx = self.settings.fleet_speed * self.fleet_direction
        left = min(alien.x for alien in self.fleet)
        right = max(alien.x + alien.rect.width for alien in self.fleet)
        dy = 0
        if dx > 0 and right + dx >= self.settings.screen_w:
            dx = self.settings.screen_w - right
            self.fleet_direction = -1
            dy = self.settings.fleet_drop_speed
        elif dx < 0 and left + dx <= 0:
            dx = -left
            self.fleet_direction = 1
            dy = self.settings.fleet_drop_speed
        for alien in self.fleet:
            alien.move(dx, dy)

    def check_collisions(self, bullets):
        """Spend each hit bullet on the nearest alien and return hits and points."""
        hits = points = 0
        for bullet in bullets.sprites():
            targets = pygame.sprite.spritecollide(bullet, self.fleet, False)
            if not targets:
                continue
            # Shots travel upward: the lowest overlapping alien is hit first.
            target = max(targets, key=lambda alien: alien.rect.bottom)
            bullet.kill()
            hits += 1
            if target.take_hit(bullet.damage):
                points += target.points
        return hits, points

    def check_fleet_bottom(self):
        """Report whether any alien has crossed the bottom of the playfield."""
        return any(alien.rect.bottom >= self.settings.screen_h for alien in self.fleet)

    def draw(self):
        """Draw all remaining aliens, including their armor indicators."""
        for alien in self.fleet:
            alien.draw_alien()
