# Emulator Comparison Overview

## PS4 Emulator Landscape (April 2026)

There are several PS4 emulation projects, but only one is genuinely usable for playing games today. This page compares them all so you can make an informed choice.

## Comparison Table

| Feature | shadPS4 | fpPS4 | RPCSX | psOff | Others |
|---------|---------|-------|-------|-------|--------|
| **Status** | Active, recommended | Active (rewrite in progress) | Active (early) | Closed-source | Inactive/early |
| **Latest Version** | v0.15.0 (Mar 2026) | Nightly | Git only | 2025Nov10 | Varies |
| **Platforms** | Windows, Linux, macOS | Windows only | Linux only | Windows | Varies |
| **Language** | C++ | Free Pascal | C++ | C++ | Varies |
| **License** | GPLv2 | LGPLv2.1 | GPLv2 | Proprietary | Varies |
| **GitHub Stars** | 30,600+ | 2,100+ | 1,900+ | N/A | <500 |
| **Contributors** | 187 | 11 | 66 | Unknown | <15 |
| **Playable Games** | 109-129 (15-17%) | 111 (5.4%) | 0 (0%) | 4 (0.7%) | 0-10 |
| **Tested Games** | 724-763 | 2,062 | 76 | 545 | <200 |
| **PS4 Pro Support** | Partial | No | No | No | No |
| **GUI** | QtLauncher (separate) | Third-party | No | No | Varies |
| **Steam Deck** | Yes (via EmuDeck) | No | Theoretically | No | No |
| **Firmware Required** | Some modules (optional) | Unknown | Yes | Unknown | Varies |
| **Trophy Support** | Yes | No | No | No | No |

## The Verdict

### Use shadPS4

There is no real competition right now. shadPS4 is:

- **The most compatible** -- 3x more playable games than the next best option
- **The most actively developed** -- weekly commits, 187 contributors, frequent releases
- **Cross-platform** -- runs on Windows, Linux, macOS, and Steam Deck
- **Well-documented** -- official wiki, quickstart guide, active Discord community
- **Integrated with EmuDeck** -- first-class Steam Deck support

### Why Not the Others?

| Emulator | Why Not (Yet) |
|----------|---------------|
| **fpPS4** | Windows-only, kernel rewrite stalled development for ~2 years, far fewer playable titles |
| **RPCSX** | 0 playable titles, Linux-only, very early stage despite talented team (RPCS3 developers) |
| **psOff** | Went closed-source in December 2024, only 4 playable titles, limited trust |
| **Obliteration** | Cannot boot any commercial games yet |
| **Orbital** | Stuck at PS4 Safe Mode, appears dormant |
| **Spine** | Abandoned (last update May 2022), was Linux-only and closed-source |

## Emulator History Timeline

| Date | Milestone |
|------|-----------|
| 2020 | GPCS4 runs first commercial games (We Are Doomed, Sonic Mania) |
| 2021 | Spine shows promise on Linux but remains closed-source |
| 2022 | fpPS4 emerges, runs small games; Kyty shows first GUI |
| 2023 | shadPS4 development accelerates; RPCSX announced by RPCS3 devs |
| 2024 Aug | shadPS4 gets Bloodborne in-game -- major milestone |
| 2024 Dec | psOff goes closed-source |
| 2025 | shadPS4 reaches 100+ playable titles, EmuDeck integration |
| 2026 Mar | shadPS4 v0.15.0 released with major compatibility improvements |

## Detailed Pages

- [shadPS4](shadps4.md) -- full deep dive on the recommended emulator
- [fpPS4](fpps4.md) -- the second-place option
- [RPCSX](rpcsx.md) -- the promising Linux-only project
- [Other Projects](others.md) -- brief coverage of the rest
