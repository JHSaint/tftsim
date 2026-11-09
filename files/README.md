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
- Layout: on screens 1060px or wider, the Combat log is on the left, the board in the middle and the Selected unit panel on the right. Team builder, Traits, Board state and Unit roster follow below at full width, with the roster last. Between 700 and 1059px the board and Selected unit sit side by side with the log underneath; below 700px everything stacks. The Blue/Red toggle lives in the Team builder, and a label in the top bar shows which team board clicks place for. Role and damage type are dropdowns next to the Unit menu
- Collapsible panels (Team builder, Unit roster, Traits, Selected unit, Board state, Combat log) with Collapse all / Expand all; closed panels are remembered in the browser
- Team builder: a tile for every imported unit, click to add it to the board
- Selected unit panel: in setup it shows a Base / Bonus / Total table for every stat (health, mana, AD, AP, attack speed, armor, MR, range, crit, crit damage, damage amp, durability, omnivamp, mana per attack/second) with current trait bonuses. During a fight it updates every frame: position, state, target, health and mana bars, damage dealt/taken/per second, trait bonuses and stacks (Rapidfire, Spellweaver, Hunter, Monolith and so on). Switching units mid-fight works

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

Every unit in the imported CSV appears as a tile, grouped by cost with the cost colour as the border. Search (by unit name or trait) and the role filter narrow the list, and "Clear blue" / "Clear red" empty one side.

- **Drag a tile onto the board.** The half of the board you drop it on decides its team (rows a-d on top are red, on the bottom are blue). Dropping on an occupied hex is refused.
- **Click a tile** to add the unit to the team selected in the placement bar, **right-click** to add it to the other team. Melee units go to the front rows and ranged units to the back rows, centre columns first.
- **Drag units already on the board** to move them to an empty hex, or onto another unit to swap places. Dropping off the board changes nothing. Click without moving to select a unit and edit its stats.
- Moving and adding are disabled while a fight is running or finished: press Reset first.
- Tile dragging uses pointer events and works with mouse and pen. On touch screens tap a tile to add it and drag units on the board.

Images: the `image` column holds an `https://` URL or a `data:image/...` URI (quote data URIs, since they contain a comma). Images show on the tiles, on the board and on the drag ghost. If an image is missing or blocked the unit's initials are shown instead. Pages served from `claude.ai` block remote images, so initials show there; from GitHub Pages or a local file the images load. When served over http the page also loads `units-set18.csv` from its own folder on start.

## Traits (phase 3)

Stat-only traits and the combat-triggered stat bonuses listed below affect fights. Other traits show in the trait panel greyed out with no effect.

- `units-set18.csv` has a `traits` column: semicolon-separated names per unit (for example `Attuned;Lunar;Spellweaver`). Lux lists only `Avatar`; pick her origin in the inspector. Membership came from op.gg's Set 18 page, where the unit view and the trait view agree on all 65 units and 36 traits.
- `traits.csv` defines the traits, one row per breakpoint and effect. `bucket` is **A** (static bonus), **B** (bonus that changes during combat) or **C** (mechanics, not modelled). `scope` is `team`, `members` (units with the trait) or `adjacent_allies`. Rows with a `trigger` are dynamic; `param` is the stack cap, interval or threshold for that trigger. Traits with only a summary row (Attuned, Fae, Old Growth, Thornmaiden and the C traits) have no effect. The page embeds the same data as defaults. Importing a `traits.csv` (file picker or paste box, detected automatically) or serving it next to `index.html` over http replaces them.
- Numbers start from op.gg's launch values and apply Riot's patch notes 18.2 to 18.6. `confidence` and `notes` say which were cross-checked. Re-check after each patch.

Static bonuses are applied at combat start, separately for each team:

- A trait is active at the highest breakpoint not above its count. Counts use unique champions (two copies of one champion count once) and Lux counts her chosen origin twice.
- `team` bonuses go to every unit on the team, `members` bonuses to units with the trait. Where a trait has both, member bonuses add on top of the team bonus, except Invoker, whose wording lists the team and Invoker amounts separately, so the Invoker value replaces it (`MEMBER_MODE` in the script). The rule follows the trait wording: "Your team gains X. Members gain more" means the team value applies to everyone and members get it plus the extra (Defender 2: 37 armor for Defenders, 12 for the rest).
- Lunar: members get double the listed value; other allies get the listed value only if they are directly adjacent to a Lunar champion at combat start. There is no whole-team option.
- Adaptor puts its bonus on whichever of AD or AP is higher. Stats that are themselves percentages (durability, crit, omnivamp) add percentage points. Ravager's omnivamp heals for a share of damage dealt.

Combat-triggered bonuses (`trigger` column):

| Trigger | Trait | Effect |
|---|---|---|
| `per_attack` | Rapidfire | Attack speed per attack, up to `param` stacks |
| `per_cast` | Spellweaver | AP per cast, no cap |
| `no_target_swap` | Hunter | Damage amp after `param` seconds on the same target; resets when the target changes |
| `double_vs_low_health` | Ravager | Damage amp, doubled against targets below `param`% health |
| `per_enemy_targeting` | Monolith | Armor and MR per enemy currently targeting the unit |
| `on_takedown` | (none yet) | Stat per takedown, up to `param` stacks if set. A takedown is a kill or an assist |
| `every_seconds` | Riftbeast (7 and 10) | AD and AP every `param` seconds, stacking. The other stats this trait grows are not modelled |

The "Apply trait bonuses" checkbox turns all trait effects off, which is useful for comparing with and without traits using "Run 200 fights".

## Takedowns

When a unit dies, credit is decided after all of that tick's damage has landed:

- The unit whose hit brought the victim to 0 health gets the kill, but only if it is still alive after the tick. If it died in the same tick, nobody gets the kill.
- Any other living enemy of the victim that damaged it within the last `ASSIST_WINDOW` seconds (3, unverified) gets an assist.
- A kill or an assist is one takedown. Credit is given once per death. Takedowns show in the Selected unit panel and the combat log, and `on_takedown` traits stack on each one.

## Board state (for bug reports)

"Copy board state" copies a text snapshot to the clipboard and shows it in the Board state box. It lists every unit with its side, name and position, the trait counts per side, and, if a fight exists, the current position, health, mana, target and state of every unit. Positions are `top` or `bot` (the half of the board), a row letter `a`-`d` counting out from the centre line, and a column `1`-`7` left to right, for example `bot-d4`, with the 0-based `[c,r]` coordinates next to them. The last line is a `DATA` JSON line that "Load pasted state" reads to rebuild the board, stage, seed and trait settings. The same seed and setup replay the same fight.

## Design notes

- The board is symmetric under a 180° rotation, so a unit at column `n` on one side mirrors column `8-n` on the other (same row letter)
- All damage in a tick lands together, and unit order is shuffled each tick, so neither side has a built-in advantage
- Targeting: lowest hex distance, then Tanks over others (Assassins last), then the true centre-to-centre distance on the board (a unit straight ahead beats one off to the side at the same hex distance), then a seeded random pick for exact ties such as mirror-image positions. The same ordering picks the replacement target when a blocked unit retargets
- Blocked units retarget: each time a unit steps, it measures the real route to its target around other units. If that route is 2 or more steps longer than the straight one (or there is none), it switches to the enemy it can reach in the fewest steps (closest, then Tanks, then a seeded random pick). Unblocked units keep their target until it dies. `BLOCK_SLACK` in the script sets the threshold
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
