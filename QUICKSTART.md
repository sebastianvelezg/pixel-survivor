# 🚀 Quick Start Guide - Pixel Survivor: Worlds

## 📦 Setup

1. **Install Python 3.10+**

   Make sure you have Python 3.10 or higher installed.
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Game**
   ```bash
   python main.py
   ```

---

## 🛣️ Development Roadmap (Condensed)

### ⚙️ Phase 1 — Player Movement & Aiming (START HERE!)

**Goal:** Get a player moving and facing the mouse

**Files:**
- [ ] `main.py` — Game window, loop, FPS clock
- [ ] `scripts/player.py` — WASD movement, mouse rotation

**Test:** Player moves with WASD and rotates toward mouse ✅

---

### 🎮 Phase 2 — Complete Combat Loop

**Goal:** Shooting, enemies, health, game over

**Files:**
- [ ] `scripts/bullet.py` — Projectiles
- [ ] `scripts/enemy.py` — Chase AI, collision damage
- [ ] `scripts/game.py` — Game manager, collision detection

**Test:** Can shoot enemies, take damage, and die ✅

---

### 🌍 Phase 3 — Rounds & Worlds

**Goal:** 10 worlds with progressive rounds

**Files:**
- [ ] `scripts/round_manager.py` — Wave spawning
- [ ] `scripts/world.py` — World progression, difficulty scaling

**Test:** Complete World 1 (10 rounds), advance to World 2 ✅

---

### 🎒 Phase 4 — Loot & Inventory

**Goal:** Drops, weapons, powerups, inventory

**Files:**
- [ ] `scripts/weapon.py` — Pistol, shotgun, rifle, plasma gun
- [ ] `scripts/drop.py` — Health, weapons, powerups, coins
- [ ] `scripts/powerup.py` — Speed, damage, shield, invincibility
- [ ] `scripts/inventory.py` — 3 weapon slots, switching (1/2/3)

**Test:** Enemies drop items, can pick up and switch weapons ✅

---

### 🎨 Phase 5 — UI & Menus

**Goal:** Professional HUD and menus

**Files:**
- [ ] `scripts/ui.py` — HUD (HP, weapons, round), menus
- [ ] `scripts/upgrade_shop.py` — Between-round upgrades

**Test:** All menus work, HUD shows info, can buy upgrades ✅

---

### 🎵 Phase 6 — Audio & Sprites

**Goal:** Pixel art and sound

**Files:**
- [ ] `scripts/audio_manager.py` — SFX and music
- [ ] Create/find assets (sprites, sounds, music)

**Test:** Game has graphics, animations, sound effects, music ✅

---

### 💾 Phase 7 — Save/Load

**Goal:** Persistent progress

**Files:**
- [ ] `scripts/save_manager.py` — Save/load to JSON

**Test:** Can quit and continue from last round ✅

---

### 🔥 Phase 8 — Polish & Advanced

**Goal:** Particles, bosses, hazards

**Files:**
- [ ] `scripts/particle_system.py` — Visual effects
- [ ] `scripts/boss.py` — Boss enemies (World 7+)
- [ ] `scripts/hazards.py` — Environmental dangers (World 5+)

**Test:** Particles, bosses, and hazards work ✅

---

### 🏆 Phase 9 — Endgame Content

**Goal:** Endless mode and leaderboard

**Files:**
- [ ] `scripts/endless_mode.py` — Infinite survival
- [ ] `scripts/leaderboard.py` — Score tracking

**Test:** Endless mode works, leaderboard saves scores ✅

---

### 🧪 Phase 10 — Testing & Balance

**Goal:** Polish and balance

- [ ] Playtest all 10 worlds
- [ ] Balance difficulty curves
- [ ] Fix bugs
- [ ] Optimize performance

**Test:** Game is polished, balanced, and fun! ✅

---

## 🎨 Asset Creation Resources

### Pixel Art Tools
- **Aseprite** (paid, best for animations) - aseprite.org
- **Piskel** (free, web-based) - piskelapp.com
- **GIMP** (free) - gimp.org
- **LibreSprite** (free, Aseprite fork) - libresprite.github.io

### Free Asset Sources
- **OpenGameArt.org** - Massive library of free game assets
- **itch.io** - Search for "pixel art" + "CC0" or "free"
- **Kenney.nl** - High-quality free assets

### Sound & Music
- **Sounds:** freesound.org, opengameart.org
- **Music:** incompetech.com, opengameart.org, freemusicarchive.org
- **Editor:** Audacity (free) for editing audio

