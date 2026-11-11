"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Run the game loop and control transitions between screens.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame

from alien_fleet import AlienFleet
from arsenal import Arsenal
from button import Button
from game_stats import GameStats
from hud import HUD
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Run the menu, active game, and game-over screen."""

    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    def __init__(self):
        """Initialize Pygame, load game assets, and open the Play menu."""
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        size = (self.settings.screen_w, self.settings.screen_h)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(self.settings.name)
        self.bg = pygame.transform.scale(
            pygame.image.load(str(self.settings.bg_file)).convert(), size
        )
        self.clock = pygame.time.Clock()
        self.laser_sound = self._load_sound(self.settings.laser_sound, 0.7)
        self.impact_sound = self._load_sound(self.settings.impact_sound, 0.5)
        self.game_stats = GameStats(self)
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.weapon_mode = "rapid"
        self.hud = HUD(self)
        self.play_button = Button(self, "Play")
        self.state = self.MENU
        self.running = True

    @staticmethod
    def _load_sound(path, volume):
        """Load and set the volume of a sound when audio is available."""
        if pygame.mixer.get_init() is None:
            return None
        sound = pygame.mixer.Sound(str(path))
        sound.set_volume(volume)
        return sound

    def run_game(self):
        """Process input every frame and update gameplay only while playing."""
        try:
            while self.running:
                self._check_events()
                if not self.running:
                    break
                if self.state == self.PLAYING:
                    self.ship.update()
                    self.alien_fleet.update_fleet()
                    self._check_collisions()
                self._update_screen()
                self.clock.tick(self.settings.FPS)
        finally:
            self.game_stats.save_scores()
            pygame.quit()

    def restart_game(self):
        """Start a fresh run with three lives, wave one, and the Rapid weapon."""
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.weapon_mode = "rapid"
        self._reset_wave()
        self.state = self.PLAYING
        pygame.mouse.set_visible(False)

    def _reset_wave(self):
        """Clear shots and cooldown, center the ship, and create one fleet."""
        self.ship.arsenal.reset()
        self.ship._center_ship()
        self.ship.moving_left = self.ship.moving_right = False
        self.alien_fleet.create_fleet(self.game_stats.level)

    def _check_collisions(self):
        """Apply hits, subtract a life on a breach, or advance a cleared wave."""
        fleet = self.alien_fleet
        if self.ship.check_collisions(fleet.fleet) or fleet.check_fleet_bottom():
            self._lose_life()
            return

        hits, points = fleet.check_collisions(self.ship.arsenal.arsenal)
        if hits and self.impact_sound:
            self.impact_sound.play()
        if points:
            self.game_stats.add_points(points)

        if not fleet.fleet:
            self.game_stats.update_level()
            self.settings.increase_difficulty()
            self._reset_wave()

    def _lose_life(self):
        """Lose exactly one life and show the Play menu again at zero."""
        self.game_stats.ship_count -= 1
        if self.game_stats.ship_count > 0:
            self._reset_wave()
        else:
            self.state = self.GAME_OVER
            self.ship.arsenal.reset()
            self.ship.moving_left = self.ship.moving_right = False
            pygame.mouse.set_visible(True)
            self.game_stats.save_scores()

    def _update_screen(self):
        """Draw the fleet and HUD in play, or the Play screen while inactive."""
        self.screen.blit(self.bg, (0, 0))
        if self.state == self.PLAYING:
            self.ship.draw()
            self.alien_fleet.draw()
            self.hud.draw()
        else:
            title = "Game Over" if self.state == self.GAME_OVER else "Twin Cannons"
            self.hud.draw_menu(title, self.state == self.GAME_OVER)
            self.play_button.draw()
        pygame.display.flip()

    def _check_events(self):
        """Route keyboard and mouse input according to the current game state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.running = False
                    return
                if self.state == self.PLAYING:
                    self._handle_play_key(event.key)
                elif event.key == pygame.K_RETURN:
                    self.restart_game()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (self.state != self.PLAYING and event.button == 1
                        and self.play_button.check_clicked(event.pos)):
                    self.restart_game()
            elif event.type == pygame.WINDOWFOCUSLOST:
                self.ship.moving_left = self.ship.moving_right = False

    def _handle_play_key(self, key):
        """Move, choose a weapon, or fire a shot during the active game."""
        if key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif key == pygame.K_1:
            self.weapon_mode = "rapid"
        elif key == pygame.K_2:
            self.weapon_mode = "power"
        elif key == pygame.K_SPACE and self.ship.fire(self.weapon_mode):
            if self.laser_sound:
                self.laser_sound.play()
                self.laser_sound.fadeout(80)


if __name__ == "__main__":
    AlienInvasion().run_game()
