# shadPS4

## The Leading PS4 Emulator

shadPS4 is an early PlayStation 4 emulator for Windows, Linux, and macOS, written in C++. It is the first emulator to get major PS4 titles like Bloodborne running in-game, and it offers the best game compatibility of any PS4 emulator by a wide margin.

The project is led by **George Moralis** (`georgemoralis`), one of the co-founders of PCSX2 (the legendary PS2 emulator), giving it strong pedigree in the emulation community.

## Key Facts

| Detail | Value |
|--------|-------|
| Latest release | v0.15.0 (March 16, 2026) |
| Total releases | 21 |
| GitHub stars | 30,600+ |
| Contributors | 187 |
| License | GPLv2 |
| Language | C++ (C++23) |
| Graphics API | Vulkan 1.3 |
| Platforms | Windows 10+, Ubuntu 22.04+, macOS 15.4+ |
| Website | [shadps4.net](https://shadps4.net/) |
| Source code | [github.com/shadps4-emu/shadPS4](https://github.com/shadps4-emu/shadPS4) |
| Discord | [discord.gg/bFJxfftGW6](https://discord.gg/bFJxfftGW6) |

## Architecture

shadPS4 is a **compatibility layer** (HLE/LLE hybrid), not a low-level hardware emulator. Because the PS4 uses x86-64 (the same architecture as desktop PCs), shadPS4 can execute game code natively rather than translating instructions. The main challenges are:

- **GPU emulation** -- The PS4's AMD GCN GPU must be translated to Vulkan. shadPS4's shader compiler is inspired by yuzu's Hades compiler.
- **OS emulation** -- The PS4 runs a modified FreeBSD kernel. shadPS4 reimplements system calls and libraries needed by games.
- **Library emulation** -- PS4 system libraries are either reimplemented in C++ (HLE) or loaded directly from dumped firmware (LLE).

### HLE vs LLE Modules

shadPS4 supports loading some PS4 firmware modules directly (LLE mode) for features not yet reimplemented:

| LLE Module | Purpose |
|------------|---------|
| libSceCesCs.sprx | Character encoding |
| libSceFont.sprx | Font rendering |
| libSceFontFt.sprx | FreeType font rendering |
| libSceFreeTypeOt.sprx | OpenType font support |
| libSceJpegDec.sprx | JPEG decoding |
| libSceJpegEnc.sprx | JPEG encoding |
| libSceJson.sprx | JSON parsing |
| libSceJson2.sprx | JSON parsing v2 |
| libSceLibcInternal.sprx | C standard library internals |
| libSceNgs2.sprx | Next-gen audio system |
| libScePngEnc.sprx | PNG encoding |
| libSceRtc.sprx | Real-time clock |
| libSceUlt.sprx | Ultra lightweight threads |
| libSceAudiodec.sprx | Audio decoding |

These must be dumped from a jailbroken PS4. See the [Firmware Dumping Guide](../guides/firmware-dumping.md).

## Features

### What Works

- Running commercial PS4 games (129 playable, 196 in-game on Linux)
- Vulkan-based GPU rendering
- Xbox and DualShock controller support (plug and play)
- Keyboard and mouse input with customizable bindings
- Per-game input profiles
- Trophy support with custom icons and sound notifications
- Fullscreen mode
- FPS counter and video debug info
- Internal resolution scaling (via patches)
- Built-in cheat manager
- Built-in patch manager
- Motion controls emulation
- Audio output (improved SDL3 backend in v0.15.0)
- DLC installation and loading
- Game updates installation

### What Doesn't Work (Yet)

- Most AAA titles (only ~17% of tested games are playable)
- PS4 Pro enhanced features (partial/limited)
- PlayStation VR
- Online multiplayer / PSN connectivity
- PlayStation Camera / Move controllers (WIP)
- Save states
- Fast forward / rewind

## v0.15.0 Release Highlights (March 2026)

The latest release brought significant improvements:

**Core:**

- Implemented guest signal handlers
- Implemented kqueue and kevent kernel events
- Improved filesystem stability (fixed crashes from vector pointer returns)
- Thread TLS initialization on creation
- System fonts mounting

**GPU & Shaders:**

- Support for 32-thread sharing mode
- IMAGE_ATOMIC_CMPSWAP implementation
- Relaxed and precise readback modes
- Force subgroup size to 64 when possible

**Libraries:**

- Improved audio output with SDL3 backend
- npWebApi library implementation
- Improved motion controls emulation
- Network library improvements
- SysModule HLE implementation

## GUI Options

shadPS4 itself is a command-line application. For a graphical interface, use the **QtLauncher**:

- Download from [shadps4-emu/shadps4-qtlauncher releases](https://github.com/shadps4-emu/shadps4-qtlauncher/releases)
- Displays game library with cover art and background music
- Per-game settings configuration
- One-click game launching

!!! tip "Steam Deck Users"
    EmuDeck handles the GUI setup automatically. See the [Steam Deck Setup Guide](../guides/steam-deck-setup.md).

## Compatibility Statistics

shadPS4 uses a 5-tier compatibility rating system:

| Rating | Windows | Linux | macOS |
|--------|---------|-------|-------|
| Playable | 109 (15.1%) | 129 (16.9%) | 11 (4.1%) |
| Ingame | 184 (25.4%) | 196 (25.7%) | 45 (16.6%) |
| Menus | 125 (17.3%) | 101 (13.2%) | 35 (12.9%) |
| Boots | 121 (16.7%) | 153 (20.1%) | 45 (16.6%) |
| Nothing | 185 (25.6%) | 184 (24.1%) | 135 (49.8%) |
| **Total Tested** | **724** | **763** | **271** |

!!! note "Linux Leads"
    Linux consistently has the best compatibility numbers. This is likely due to better Vulkan driver support on Linux and the fact that many testers use Linux-based systems (including Steam Deck).

## Main Development Team

| Developer | GitHub |
|-----------|--------|
| georgemoralis | [github.com/georgemoralis](https://github.com/georgemoralis) |
| psucien | [github.com/psucien](https://github.com/psucien) |
| viniciuslrangel | [github.com/viniciuslrangel](https://github.com/viniciuslrangel) |
| roamic | [github.com/roamic](https://github.com/roamic) |
| squidbus | [github.com/squidbus](https://github.com/squidbus) |
| frodo (baggins183) | [github.com/baggins183](https://github.com/baggins183) |
| Stephen Miller | [github.com/StevenMiller123](https://github.com/StevenMiller123) |
| kalaposfos13 | [github.com/kalaposfos13](https://github.com/kalaposfos13) |

## Support the Project

shadPS4 accepts donations via [Ko-fi](https://ko-fi.com/shadps4).