### Quick Tips
- ✅ Start with **colored rectangles/circles** — add sprites later
- ✅ Use **32x32px** for player/enemies, **16x16px** for items
- ✅ Keep art style **consistent** (same palette, resolution)
- ✅ Use **.wav** for short SFX, **.ogg** for music (smaller files)

---

## ✅ Phase Completion Checklist

### Phase 1
- [ ] Window opens at 800x600
- [ ] Player renders (rectangle is fine)
- [ ] WASD moves player in all directions
- [ ] Player stays within screen bounds
- [ ] Player rotates to face mouse cursor

### Phase 2
- [ ] Left click/spacebar shoots bullets
- [ ] Bullets travel in aimed direction
- [ ] Enemies spawn at screen edges
- [ ] Enemies chase player
- [ ] Bullets kill enemies on collision
- [ ] Enemies damage player on collision
- [ ] HP bar shows player health
- [ ] Game over screen when HP = 0

### Phase 3
- [ ] Game starts at World 1, Round 1
- [ ] Rounds spawn progressively more enemies
- [ ] "Round Complete" message between rounds
- [ ] After 10 rounds, World 2 unlocks
- [ ] Enemies get harder each world
- [ ] Score/kills are tracked

### Phase 4
- [ ] Enemies drop items on death (health, weapons, coins)
- [ ] Walk over items to auto-pickup
- [ ] 3 weapon slots in inventory
- [ ] Press 1/2/3 to switch weapons
- [ ] Powerups apply buffs with visible timers
- [ ] Different weapons behave differently

### Phase 5
- [ ] HUD shows HP, weapon, round, world, coins
- [ ] Main menu with Play button
- [ ] Pause menu (ESC key)
- [ ] Game over menu with Retry button
- [ ] Upgrade shop between rounds
- [ ] Can purchase upgrades with coins

### Phase 6
- [ ] Player sprite loaded and animated
- [ ] Enemy sprites loaded
- [ ] World background images loaded
- [ ] Sound effects play (shoot, hit, death, pickup)
- [ ] Background music plays per world
- [ ] Animations smooth and polished

### Phase 7
- [ ] Progress saves after each round
- [ ] "Continue" button on main menu
- [ ] Can resume from saved world/round
- [ ] "New Game" option deletes save

### Phase 8
- [ ] Particles spawn on bullet impacts
- [ ] Particles spawn on enemy deaths
- [ ] Screen shakes on player damage
- [ ] Bosses spawn every 10th round (World 7+)
- [ ] Hazards spawn and damage player (World 5+)

### Phase 9
- [ ] Endless mode unlocks after World 10
- [ ] Endless mode difficulty scales infinitely
- [ ] Leaderboard tracks top 10 scores
- [ ] Can enter name for high scores

### Phase 10
- [ ] All 10 worlds completable
- [ ] No game-breaking bugs
- [ ] Difficulty curve feels smooth
- [ ] Drop rates feel rewarding
- [ ] Performance good with 30+ enemies
- [ ] Game is fun and polished!

---

## 🆘 Troubleshooting

**Window won't open?**
- Check Pygame is installed: `pip show pygame`
- Make sure Python 3.10+: `python --version`

**Player won't move?**
- Check `pygame.key.get_pressed()` is working
- Verify `player.update()` is called in game loop

**Collisions not working?**
- Use Pygame's `rect.colliderect()` for simple collision
- Or check distance: `math.hypot(dx, dy) < radius`

**Game running too fast/slow?**
- Use delta time: `dt = clock.tick(60) / 1000.0`
- Multiply movement by `dt` for FPS-independent movement

**Sprites not loading?**
- Check file paths are correct (absolute or relative)
- Use `os.path.join()` for cross-platform paths
- Print error messages: `except Exception as e: print(e)`

---

## 📚 Need More Help?

- **Full Details:** See [README.md](README.md) for complete implementation guide
- **Pygame Docs:** pygame.org/docs
- **Python Docs:** docs.python.org

---

## 🎮 Development Tips

1. **Test early, test often** — Don't build everything before testing
2. **Use print statements** — Debug with `print(player.x, player.y)`
3. **Start simple** — Colored shapes first, sprites later
4. **Comment your code** — Future you will thank present you
5. **Git commits** — Commit after each working phase
6. **Have fun!** — This is a game project, enjoy the process!
