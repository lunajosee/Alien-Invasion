"""Program Name: Twin Cannons - Track 1 - Milestone 2
Author: Jose Luna
Purpose: Demonstrate the player, weapons, and enemy fleet.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 21, 2026
"""

import pygame

from alien_fleet import AlienFleet
from training_range import TrainingRange


class FleetDemo(TrainingRange):
    """Extend the weapon prototype with a moving enemy fleet."""

    def __init__(self):
        """Set up the existing prototype and create the first fleet."""
        super().__init__()
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet(1)

    def _select_mode(self, mode):
        """Select a weapon and identify this demo in the window caption."""
        self.mode = mode
        pygame.display.set_caption(
            f"Twin Cannons - Track 1 - Milestone 2 ({mode.title()})"
        )

    def run(self):
        """Update and draw the player, weapons, and fleet until quitting."""
        try:
            while self._handle_events():
                self.ship.update()
                self.alien_fleet.update_fleet()

                self.screen.blit(self.background, (0, 0))
                self.ship.draw()
                self.alien_fleet.draw()

                pygame.display.flip()
                self.clock.tick(self.settings.FPS)
        finally:
            pygame.quit()


if __name__ == "__main__":
    FleetDemo().run()