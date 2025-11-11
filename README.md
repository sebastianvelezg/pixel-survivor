# 🕹️ Pixel Survivor: Worlds

## 📖 Overview

Pixel Survivor: Worlds is a single-player **top-down arena survival** game built in Python with Pygame.
You fight off endless waves of enemies across multiple worlds, progressing through increasingly difficult stages until you reach the ultimate challenge — World 10, where you must survive 100 rounds of relentless combat.

The game blends arcade-style action, procedural enemy generation, and progressive difficulty scaling, all wrapped in nostalgic retro pixel art.

## 🌍 Gameplay Structure

| World | Rounds to Complete | Difficulty Scaling |
|-------|-------------------|--------------------|
| 1 | 10 | Basic enemies, slow speed |
| 2 | 20 | Faster enemies, tighter spawn intervals |
| 3 | 30 | New enemy types (ranged/melee) |
| 4 | 40 | Faster projectile speed |
| 5 | 50 | Environmental hazards introduced |
| 6 | 60 | Elite enemies spawn |
| 7 | 70 | Mini-bosses appear every 10 rounds |
| 8 | 80 | Double spawn rates |
| 9 | 90 | Enemies gain increased health and damage |
| 10 | 100 | Final "Endless World" — survive as long as possible |

Each world must be cleared (all rounds completed) before the player can unlock the next.
Difficulty increases gradually, encouraging skill growth and mastery.

## ⚔️ Core Gameplay

- **Top-down arena** with 360° movement and combat
- **Player controls:**
  - **WASD** - Move in all directions
  - **Mouse** - Aim and control look direction
  - **Left Click / Spacebar** - Attack or shoot
- **Objective:** Survive every round by defeating all spawned enemies
- **Between rounds:** Short cooldown or upgrade screen
- **After 10 worlds:** Unlock "Endless Mode"

## 💥 Key Features

- 🎮 Single-player arcade action
- 🌌 10 unique worlds, each with progressive enemy scaling
- 🔄 Round-based survival (waves of enemies)
- ⚙️ Procedural enemy spawns and positioning
- 🧠 AI-driven enemies that chase or shoot at the player
- 🎒 **Drop & Inventory System** - collect health, weapons, and power-ups from defeated enemies
- 🧱 Pixel art design (retro-style visuals)
- 🔊 Sound effects and background music
- 💾 Save/load progression system (world and round tracking)
- 🧩 Expandable system for new worlds, power-ups, and weapons

## 🎒 Drop & Inventory System

### Drops
When enemies are defeated, they have a chance to drop valuable items in the world:

- **💊 Health Packs** - Restore player HP (10%, 25%, or 50%)
- **🔫 Weapons** - New guns with different stats (pistol, shotgun, rifle, plasma gun)
- **⚡ Power-ups** - Temporary buffs
  - Speed boost (10 seconds)
  - Damage multiplier (15 seconds)
  - Shield (absorbs 3 hits)
  - Invincibility (5 seconds)
- **💰 Coins** - Currency for upgrades between rounds

### Inventory System
- **Weapon Slots**: Hold up to 3 weapons, switch with number keys (1, 2, 3)
- **Active Power-ups**: Display remaining duration on HUD
- **Auto-pickup**: Walk over items to collect them
- **Drop Rarity**:
  - Common (60%): Health packs, basic weapons
  - Uncommon (30%): Better weapons, minor power-ups
  - Rare (9%): Major power-ups, coins
  - Legendary (1%): Unique weapons, max health increase

## 🧠 Technical Stack

| Component | Description |
|-----------|-------------|
| Language | Python 3.10+ |
| Game Engine | Pygame |
| Graphics | Pixel-based sprites and backgrounds |
| Audio | WAV/OGG sound effects for hits, attacks, and background music |
| Data | JSON for saving player progress and world state |

## 📁 Project Structure

