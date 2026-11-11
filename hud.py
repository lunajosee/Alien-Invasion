"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Draw the menu and the weapon, score, wave, and lives displays.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import pygame


class HUD:
    """Show the current weapon, cooldown, wave, lives, and scores."""

    def __init__(self, game):
        """Load the HUD font and establish the dimensions used for layout."""
        self.game = game
        self.screen = game.screen
        self.bounds = self.screen.get_rect()
        settings = game.settings
        font_path = str(settings.font_file)
        self.font = pygame.font.Font(font_path, settings.HUD_font_size)
        self.title_font = pygame.font.Font(font_path, 54)
        self.muted = (181, 200, 217)
        self.ink = (239, 246, 250)
        self.cyan = (106, 225, 246)
        self.gold = (250, 200, 77)

    def draw(self):
        """Draw live game values and indicate when the next shot is available."""
        game = self.game
        stats = game.game_stats
        pygame.draw.rect(self.screen, (11, 21, 35), (0, 0, self.bounds.width, 84))
        mode = game.weapon_mode
        weapon = game.settings.weapon_modes[mode]
        color = self.cyan if mode == "rapid" else self.gold
        arsenal = game.ship.arsenal
        if pygame.time.get_ticks() < arsenal.next_shot_ms:
            status = "Recharging"
        elif len(arsenal.arsenal) >= game.settings.bullet_amount:
            status = "Shot limit"
        else:
            status = "Ready"
        self._draw_text(f"{mode.title()}  /  {status}", (20, 14), color)
        self._draw_text(f"1 Rapid   2 Power   /   {weapon['damage']} damage",
                        (20, 46), self.muted)
        self._draw_text(f"Wave {stats.level}   /   Lives {stats.ship_count}",
                        (self.bounds.centerx, 14), self.ink, anchor="midtop")
        self._draw_text(f"Score {stats.score:,}", (self.bounds.right - 20, 14),
                        self.ink, anchor="topright")
        self._draw_text(f"Best {stats.hi_score:,}", (self.bounds.right - 20, 46),
                        self.muted, anchor="topright")

    def draw_menu(self, title, game_over):
        """Draw a dark menu overlay, with the score or instructions as appropriate."""
        overlay = pygame.Surface(self.bounds.size, pygame.SRCALPHA)
        overlay.fill((8, 15, 27, 219))
        self.screen.blit(overlay, (0, 0))
        center_x, center_y = self.bounds.center
        self._draw_text(title, (center_x, center_y - 133), self.ink,
                        anchor="midtop", font=self.title_font)
        if game_over:
            stats = self.game.game_stats
            subtitle = f"Score {stats.score:,}   /   Best {stats.hi_score:,}"
        else:
            subtitle = "ALIEN INVASION  /  TRACK 1: MECHANICS"
        self._draw_text(subtitle, (center_x, center_y - 61), self.cyan, anchor="midtop")
        self._draw_text("Arrow keys: move   /   Space: fire   /   1 or 2: switch",
                        (center_x, center_y + 65), self.ink, anchor="midtop")
        self._draw_text("Gold armor takes two Rapid hits or one Power hit.",
                        (center_x, center_y + 100), self.gold, anchor="midtop")

    def _draw_text(self, message, position, color, *, anchor="topleft", font=None):
        """Render text and align its requested anchor to the given point."""
        image = (font or self.font).render(message, True, color)
        self.screen.blit(image, image.get_rect(**{anchor: position}))
