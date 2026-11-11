"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Configure assets and the two weapon modes.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

from pathlib import Path
class Settings:
    """Store the asset paths, game constants, and adjustable settings."""

    def __init__(self):
        """Set window dimensions, paths, and static game options."""
        assets_dir = Path(__file__).resolve().parent / "Assets"
        self.name = "Alien Invasion: Twin Cannons - Track 1"
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = assets_dir / 'images' / "Starbasesnow.png"
        self.difficulty_scale = 1.12
        self.scores_file = assets_dir / 'file' / "scores.json"

        self.ship_file = assets_dir / 'images' / "ship2(no bg).png"
        self.ship_w = 40
        self.ship_h = 60
        self.bullet_file = assets_dir / 'images' / "laserBlast.png"
        self.laser_sound = assets_dir / 'sound' / "laser.mp3"
        self.impact_sound = assets_dir / 'sound' / "impactSound.mp3"

        self.alien_file = assets_dir / 'images' / "enemy_4.png"
        self.alien_w = 40
        self.alien_h = 40

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0, 135, 50)

        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = assets_dir / 'Fonts' / 'Silkscreen' / 'Silkscreen-Regular.ttf'

    def initialize_dynamic_settings(self):
        """Restore starting speeds and weapon rules."""
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_speed = 7
        self.bullet_amount = 5
        self.weapon_modes = {
            'rapid': {'size': (14, 44), 'speed': 10, 'damage': 1, 'cooldown_ms': 140},
            'power': {'size': (36, 86), 'speed': 6, 'damage': 2, 'cooldown_ms': 520},
        }

        self.fleet_speed = 3
        self.fleet_drop_speed = 60
        self.alien_points = 50

    def increase_difficulty(self):
        """Speed up later fleets without changing the weapons or ship."""
        self.fleet_speed = min(6, self.fleet_speed * self.difficulty_scale)