```
pixel_survivor_worlds/
│
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── QUICKSTART.md                    # Quick reference guide
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
│
├── config/
│   └── settings.json               # Game configuration & difficulty curves
│
├── assets/
│   ├── player/                     # Player sprites (32x32px)
│   │   ├── idle.png
│   │   ├── walk.png
│   │   ├── attack.png
│   │   └── README.md
│   │
│   ├── enemies/                    # Enemy sprites
│   │   ├── basic_enemy.png
│   │   ├── elite_enemy.png
│   │   ├── boss_enemy.png
│   │   ├── ranged_enemy.png
│   │   └── README.md
│   │
│   ├── worlds/                     # World backgrounds (800x600px)
│   │   ├── world1_bg.png
│   │   ├── world2_bg.png
│   │   ├── ... (world3-10)
│   │   └── README.md
│   │
│   ├── weapons/                    # Weapon sprites
│   │   ├── pistol.png
│   │   ├── shotgun.png
│   │   ├── rifle.png
│   │   ├── plasma_gun.png
│   │   └── README.md
│   │
│   ├── drops/                      # Item drop sprites (16x16px)
│   │   ├── health_small.png
│   │   ├── health_medium.png
│   │   ├── health_large.png
│   │   ├── coin.png
│   │   ├── powerup_*.png
│   │   └── README.md
│   │
│   ├── sounds/                     # Sound effects (.wav)
│   │   ├── shoot.wav
│   │   ├── hit.wav
│   │   ├── death.wav
│   │   ├── pickup.wav
│   │   └── README.md
│   │
│   ├── music/                      # Background music (.ogg)
│   │   ├── menu.ogg
│   │   ├── world1-10.ogg
│   │   ├── boss_fight.ogg
│   │   └── README.md
│   │
│   └── fonts/                      # Pixel fonts
│       ├── pixel_font.ttf
│       └── README.md
│
├── scripts/
│   ├── __init__.py                 # Package initializer
│   │
│   ├── ── Core Gameplay (Phase 1-2)
│   ├── player.py                   # Player class
│   ├── bullet.py                   # Bullet/projectile class
│   ├── enemy.py                    # Enemy AI and behavior
│   ├── game.py                     # Main game manager
│   │
│   ├── ── World System (Phase 3)
│   ├── world.py                    # World management
│   ├── round_manager.py            # Round-based spawning
│   │
│   ├── ── Items & Progression (Phase 4)
│   ├── drop.py                     # Item drops
│   ├── inventory.py                # Inventory system
│   ├── weapon.py                   # Weapon definitions
│   ├── powerup.py                  # Powerup effects
│   │
│   ├── ── UI & Menus (Phase 5)
│   ├── ui.py                       # HUD and menus
│   ├── upgrade_shop.py             # Between-round upgrades
│   │
│   ├── ── Polish & Advanced (Phase 6-8)
│   ├── audio_manager.py            # Sound/music manager
│   ├── save_manager.py             # Save/load system
│   ├── particle_system.py          # Visual effects
│   ├── boss.py                     # Boss enemies
│   ├── hazards.py                  # Environmental hazards
│   │
│   └── ── Endgame Content (Phase 9)
│       ├── endless_mode.py         # Infinite survival mode
│       └── leaderboard.py          # Score tracking
│
└── saves/
    ├── player_progress.json        # Auto-generated save file
    └── README.md
```

## 🚀 Game Progression

1. **World Start:**
   - Background, soundtrack, and enemy set are loaded.

2. **Rounds:**
   - Each round spawns enemies in increasing numbers.

3. **Round Complete:**
   - Brief pause + score update.

4. **World Clear:**
   - Player advances to the next world.

5. **World 10:**
   - Endless rounds (no limit) — pure survival.

## 🧱 Future Expansion Ideas

- 💡 Weapon upgrades and skill trees
- 💡 Unlockable characters with unique abilities
- 💡 Boss fights with pattern-based AI
- 💡 Co-op local multiplayer
- 💡 Online leaderboard (high scores by world)
- 💡 Mobile version using Kivy or Godot integration

## 🛣️ Development Roadmap

Follow this roadmap to build Pixel Survivor: Worlds in the correct order, from foundation to polish.

---

### ⚙️ Phase 1 — Basic Player Movement & World 1

**🎯 Goal:** Get a playable prototype with player movement, mouse aiming, and basic shooting in World 1.

**Files to Implement:**

1. **`main.py`**
   - Initialize Pygame
   - Create window (800x600)
   - Set up FPS clock (60 FPS)
   - Create simple game loop
   - Import and instantiate basic Player class
   - Handle WASD input and mouse position
   - Draw everything to screen

2. **`scripts/player.py`**
   - **Class: `Player`**
   - Attributes: `x`, `y`, `speed`, `angle`, `hp`, `max_hp`
   - `update(keys, mouse_pos)` - WASD movement + rotate toward mouse
   - `draw(screen)` - render as colored circle/rectangle
   - Boundary checking (stay within screen)

