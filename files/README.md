# TFT fight simulator

A single-file, dependency-free fight simulator for Teamfight Tactics-style combat on a hex board. Open `index.html` in a browser to run it. Nothing to install or build.

## Features

- 7×8 hex board (odd rows offset right), columns labelled 1–7 and rows a–d counting out from the centre on each side
- Nearest-enemy targeting by hex distance, step-by-step movement with pathfinding around other units
- Roles Revamped system: damage type (Attack, Magic, Hybrid) plus team role (Tank, Fighter, Marksman, Caster, Specialist) with role-based mana
- Editable stats per unit (health, AD, AP, attack speed, armor, MR, range, crit, damage amp, durability, mana) and star levels
- Damage pipeline: raw → crit → damage amp → armor/MR → durability → HP
- Seeded randomness: the same seed replays the same fight
- "Run 200 fights" Monte Carlo mode with win, loss and tie rates
- Combat log and per-unit damage totals

## Controls

- Click an empty hex to place a unit, click a unit to inspect or edit it, right-click a unit to remove it
- Start, pause, reset, random boards, stage (affects Fighter attack speed), speed, seed

## Design notes

- The board is symmetric under a 180° rotation, so a unit at column `n` on one side mirrors column `8-n` on the other (same row letter)
- All damage in a tick lands together, and unit order is shuffled each tick, so neither side has a built-in advantage
- Targeting: lowest hex distance, then Tanks, then a seeded random pick among ties
- Ranged units pick targets before melee units move

## Known approximations

This is a reverse-engineered approximation, not Riot's engine. In particular:

- Role stats, spell damage and star scaling (×1.8 HP, ×1.5 AD and spell damage per star) are placeholders, all editable in the constants at the top of the script
- Base crit damage defaults to 140% and is unverified
- Tank mana from damage taken uses 1% pre-mitigation plus 3% post-mitigation, capped at 42 per hit, from memory
- Order of damage amp, resists and durability is an assumption
- Tie-breaking and movement timing (0.55s per hex) are guesses

## Not yet implemented

Items, traits, augments, shields, healing, real champion abilities and data, crowd control.

## Rules sources

Role mana rules follow Riot's "Roles Revamped and Item Changes" article (Set 15 launch) with the patch 15.4 changes (Assassin merged into Fighter, Fighter omnivamp replaced by scaling attack speed, ranged units targeting before melee move). Roles may have changed in later sets.
