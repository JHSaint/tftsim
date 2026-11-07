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
- CSV import of unit base stats (file picker or pasted text)
- Team builder: a tile for every imported unit, click to add it to the board

## Controls

- Click an empty hex to place a unit, click a unit to inspect or edit it, right-click a unit to remove it
- Start, pause, reset, random boards, stage (affects Fighter attack speed), speed, seed

## CSV import

One row per unit with its 1-star base stats (star scaling is applied by the sim). See `sample-units.csv`. Import it from the "Unit roster" section, then choose the unit in the Unit menu before placing it. Importing replaces the previous roster; units already on the board keep their stats.

| Column (case-insensitive, other spellings accepted) | Notes |
|---|---|
| `name` (or unit, champion) | Required |
| `role` | Team role: Tank, Fighter, Assassin, Marksman, Caster or Specialist. May also include the damage type, for example `Attack Tank` ("Assasin" is accepted as a typo for Assassin) |
| `damage_type` | Physical (or Attack), Magic, or Both (or Hybrid). Overrides the damage type in `role` |
| `hp`, `ad`, `ap`, `attack_speed`, `armor`, `magic_resist`, `range` | Numbers |
| `crit_chance`, `crit_damage`, `damage_amp`, `durability` | Percentages written as 25, not 0.25 |
| `mana`, `mana_per_attack`, `mana_per_second` | Max mana and role mana rules |
| `cost` (optional) | Gold cost, 1 to 5. Groups the team builder and sets the tile border colour. The colours live in the `COSTCOL` constant in the script, not in the CSV |
| `image` (optional) | An `https://` URL or a `data:image/...` URI. Quote data URIs, since they contain a comma |

Missing columns use the role defaults. Unknown columns are ignored and listed after import. Commas, semicolons and tabs are detected as delimiters, quoted fields and Windows line endings are handled, and bad values are reported and replaced by role defaults.

## Team builder

Every unit in the imported CSV appears as a tile, grouped by cost with the cost colour as the border. Search and role filters narrow the list, and "Clear blue" / "Clear red" empty one side.

- **Drag a tile onto the board.** The half of the board you drop it on decides its team (rows a-d on top are red, on the bottom are blue). Dropping on an occupied hex is refused.
- **Click a tile** to add the unit to the team selected in the placement bar, **right-click** to add it to the other team. Melee units go to the front rows and ranged units to the back rows, centre columns first.
- **Drag units already on the board** to move them to an empty hex, or onto another unit to swap places. Dropping off the board changes nothing. Click without moving to select a unit and edit its stats.
- Moving and adding are disabled while a fight is running or finished: press Reset first.
- Tile dragging uses pointer events and works with mouse and pen. On touch screens tap a tile to add it and drag units on the board.

Images: the `image` column holds an `https://` URL or a `data:image/...` URI (quote data URIs, since they contain a comma). Images show on the tiles, on the board and on the drag ghost. If an image is missing or blocked the unit's initials are shown instead. Pages served from `claude.ai` block remote images, so initials show there; from GitHub Pages or a local file the images load. When served over http the page also loads `units-set18.csv` from its own folder on start.

## Design notes

- The board is symmetric under a 180° rotation, so a unit at column `n` on one side mirrors column `8-n` on the other (same row letter)
- All damage in a tick lands together, and unit order is shuffled each tick, so neither side has a built-in advantage
- Targeting: lowest hex distance, then Tanks, then a seeded random pick among ties
- Ranged units pick targets before melee units move

## Known approximations

This is a reverse-engineered approximation, not Riot's engine. In particular:

- Role stats, spell damage and star scaling (spell damage ×1.5 per star is unverified; HP and AD ×1.8 per star match MetaBot's Set 18 stats) are placeholders, all editable in the constants at the top of the script
- Base crit damage defaults to 140% and is unverified
- Tank mana from damage taken uses 1% pre-mitigation plus 3% post-mitigation, capped at 42 per hit, from memory
- Order of damage amp, resists and durability is an assumption
- Tie-breaking and movement timing (0.55s per hex) are guesses

## Data

`units-set18.csv` has the 65 Set 18 (Enchanted Wilds) units with 1-star base stats (health, AD, attack speed, armor, MR, range, max mana), taken from MetaBot's Set 18 champion stats table (page dated 6 Nov 2026; the exact patch it reflects is not stated). Role, damage type, AP, crit and crit damage are blank and use the role defaults until filled in. Stats change between patches, so re-check against the game.

## Not yet implemented

Items, traits, augments, shields, healing, real champion abilities and data, crowd control.

## Rules sources

Role mana rules follow Riot's "Roles Revamped and Item Changes" article (Set 15 launch) with the patch 15.4 changes (Fighter omnivamp replaced by scaling attack speed, ranged units targeting before melee move). Patch 15.4 merged Assassin into Fighter, but the Set 18 unit data lists Assassins, so the sim treats Assassin as its own role again using the 15.1 launch rules: 10 mana per attack and less likely to be targeted (the tie-break puts Tanks first and Assassins last). That is an assumption. Roles may have changed in later sets.
