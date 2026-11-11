"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Demonstrate Rapid and Power shots in the Milestone 1 training range.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame

from arsenal import Arsenal
from settings import Settings
from ship import Ship


class TrainingRange:
    """Run the player and weapons without starting the tutorial fleet or menus."""

    def __init__(self):
        """Load the background and sound, then create the player ship."""
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        size = (self.settings.screen_w, self.settings.screen_h)
        self.screen = pygame.display.set_mode(size)
        background = pygame.image.load(self.settings.bg_file).convert()
        self.background = pygame.transform.scale(background, size)
        self.clock = pygame.time.Clock()
        self.ship = Ship(self, Arsenal(self))
        self.laser = pygame.mixer.Sound(str(self.settings.laser_sound))
        self.laser.set_volume(0.7)
        self.mode = 'rapid'
        self._select_mode(self.mode)

    def _select_mode(self, mode):
        """Set the weapon used by the next shot and show it in the caption."""
        self.mode = mode
        pygame.display.set_caption(
            f'Alien Invasion: Twin Cannons - Track 1 ({mode.title()})'
        )

    def _handle_events(self):
        """Handle movement, weapon selection, and firing; return false to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_1:
                    self._select_mode('rapid')
                elif event.key == pygame.K_2:
                    self._select_mode('power')
                elif event.key == pygame.K_SPACE and self.ship.fire(self.mode):
                    self.laser.play()
                    self.laser.fadeout(80)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
        return True

    def run(self):
        """Update and draw the ship and bullets until the player quits."""
        try:
            while self._handle_events():
                self.ship.update()
                self.screen.blit(self.background, (0, 0))
                self.ship.draw()
                pygame.display.flip()
                self.clock.tick(self.settings.FPS)
        finally:
            pygame.quit()


if __name__ == '__main__':
    TrainingRange().run()
