"""Program Name: Alien Invasion: Twin Cannons - Track 1
Author: Jose Luna (project author)
Purpose: Track lives, wave, score, and the saved high score.
Starter Code Links: https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab
Date Updated: November 10, 2026
"""

import json


class GameStats:
    """Track the current run and retain a high score between sessions."""

    def __init__(self, game):
        """Load the saved record and initialize a run."""
        self.settings = game.settings
        self.path = self.settings.scores_file
        self.hi_score = self._load_score()
        self.saved_hi_score = self.hi_score
        self.reset_stats()

    def _load_score(self):
        """Return a valid nonnegative saved record, or zero on a new install."""
        try:
            scores = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return 0
        score = scores.get("hi_score") if isinstance(scores, dict) else None
        return score if type(score) is int and score >= 0 else 0

    def save_scores(self):
        """Persist a new record without rewriting the file every run."""
        if self.hi_score <= self.saved_hi_score:
            return
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps({"hi_score": self.hi_score}, indent=4) + "\n",
                encoding="utf-8",
            )
            temporary.replace(self.path)
        except OSError as error:
            print(f"Could not save the high score: {error}")
        else:
            self.saved_hi_score = self.hi_score

    def reset_stats(self):
        """Restore the starting lives, score, and wave without clearing the record."""
        self.ship_count = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def add_points(self, points):
        """Award points for destroyed aliens and update the record."""
        self.score += points
        self.hi_score = max(self.hi_score, self.score)

    def update_level(self):
        """Advance the wave number after the entire fleet is cleared."""
        self.level += 1