**What You Should Have:**
- Window opens with a player square/circle
- Player moves smoothly with WASD
- Player rotates to face mouse cursor
- Can close window properly

**✅ Success Criteria:** Player moves in all directions, faces mouse, stays within screen bounds.

---

### 🎮 Phase 2 — Complete Gameplay Loop (Shoot, Kill, Die)

**🎯 Goal:** Add shooting, enemies, health, and a basic game over screen. Make World 1 fully playable.

**Files to Implement:**

3. **`scripts/bullet.py`**
   - **Class: `Bullet`**
   - Attributes: `x`, `y`, `angle`, `speed`, `damage`
   - `update()` - move in direction
   - `is_off_screen()` - remove if outside bounds
   - `draw(screen)` - render as small circle

4. **`scripts/enemy.py`**
   - **Class: `Enemy`**
   - Attributes: `x`, `y`, `hp`, `speed`, `damage`
   - `move_toward_player(player_pos)` - simple chase AI
   - `take_damage(amount)` - reduce HP, die if HP <= 0
   - `attack_player(player)` - deal damage on collision
   - `draw(screen)` - render as colored square

5. **`scripts/game.py`** (Basic version)
   - **Class: `Game`**
   - Attributes: `player`, `bullets` (list), `enemies` (list), `running`, `game_over`
   - `run()` - main game loop
   - `handle_events()` - shoot on left click/spacebar, quit on ESC
   - `update()` - update all objects, check collisions
   - `check_collisions()`:
     - Bullets hit enemies → enemy takes damage
     - Enemies hit player → player takes damage
   - `spawn_enemies(count)` - spawn at random edges
   - `draw()` - render player, bullets, enemies, simple HP bar
   - `game_over_screen()` - display "You Died!" message

**Update `main.py`:**
- Use `Game` class instead of manual game loop

**What You Should Have:**
- Player shoots bullets toward mouse
- Enemies spawn and chase player
- Bullets kill enemies
- Enemies damage player
- Player dies when HP reaches 0
- Game over screen appears

**✅ Success Criteria:** Full combat loop working. You can shoot enemies, take damage, and see game over when you die.

### 🌍 Phase 3 — Rounds, Worlds, and Progression

**🎯 Goal:** Structure the game into rounds and worlds with escalating difficulty.

**Files to Implement:**

6. **`scripts/round_manager.py`**
   - **Class: `RoundManager`**
   - Attributes: `current_round`, `enemies_per_round`, `spawn_timer`, `round_complete`
   - `start_round()` - spawn wave of enemies (increases each round)
   - `is_round_complete()` - check if all enemies are dead
   - `next_round()` - increment round, increase difficulty
   - Display round number on screen

7. **`scripts/world.py`**
   - **Class: `World`**
   - Attributes: `world_number`, `total_rounds`, `background_color`
   - `load_world(num)` - load world data from settings.json
   - `get_difficulty_multiplier()` - scale enemy HP/speed
   - `is_world_complete()` - check if all rounds finished
   - `next_world()` - advance to next world

8. **Update `config/settings.json`**
   - Already created! Contains all 10 worlds with difficulty curves

**Update `scripts/game.py`:**
- Add `round_manager` and `world` objects
- Between rounds: show "Round X Complete!" message
- After world completion: show "World X Complete!" and load next world
- Track score (kills, time survived)

**What You Should Have:**
- Game starts at World 1, Round 1
- Each round spawns more/stronger enemies
- "Round Complete" screen between rounds
- After 10 rounds, advance to World 2
- Difficulty increases noticeably each world

**✅ Success Criteria:** Can complete World 1 (10 rounds) and progress to World 2 with harder enemies.

---

### 🎒 Phase 4 — Drops, Weapons, and Inventory

**🎯 Goal:** Add loot drops, multiple weapons, powerups, and inventory management.

**Files to Implement:**

9. **`scripts/weapon.py`**
   - **Class: `Weapon`**
   - Attributes: `name`, `damage`, `fire_rate`, `bullet_speed`, `spread`
   - Weapon types:
     - Pistol (fast, low damage)
     - Shotgun (spreads 5 bullets, short range)
     - Rifle (slow, high damage)
     - Plasma Gun (medium everything)
   - `can_fire()` - check cooldown timer
   - `shoot(angle)` - return list of Bullet objects

