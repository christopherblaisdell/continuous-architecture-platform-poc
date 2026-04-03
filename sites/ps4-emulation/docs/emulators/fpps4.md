# fpPS4

## The Second-Place Contender

fpPS4 is a PlayStation 4 compatibility layer written in Free Pascal. It was the second PS4 emulator to gain traction and currently offers the second-best game compatibility after shadPS4, though the gap is significant.

!!! warning "Development Paused"
    The developer (`red-prig`) is currently rewriting the emulator core in a separate `kern` branch. Until this rewrite is complete, there will be no support for specific games. The main branch has not seen commits in approximately 2 years.

## Key Facts

| Detail | Value |
|--------|-------|
| Latest release | v0.0.1 (December 2022) |
| GitHub stars | 2,100+ |
| Contributors | 11 |
| License | LGPLv2.1 |
| Language | Free Pascal (67%), C++ (33%) |
| Platforms | Windows only |
| Source code | [github.com/red-prig/fpPS4](https://github.com/red-prig/fpPS4) |
| Discord | [discord.gg/up9qatpX7M](https://discord.gg/up9qatpX7M) |

## Compatibility

| Metric | Value |
|--------|-------|
| Playable titles | 111 (5.38%) |
| Total tested | 2,062 |
| Compatibility tracker | [GitHub Issues](https://github.com/red-prig/fpps4-game-compatibility/issues) |

While fpPS4 has been tested against more titles than shadPS4 (2,062 vs 1,758), its playable percentage is much lower (5.4% vs 15-17%).

## System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Windows 7 SP1 x64 or higher |
| CPU | x64 with AVX2 support |
| GPU | Vulkan API support |

## Controls

fpPS4 supports XInput-compatible gamepads natively. Buttons can be remapped by pressing Escape during emulation. The DualShock 4 touchpad is emulated by the mouse.

| PS4 Button | Keyboard Key |
|------------|-------------|
| Left Stick | W/A/S/D |
| Right Stick | I/J/K/L |
| Triangle | Numpad 8 |
| Square | Numpad 4 |
| Cross | Numpad 2 |
| Circle | Numpad 6 |
| L1 / R1 | Q / E |
| L2 / R2 | 1 / 4 |
| L3 / R3 | Z / C |
| OPTIONS | Enter |
| D-Pad | Arrow Keys |

Press Alt+Enter for borderless fullscreen.

## Building from Source

fpPS4 requires:

- **Free Pascal compiler** 3.3.1 (trunk via fpcupdeluxe), x86_64 only
- **Lazarus** 2.0.0 or higher, x86_64 only

## Strengths

- Helped pioneer PS4 emulation research
- Unique approach using Free Pascal
- The `red-prig` developer contributed the trophy key export tool used by shadPS4
- LGPL license allows broader code reuse

## Weaknesses

- Windows-only (no Linux, no macOS, no Steam Deck)
- Development effectively stalled for ~2 years during kernel rewrite
- Very small contributor base (11 people)
- No official GUI (third-party launchers exist)
- Far fewer playable titles than shadPS4
- No trophy support, no DLC support

## Should You Use fpPS4?

**For most users: No.** shadPS4 is better in every practical metric. fpPS4 is primarily of interest to:

- Developers studying alternative emulation approaches
- Researchers interested in the Free Pascal implementation
- Users who want to test niche titles not yet tested on shadPS4

The kernel rewrite may eventually bring fpPS4 back to active development, but there's no timeline for completion.
