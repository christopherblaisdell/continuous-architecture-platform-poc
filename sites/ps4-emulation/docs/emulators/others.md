# Other PS4 Emulation Projects

## Beyond the Big Three

Several other PS4 emulation projects exist at various stages of development. None are recommended for end users, but they contribute to the broader understanding of PS4 system architecture.

## psOff

| Detail | Value |
|--------|-------|
| Platforms | Windows |
| Playable titles | 4 out of 545 tested (0.7%) |
| License | Proprietary (was GPLv3 before December 2024) |
| Status | Active but closed-source |

psOff is a compatibility layer that was previously open-source under GPLv3. In December 2024, the developer made it closed-source, which significantly reduced community trust and contribution potential.

The developer is focused primarily on the rendering pipeline, with plans to make it "almost perfect." It currently lacks support for multiple command buffer submits, for-loops in shaders, and various opcodes.

**Verdict:** The move to closed-source, combined with only 4 playable titles, makes this hard to recommend over shadPS4.

---

## Obliteration

| Detail | Value |
|--------|-------|
| Platforms | Windows, Linux, macOS |
| Playable titles | 0 |
| License | Dual licensed (Apache 2.0 or MIT) |
| Status | Active |
| Source | [github.com/obhq/obliteration](https://github.com/obhq/obliteration) |

Obliteration started as a hard-fork from Kyty but was rewritten from scratch, using Kyty and Uplift as references. It takes a different approach from shadPS4 by requiring PS4 firmware files (similar to Spine).

Despite promising architectural work, Obliteration cannot boot any commercial games yet. It's primarily of interest to emulator developers studying alternative PS4 emulation approaches.

---

## ChonkyStation4

| Detail | Value |
|--------|-------|
| Platforms | Windows |
| Playable titles | 10 out of 164 tested (6.1%) |
| License | GPLv3 |
| Status | Active |

A newer entry in the PS4 emulation space. While it has a slightly higher compatibility percentage than fpPS4, the total number of tested and playable titles is very small.

---

## Orbital

| Detail | Value |
|--------|-------|
| Platforms | Windows, Linux |
| Playable titles | 0 |
| License | MIT |
| Status | Inactive |
| Source | [github.com/AlexAltea/orbital](https://github.com/AlexAltea/orbital) |

Orbital took a fundamentally different approach as a **low-level emulator** based on QEMU. Instead of reimplementing PS4 libraries at a high level, it attempted to emulate the entire PS4 hardware stack, including the kernel.

Created by Alexandro Sanchez (AlexAltea), who is also involved with RPCS3 and Nucleus. Despite impressive technical work, Orbital got stuck at the PS4's Safe Mode and development appears to have halted.

---

## Spine (Abandoned)

| Detail | Value |
|--------|-------|
| Platforms | Linux only |
| Playable titles | 4 out of 1,001 tested (0.4%) |
| License | Proprietary (closed-source) |
| Status | Abandoned (last update May 2022) |

Spine was a Linux-exclusive emulator whose creator kept the source code closed to prevent a Windows-only fork from emerging. Its authenticity was verified by Orbital developer AlexAltea.

Spine showed early promise but was abandoned before reaching a useful level of compatibility. It's now only of historical interest.

---

## Kyty (Abandoned)

| Detail | Value |
|--------|-------|
| Platforms | Windows |
| Playable titles | 2 (Blackhole, Worms W.M.D.) |
| License | MIT |
| Status | Inactive |
| Source | [github.com/InoriRus/Kyty](https://github.com/InoriRus/Kyty) |

Notable as the first PS4 emulator with a GUI. Created by InoriRus, it aimed at both PS4 and PS5 compatibility. Development has effectively stopped, and Obliteration was forked from it.

---

## GPCS4 (Abandoned)

| Detail | Value |
|--------|-------|
| Platforms | Windows |
| Playable titles | 2 (We Are Doomed, Sonic Mania) |
| License | GPLv3 |
| Status | Inactive |

GPCS4 was historically significant as one of the first projects to run commercial PS4 games (showing Nier: Automata logos and running simple titles in early 2020). Development has halted -- it appears to have been primarily a research project for 3D graphics.

---

## Summary

| Project | Playable | Platform | Active | Worth Watching? |
|---------|----------|----------|--------|-----------------|
| psOff | 4 | Windows | Yes | Maybe (closed-source is concerning) |
| ChonkyStation4 | 10 | Windows | Yes | Yes (growing) |
| Obliteration | 0 | Cross-platform | Yes | Yes (good architecture) |
| Orbital | 0 | Win/Linux | No | No |
| Spine | 4 | Linux | No | No |
| Kyty | 2 | Windows | No | No |
| GPCS4 | 2 | Windows | No | No |

!!! tip "For Playing Games"
    None of these projects are suitable for playing games. Use [shadPS4](shadps4.md) instead.