10. **`scripts/drop.py`**
    - **Class: `Drop`**
    - Attributes: `x`, `y`, `drop_type`, `rarity`, `lifetime`
    - Types: HEALTH, WEAPON, POWERUP, COIN
    - `update()` - floating animation, despawn after 30 seconds
    - `draw(screen)` - render as colored square with icon
    - `apply_to_player(player, inventory)` - give item effect

11. **`scripts/powerup.py`**
    - **Class: `Powerup`**
    - Types: SPEED_BOOST, DAMAGE_MULT, SHIELD, INVINCIBILITY
    - `apply(player)` - activate buff
    - `update(dt)` - countdown duration
    - `remove(player)` - deactivate when expired

12. **`scripts/inventory.py`**
    - **Class: `Inventory`**
    - Attributes: `weapons` (max 3), `active_weapon_index`, `powerups`, `coins`
    - `add_weapon(weapon)` - add to empty slot or replace
    - `switch_weapon(index)` - press 1/2/3 to switch
    - `add_powerup(powerup)` - activate and track
    - `update(dt)` - tick powerup timers
    - `get_active_weapon()` - return current weapon

**Update `scripts/enemy.py`:**
- `drop_loot()` - random chance to drop items based on rarity table:
  - Common (60%): Small health
  - Uncommon (30%): Medium health, basic weapons
  - Rare (9%): Powerups, coins
  - Legendary (1%): Best weapons, large health

**Update `scripts/player.py`:**
- Add `inventory` attribute
- Use `inventory.get_active_weapon()` when shooting

**Update `scripts/game.py`:**
- Add `drops` list
- Check player-drop collisions
- Handle number keys (1,2,3) for weapon switching

**What You Should Have:**
- Enemies drop items when killed (health, weapons, powerups, coins)
- Walk over items to pick them up
- Switch between 3 weapons with number keys
- Powerups show duration timer
- Different weapons have different behaviors

**✅ Success Criteria:** Enemy drops spawn, can be collected, weapons can be switched, powerups apply buffs with timers.

---

### 🎨 Phase 5 — UI, HUD, and Menus

**🎯 Goal:** Professional-looking interface with HUD, menus, and upgrade shop.

**Files to Implement:**

13. **`scripts/ui.py`**
    - **Class: `HUD`**
    - `draw_health_bar(screen, player)` - top-left HP bar
    - `draw_weapon_display(screen, inventory)` - bottom-right weapon icons
    - `draw_powerup_timers(screen, powerups)` - active buffs with countdown
    - `draw_round_info(screen, round, world)` - top-center "World X - Round Y"
    - `draw_coin_count(screen, coins)` - top-right coin display
    - `draw_kill_count(screen, kills)` - score tracker

    - **Class: `Menu`**
    - `MainMenu` - Play, Quit buttons
    - `PauseMenu` - Resume, Main Menu buttons (press ESC to pause)
    - `GameOverMenu` - Retry, Main Menu buttons, final score
    - `draw(screen)` - render menu
    - `handle_click(pos)` - detect button clicks

14. **`scripts/upgrade_shop.py`**
    - **Class: `UpgradeShop`**
    - Shows between rounds
    - Upgrades available (using coins):
      - Max HP +20 (50 coins)
      - Move Speed +10% (40 coins)
      - Damage +15% (60 coins)
      - Fire Rate +10% (50 coins)
    - `draw(screen, player, coins)`
    - `handle_purchase(upgrade, player, inventory)`

**Update `scripts/game.py`:**
- Add game states: `MENU`, `PLAYING`, `PAUSED`, `ROUND_COMPLETE`, `GAME_OVER`, `SHOP`
- Show HUD during `PLAYING`
- Show appropriate menu for each state
- ESC key toggles pause
- After round complete, show upgrade shop before next round

**What You Should Have:**
- Main menu on game start
- In-game HUD showing HP, weapons, round, coins, powerups
- Pause menu (ESC)
- Upgrade shop between rounds
- Game over screen with score
- Professional-looking UI

**✅ Success Criteria:** All menus work, HUD displays correctly, upgrade shop allows purchases between rounds.

---

### 🎵 Phase 6 — Audio, Sprites, and Polish

**🎯 Goal:** Replace placeholder graphics with pixel art, add sound effects and music.

**Files to Implement:**

15. **`scripts/audio_manager.py`**
    - **Class: `AudioManager`**
    - `load_sounds()` - load all SFX and music files
    - `play_sfx(name)` - shoot, hit, death, pickup, powerup
    - `play_music(track)` - world-specific background music
    - `stop_music()`
    - `set_volume(sfx_vol, music_vol)`

