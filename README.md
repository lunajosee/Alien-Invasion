# Alien Invasion: Twin Cannons

**Jose Luna · Track 1: Custom Game Mechanics · `track_1_mechanics`**

This project builds on my [in-class Alien Invasion game](https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab). The new mechanic is choosing between a quick shot and a more powerful shot. The choice matters because gold armored aliens can survive one Rapid hit.

## Run the game

From the repository folder, activate your Python virtual environment and run:

```text
python -m pip install -r requirements.txt
python alien_invasion.py
```

The final build opens at the Play menu. To launch the isolated weapon prototype instead, run `python training_range.py`.

## Controls and rules

| Control | Action |
|---|---|
| Click Play or press Enter | Start a fresh run from the menu or Game Over |
| Left / Right | Move the ship |
| 1 / 2 | Select Rapid / Power |
| Space | Fire |
| Q or Esc | Quit |

- **Rapid** is narrow and fast. It deals one damage and can fire again after 140 milliseconds.
- **Power** is larger and slower. It deals two damage and takes 520 milliseconds to recharge. Switching weapons does not cancel the cooldown.
- Normal aliens take one damage to destroy; gold armored aliens take two. A damaged shield turns dim orange. Points are awarded only when an alien is destroyed.
- The fleet reverses direction and drops together at either side of the screen. Clearing the fleet starts a faster wave. If an alien touches the ship or reaches the bottom, you lose one life.
- At zero lives, the game stops updating the fleet and opens Game Over. Play resets the wave, lives, and weapon while preserving the high score.

## How the code fits together

- `alien_invasion.py`: runs the game loop and switches between the menu, playing, and Game Over.
- `ship.py`, `arsenal.py`, `bullet.py`: move the ship, enforce the shot limit and cooldown, and create the selected projectile.
- `alien.py`, `alien_fleet.py`: track enemy health, move the fleet together, and spend each projectile on one target.
- `settings.py`, `game_stats.py`, `button.py`, `hud.py`: configure the game, track and save scores, handle Play, and show the selected weapon and its readiness.

## Demo videos

- **Milestone_1_Demo:** Add your unlisted YouTube link if you recorded this milestone.
- **Milestone_2_Demo:** Add your unlisted YouTube link if you recorded this milestone.
- **Final_Project_Demo:** Replace this text with your unlisted YouTube link before submitting.

## Credits

- [In-class Alien Invasion starter code and existing art/audio](https://github.com/lunajosee/Alien-Invasion/commit/fce0cff1b927668d54dbe87686913285877a27ab)
- Silkscreen font: see [the included Open Font License](Assets/Fonts/Silkscreen/OFL.txt).
