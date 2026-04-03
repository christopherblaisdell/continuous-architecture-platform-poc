# RPCSX

## The RPCS3 Team's PS4 (and PS5) Project

RPCSX is an experimental PlayStation 4 and PlayStation 5 emulator for Linux, created by DH (one of the original founders of RPCS3, the leading PS3 emulator) along with RPCS3's current main developers Nekotekina and kd-11. Despite its impressive pedigree, RPCSX is in very early stages and cannot play any commercial games yet.

## Key Facts

| Detail | Value |
|--------|-------|
| Latest release | v20231111 (November 2023) |
| GitHub stars | 1,900+ |
| Contributors | 66 |
| License | GPLv2 (kernel: MIT) |
| Language | C++ (93%), C (4%), GLSL (2%) |
| Platforms | Linux only |
| Source code | [github.com/RPCSX/rpcsx](https://github.com/RPCSX/rpcsx) |
| Discord | [discord.gg/t6dzA4wUdG](https://discord.gg/t6dzA4wUdG) |

## Compatibility

| Metric | Value |
|--------|-------|
| Playable titles | 0 (0%) |
| Total tested | 76 |

RPCSX currently has **zero playable titles**. It can boot some commercial games (We Are Doomed, Sonic Mania have shown progress), but none reach a playable state.

There are reports on the RPCSX Discord that the PS4's VSH (Visual Shell / system menu) boots and reaches the Sony Interactive Entertainment logo with sound, but crashes due to race conditions and internal GPU issues.

## Architecture

RPCSX takes a different approach from shadPS4:

- Uses modified source code from RPCS3
- Also incorporates code from a private project called "RPCS4" that DH had been working on
- Aims to emulate both PS4 and PS5
- Linux-exclusive by design

## Why It Matters

Despite having zero playable games, RPCSX is worth watching because:

1. **Team pedigree** -- The RPCS3 team took years to reach playable status too, and RPCS3 is now one of the best emulators ever made
2. **PS5 ambitions** -- RPCSX aims to cover both PS4 and PS5, which no other project attempts seriously
3. **Deep systems knowledge** -- The team's experience with PlayStation architecture is unmatched
4. **66 contributors** -- Strong developer interest despite early status

## Should You Use RPCSX?

**No, not for playing games.** RPCSX is a developer/research project at this stage. It's only relevant if you:

- Want to contribute to PS4/PS5 emulation development
- Are a Linux developer interested in console emulation internals
- Want to follow the long-term trajectory of PS5 emulation

For actually playing PS4 games on Linux, use [shadPS4](shadps4.md).
