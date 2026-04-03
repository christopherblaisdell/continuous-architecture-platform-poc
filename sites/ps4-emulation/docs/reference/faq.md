# Frequently Asked Questions

## General Questions

### Is PS4 emulation legal?

**The emulator itself is legal.** shadPS4 and other PS4 emulators are clean-room implementations of the PS4 operating environment. They do not contain any Sony proprietary code.

**Firmware modules exist in a gray area.** Some PS4 system modules are needed for compatibility. These are copyrighted by Sony. Dumping them from your own console is generally considered fair use in many jurisdictions, but distributing them is not.

**Games must be legally obtained.** You need to own the games you play. Dumping games from your own PS4 discs or downloading games you've purchased digitally (via tools on a jailbroken PS4) is the expected path.

!!! warning "Downloading games you don't own is piracy"
    shadPS4 and other emulator projects do not condone piracy. The developers cannot and will not help with obtaining game files illegally.

---

### Do I need a PS4 to use shadPS4?

**Technically, no** -- shadPS4 can run many games without firmware modules. However, having access to a PS4 (especially a jailbroken one) helps for:

- Dumping firmware modules (improves compatibility for some games)
- Dumping game disc images
- Dumping trophy/NP keys
- Extracting game updates

Without a PS4, you're limited to games that work without extra firmware and games you can legally obtain through other means.

---

### What's the difference between shadPS4 and PCSX4/PCSX5?

**PCSX4 and PCSX5 are scams.** They are not real emulators. They are malware-laden hoax executables that have circulated on YouTube and social media for years, exploiting the naming convention of legitimate emulators (PCSX2 for PS2, etc.).

**shadPS4 is the only legitimate, working PS4 emulator.** It is:

- Open source (GPL-2.0 license)
- Hosted on GitHub with full source code
- Developed by a transparent community with over 187 contributors
- Capable of actually running PS4 games

If something claims to be a PS4 emulator and isn't shadPS4 (or one of the other open-source projects listed in this guide), it's almost certainly fake.

---

### Can I play PS4 games online through shadPS4?

**No.** Online functionality requires connecting to PlayStation Network servers, which is not possible through an emulator. All gameplay is offline/single-player (or local multiplayer where supported).

---

### Can I use my PS4 save data?

**Not directly.** PS4 save data is encrypted with per-console keys. There is no current method to import PS4 save files into shadPS4. You'll need to start fresh.

---

## Performance Questions

### Why does the game stutter at the beginning?

This is **shader compilation** -- completely normal. shadPS4 must translate PS4 GPU shaders to Vulkan the first time they're encountered. Once compiled, shaders are cached and the stutter goes away.

Expect 10-30 minutes of occasional stutters when first starting a new game. See the [Performance Optimization](../guides/performance-optimization.md) guide for details.

---

### Why is the game running at half speed?

Common causes:

1. **GPU is too weak** -- Lower the internal resolution
2. **V-Sync forcing 30 FPS** -- Some games target 30 FPS; this is by design
3. **CPU bottleneck** -- Less common; check CPU usage in task manager
4. **Missing firmware modules** -- Some games run poorly without proper LLE modules

---

### What FPS should I expect?

It depends entirely on the game and your hardware:

| Game Type | Typical FPS (Mid-Range PC) | Typical FPS (Steam Deck) |
|-----------|---------------------------|--------------------------|
| 2D / Indie | 60 FPS | 60 FPS |
| Simple 3D | 60 FPS | 30-60 FPS |
| AA 3D | 30-60 FPS | 20-30 FPS |
| AAA 3D | 30 FPS (if playable) | 15-30 FPS |

Check the [Playable Games](../compatibility/playable-games.md) list for per-title expectations.

---

## Compatibility Questions

### Why does my game show as "Nothing" on the compatibility list?

"Nothing" means the game doesn't boot at all. This is usually because:

- The game uses PS4 OS features not yet implemented
- The game requires specific firmware modules
- The game's specific anti-tamper or DRM prevents it from running

There's nothing you can do except wait for shadPS4 to add support. Check back after major version updates.

---

### Why does a game work on Windows but not Linux (or vice versa)?

Compatibility can differ between platforms due to:

- **GPU driver differences** -- Nvidia's proprietary Linux driver vs. Windows driver may handle edge cases differently
- **Vulkan implementation differences** -- RADV (AMD Linux) vs. amdvlk vs. Windows AMD driver
- **Filesystem case sensitivity** -- Linux is case-sensitive, which can cause issues with games that reference files inconsistently

If a game works on one platform but not the other, report it on the shadPS4 GitHub issues page.

---

### Will [specific game] work on shadPS4?

Check the [compatibility list](https://github.com/shadps4-emu/shadps4-game-compatibility/issues) on GitHub. Each game has its own issue thread with user reports across different hardware and shadPS4 versions.

If your game isn't listed, it hasn't been tested. You can test it yourself and submit a compatibility report.

---

## Setup Questions

### Where do I put game files?

Place decrypted PS4 game folders anywhere on your storage. Each game should be in its own folder containing an `eboot.bin` file and the game's file structure. Point shadPS4 to the folder (or directly to `eboot.bin`).

---

### What file format should games be in?

shadPS4 expects **decrypted, extracted game folders** -- not `.pkg` files or disc images. The game directory should contain:

```
CUSAXXXXX/
├── eboot.bin          (main executable)
├── sce_sys/
│   ├── param.sfo     (game metadata)
│   └── ...
└── ...                (game data files)
```

If you have a `.pkg` file, it needs to be installed/extracted first (typically done on a jailbroken PS4 or with pkg extraction tools).

---

### Do I need to decrypt games?

**Yes.** PS4 games are encrypted. shadPS4 cannot run encrypted game files. Games must be decrypted before use. This is typically done:

- On a jailbroken PS4 using homebrew dumping tools
- Via extraction tools that handle decryption

---

### How do I update shadPS4?

1. Download the latest release from the [shadPS4 GitHub releases page](https://github.com/shadps4-emu/shadPS4/releases)
2. Extract and replace the old executable
3. Your shader cache and settings are preserved (usually)
4. On Steam Deck via EmuDeck, use EmuDeck's built-in update mechanism

!!! tip "Check release notes"
    Major updates may change settings formats or invalidate shader caches. Read the release notes before updating.

---

## Steam Deck Questions

### Should I use EmuDeck or manual setup?

**EmuDeck is recommended** for most users. It:

- Handles shadPS4 installation and updates
- Creates correct Steam shortcuts for Gaming Mode
- Configures controller layouts and per-game settings
- Manages paths and folder structure

Manual setup gives more control but requires Linux command-line knowledge. See the [Steam Deck Setup Guide](../guides/steam-deck-setup.md) for both methods.

---

### Can I run PS4 games from a microSD card on Steam Deck?

**Yes**, but with caveats:

- Use an **A2-rated** microSD card for best performance
- Load times will be longer than internal SSD
- Game performance itself is not significantly affected
- Some games with heavy asset streaming may stutter more

---

### Does PS4 emulation drain the Steam Deck battery fast?

**Yes.** PS4 emulation is one of the most demanding tasks you can run on a Steam Deck. Expect:

- **1-2 hours** for 3D games at full TDP
- **2-3 hours** for 2D/indie games at lower TDP
- Using a 30 FPS cap and TDP limit extends battery life significantly
