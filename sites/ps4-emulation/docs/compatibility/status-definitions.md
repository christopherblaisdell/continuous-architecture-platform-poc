# Status Definitions

## shadPS4 Compatibility Rating Scale

shadPS4 uses a five-tier rating system to classify game compatibility. Understanding these tiers helps set expectations before you try a game.

## The Five Tiers

### Playable

The game can be played from start to finish or for extended sessions with acceptable performance and stability.

**What to expect:**

- Core gameplay is functional
- The game is completable (or for open-ended games, can be played extensively)
- Performance is generally at or near the PS4's original framerate
- Minor graphical glitches or missing effects may still exist
- Occasional crashes are possible but rare

**This does NOT mean:**

- The game is perfect or identical to the PS4 original
- There are zero bugs or visual differences
- Performance is always 100% stable

---

### Ingame

The game gets past the title screen and menus into actual gameplay, but has issues that prevent a comfortable play experience.

**What to expect:**

- You can control your character and interact with the game world
- Significant graphical glitches, missing effects, or rendering errors
- Performance may be too low for enjoyable play (e.g., 10-20 FPS)
- Crashes may occur frequently
- Progression-blocking bugs may exist in later areas

**Typical reasons a game is Ingame but not Playable:**

- Major graphical corruption making the game hard to see
- Framerate too low for action-oriented gameplay
- Crashes that prevent reaching certain story checkpoints
- Audio completely missing or severely broken

---

### Menus

The game boots, displays its title screen, and allows navigation through menus, but crashes, freezes, or shows a black screen when attempting to start actual gameplay.

**What to expect:**

- Title screen renders (possibly with graphical issues)
- Menu navigation works
- Starting a new game or loading a save fails

---

### Boots

The game begins to load but does not reach functional menus. You may see a loading screen, a splash screen, or a brief flash of content before it crashes or hangs.

**What to expect:**

- The game executable launches
- Some initial content may display (developer logos, loading indicators)
- The game crashes, freezes, or shows a blank screen before reaching menus

---

### Nothing

The game does not start at all. It crashes immediately, shows an error, or produces no output.

**What to expect:**

- Immediate crash on launch
- Error messages about missing functions or unsupported features
- The emulator may display log output but the game produces nothing visible

---

## How Ratings Are Determined

- Ratings are submitted by community testers via the [compatibility database](https://github.com/shadps4-compatibility/shadps4-game-compatibility)
- Each report includes the shadPS4 version, operating system, and hardware used
- Ratings reflect the **best reported status** for each game on each platform
- A game may perform differently on different hardware or OS versions

## Distribution (April 2026)

=== "Linux"
    | Status | Count | Percentage |
    |--------|-------|------------|
    | Playable | 129 | 16.9% |
    | Ingame | 196 | 25.7% |
    | Menus | 101 | 13.2% |
    | Boots | 153 | 20.1% |
    | Nothing | 184 | 24.1% |
    | **Total** | **763** | **100%** |

=== "Windows"
    | Status | Count | Percentage |
    |--------|-------|------------|
    | Playable | 109 | 15.1% |
    | Ingame | 184 | 25.4% |
    | Menus | 125 | 17.3% |
    | Boots | 121 | 16.7% |
    | Nothing | 185 | 25.6% |
    | **Total** | **724** | **100%** |

=== "macOS"
    | Status | Count | Percentage |
    |--------|-------|------------|
    | Playable | 11 | 4.1% |
    | Ingame | 45 | 16.6% |
    | Menus | 35 | 12.9% |
    | Boots | 45 | 16.6% |
    | Nothing | 135 | 49.8% |
    | **Total** | **271** | **100%** |

!!! note "Linux Has the Best Compatibility"
    Linux consistently outperforms Windows in compatibility testing. This is partly due to better Vulkan driver implementations on Linux and the active Steam Deck testing community.

## Putting It in Perspective

About **43% of tested games on Linux** are either Playable or Ingame, meaning nearly half of all tested PS4 titles show meaningful gameplay. This is a remarkable achievement for an emulator that the developers themselves describe as "early in development."

For context, RPCS3 (PS3 emulator) took approximately 5-6 years to reach similar compatibility levels. shadPS4 has achieved this in roughly 3 years of serious development.