**Assets to Create/Find:**
- **Player sprites** (32x32px): Use tools like Aseprite, Piskel, or find on opengameart.org
  - idle.png, walk.png (animated), attack.png
- **Enemy sprites**: basic_enemy.png, elite_enemy.png
- **World backgrounds** (800x600px): Simple colored/textured backgrounds for each world
- **Weapon sprites**: pistol.png, shotgun.png, rifle.png, plasma_gun.png
- **Drop icons** (16x16px): health, coin, powerup icons
- **Sound effects** (.wav): shoot, hit, death, pickup, powerup
- **Music** (.ogg): menu, world1-10 background tracks

**Update All Classes:**
- **`player.py`**: Load and draw sprite instead of rectangle, add walking animation
- **`enemy.py`**: Load enemy sprites, death animation
- **`bullet.py`**: Small sprite or particle effect
- **`drop.py`**: Load drop icons
- **`game.py`**: Draw world background, call audio_manager for sounds
- Play sounds on: shooting, enemy death, taking damage, item pickup

**What You Should Have:**
- Pixel art player character with animations
- Enemy sprites
- Background image for each world
- Sound effects for all actions
- Background music that changes per world
- Game looks and sounds professional

**✅ Success Criteria:** Game has full pixel art graphics, smooth animations, SFX on all actions, and world-specific music.

---

### 💾 Phase 7 — Save/Load and Persistence

**🎯 Goal:** Save player progress so they can continue later.

**Files to Implement:**

16. **`scripts/save_manager.py`**
    - **Class: `SaveManager`**
    - `save_game(data)` - write to `saves/player_progress.json`
    - `load_game()` - read save file, return data dict
    - `has_save()` - check if save exists
    - `delete_save()` - wipe save for new game
    - Data saved:
      - Current world number
      - Current round
      - Player HP, upgrades purchased
      - Inventory weapons
      - Total coins collected
      - Total kills, time played

**Update `scripts/game.py`:**
- Auto-save after each round completion
- On game start, check if save exists
- Add "Continue" button to main menu if save found
- Add "New Game" option (deletes save)

**What You Should Have:**
- Game saves progress after each round
- Can quit and resume from exact position
- "Continue" button on main menu
- Can start fresh with "New Game"

**✅ Success Criteria:** Can quit mid-world, restart, and continue from last completed round with all progress intact.

---

### 🔥 Phase 8 — Advanced Content (Particles, Bosses, Hazards)

**🎯 Goal:** Add visual effects, boss battles, and environmental hazards.

**Files to Implement:**

17. **`scripts/particle_system.py`**
    - **Class: `Particle`**
    - Small colored squares that fade out
    - Spawn on: bullet impact, enemy death, item pickup
    - Add screen shake effect on player damage

18. **`scripts/boss.py`**
    - **Class: `Boss`** (extends `Enemy`)
    - Appears every 10 rounds in World 7+
    - 5x more HP than normal enemy
    - Attack patterns:
      - Circular bullet spray (shoots 8 bullets in circle)
      - Charge attack (speeds toward player)
      - Summon 3 minions
    - Boss health bar at top of screen

19. **`scripts/hazards.py`**
    - **Class: `Hazard`**
    - Appears in World 5+
    - Types:
      - Fire zones (damage over time)
      - Spike traps (high damage on contact)
      - Poison clouds (slow + damage)
    - Spawn randomly in arena

**Update `scripts/round_manager.py`:**
- Spawn boss every 10th round in World 7+
- Spawn hazards in World 5+

**What You Should Have:**
- Particle effects on all impacts
- Screen shake when hit
- Boss fights with special patterns
- Environmental hazards that add challenge
- Game feels polished and exciting

**✅ Success Criteria:** Particles appear, bosses are challenging with unique patterns, hazards spawn and affect gameplay.

---

### 🏆 Phase 9 — Endless Mode and Leaderboard

**🎯 Goal:** Endgame content and score tracking for replayability.

**Files to Implement:**

20. **`scripts/endless_mode.py`**
    - **Class: `EndlessMode`**
    - Unlocked after completing World 10
    - Infinite rounds with exponentially scaling difficulty
    - Track highest round survived
    - No round breaks (continuous spawning)

