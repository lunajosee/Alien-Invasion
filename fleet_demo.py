"""Program Name: Twin Cannons - Track 1 - Milestone 2
Author: Jose Luna
Purpose: Demonstrate fleet combat, lives, and wave progression.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 21, 2026
"""

import pygame

from alien_fleet import AlienFleet
from training_range import TrainingRange


class FleetDemo(TrainingRange):
    """Demonstrate combat and loss conditions without the final UI."""

    def __init__(self):
        """Initialize the player, starting lives, and first enemy wave."""
        super().__init__()
        self.wave = 1
        self.lives = self.settings.starting_ship_count
        self.playing = True
        self.alien_fleet = AlienFleet(self)
        self._reset_wave()
        self._update_caption()

    def _select_mode(self, mode):
        """Choose the weapon used by subsequent shots."""
        self.mode = mode

    def _update_caption(self):
        """Show demo status without loading the final HUD."""
        status = "Playing" if self.playing else "Lost - Q or Esc to quit"
        pygame.display.set_caption(
            f"Twin Cannons - Track 1 - Milestone 2 | "
            f"Wave {self.wave} | Lives {self.lives} | "
            f"{self.mode.title()} | {status}"
        )

    def _reset_wave(self):
        """Clear shots, center the player, and create the current wave."""
        self.ship.arsenal.reset()
        self.ship._center_ship()
        self.ship.moving_left = False
        self.ship.moving_right = False
        self.alien_fleet.create_fleet(self.wave)

    def _check_collisions(self):
        """Resolve a player breach, projectile damage, or a cleared wave."""
        fleet = self.alien_fleet

        if self.ship.check_collisions(fleet.fleet) or fleet.check_fleet_bottom():
            self._lose_life()
            return

        fleet.check_collisions(self.ship.arsenal.arsenal)

        if not fleet.fleet:
            self.wave += 1
            self.settings.increase_difficulty()
            self._reset_wave()
            print(f"Starting wave {self.wave}")

    def _lose_life(self):
        """Subtract one life and stop gameplay when none remain."""
        self.lives -= 1
        print(f"Life lost. Lives remaining: {self.lives}")

        if self.lives > 0:
            self._reset_wave()
        else:
            self.playing = False
            self.ship.arsenal.reset()
            self.ship.moving_left = False
            self.ship.moving_right = False
            print("Demo ended: no lives remain. Press Q or Esc to quit.")

    def _handle_events(self):
        """Use prototype controls during play and allow quitting after loss."""
        if self.playing:
            return super()._handle_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False

        return True

    def run(self):
        """Run combat while playing and keep the window visible after loss."""
        try:
            while self._handle_events():
                if self.playing:
                    self.ship.update()
                    self.alien_fleet.update_fleet()
                    self._check_collisions()

                self._update_caption()
                self.screen.blit(self.background, (0, 0))
                self.ship.draw()
                self.alien_fleet.draw()

                pygame.display.flip()
                self.clock.tick(self.settings.FPS)
        finally:
            pygame.quit()


if __name__ == "__main__":
    FleetDemo().run()