21. **`scripts/leaderboard.py`**
    - **Class: `Leaderboard`**
    - Save to `saves/high_scores.json`
    - Store top 10 scores with:
      - Player name
      - Mode (World X or Endless)
      - Highest round reached
      - Total kills
      - Time survived
    - Display on main menu

**Update `scripts/ui.py`:**
- Add "Endless Mode" button after World 10 complete
- Show leaderboard on main menu
- Enter name prompt for new high scores

**What You Should Have:**
- Endless mode unlocked after beating game
- Leaderboard tracking top 10 scores
- Ability to enter name for high scores
- Replay value with endless difficulty scaling

**✅ Success Criteria:** Endless mode works, difficulty scales infinitely, leaderboard tracks and displays top scores.

---

### 🧪 Phase 10 — Testing, Balance, and Final Polish

**🎯 Goal:** Make the game stable, fun, and ready to share.

**No New Files - Just Improvements:**

**Balance & Tuning:**
- Playtest all 10 worlds thoroughly
- Adjust enemy HP/damage in `settings.json` for smooth difficulty curve
- Fine-tune drop rates (should feel rewarding but not overpowered)
- Balance weapon stats (each should feel useful)
- Adjust powerup durations for fun gameplay

**Bug Fixes:**
- Fix any collision detection issues
- Ensure no memory leaks (test long play sessions)
- Fix edge cases (player stuck, enemies piling up, etc.)

**Polish:**
- Add screen shake intensity slider
- Improve enemy AI (spread out, don't stack)
- Add tutorial/controls screen on first launch
- Add settings menu (volume, fullscreen toggle)
- Optimize performance (30+ enemies should run smoothly)
- Add death particles and animations
- Polish menu transitions

**Testing Checklist:**
- [ ] All 10 worlds completable
- [ ] Save/load works correctly
- [ ] All weapons function properly
- [ ] Powerups apply and expire correctly
- [ ] Bosses spawn and behave correctly
- [ ] Hazards work as intended
- [ ] Audio plays without crackling
- [ ] Game doesn't crash after 1+ hour
- [ ] Leaderboard saves/loads correctly
- [ ] No exploits or game-breaking bugs

**✅ Success Criteria:** Game is polished, balanced, bug-free, and fun to play from start to endless mode!

---

### 🚀 Complete File Implementation Order

| Phase | Files to Implement | What You Get |
|-------|-------------------|--------------|
| **1** | `main.py`, `player.py` | Player movement + mouse aiming |
| **2** | `bullet.py`, `enemy.py`, `game.py` | Complete combat loop |
| **3** | `round_manager.py`, `world.py` | 10 worlds with rounds |
| **4** | `weapon.py`, `drop.py`, `powerup.py`, `inventory.py` | Loot drops + inventory |
| **5** | `ui.py`, `upgrade_shop.py` | HUD, menus, upgrades |
| **6** | `audio_manager.py` + assets | Sounds, music, pixel art |
| **7** | `save_manager.py` | Save/load progress |
| **8** | `particle_system.py`, `boss.py`, `hazards.py` | Polish + advanced content |
| **9** | `endless_mode.py`, `leaderboard.py` | Endgame content |
| **10** | Testing & balance | Final polish |

**Development Pro Tips:**

- ✅ **Test after each phase** - Don't move forward with bugs
- ✅ **Start simple** - Use colored shapes before adding sprites
- ✅ **Use `config/settings.json`** - All balance values in one place
- ✅ **Comment your code** - Future you will thank you
- ✅ **Save frequently** - Use git commits after each working phase
- ✅ **Playtest often** - Make sure it's fun, not just functional
- ✅ **Pygame sprite groups** - Use for efficient collision detection
- ✅ **Consistent art style** - Stick to 16x16 or 32x32 pixel grid
- ✅ **Math helpers** - Use `math.atan2()` for player rotation
- ✅ **Delta time** - For smooth movement independent of FPS

---

## 🧩 Installation

```bash
git clone https://github.com/yourusername/pixel-survivor-worlds
cd pixel-survivor-worlds
pip install pygame
python main.py
```

## 🧙 Developer Notes

- Keep pixel art resolution consistent (e.g., 16x16 or 32x32 base grid)
- Use Pygame's sprite groups for performance and clean logic
- Separate logic into reusable classes (Player, Enemy, World, RoundManager)
- Store game difficulty and round count in a config file for easy tuning

## 📜 License

MIT License — Free to use, modify, and share.
