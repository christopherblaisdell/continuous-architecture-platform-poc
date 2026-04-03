# System Requirements

## PC Requirements

### Minimum Requirements

These are the bare minimum specs to run simple PS4 games. Expect low settings and 30 FPS or below for most titles.

| Component | Minimum |
|-----------|---------|
| **CPU** | x86-64-v3 compatible, 4 cores / 6 threads, 2.5 GHz+ |
| **GPU** | Vulkan 1.3 capable, 2 GB VRAM |
| **RAM** | 8 GB |
| **OS** | Windows 10 64-bit / Linux (kernel 5.15+) |
| **Storage** | SSD recommended, 50+ GB free per game |

### Recommended Requirements

For playable performance at 1080p/30+ FPS in most compatible titles:

| Component | Recommended |
|-----------|-------------|
| **CPU** | AMD Ryzen 5 3600 / Intel Core i5-10400 or better |
| **GPU** | Nvidia GTX 1660 Super / AMD RX 5600 XT or better, 4+ GB VRAM |
| **RAM** | 16 GB |
| **OS** | Windows 11 64-bit / Linux (latest stable kernel) |
| **Storage** | NVMe SSD, 100+ GB free |

### High-End (1080p/60 FPS Target)

For uncapped or 60 FPS gameplay in demanding titles:

| Component | High-End |
|-----------|----------|
| **CPU** | AMD Ryzen 7 5800X / Intel Core i7-12700 or better |
| **GPU** | Nvidia RTX 3070 / AMD RX 6800 or better, 8+ GB VRAM |
| **RAM** | 32 GB |
| **Storage** | NVMe SSD |

## CPU Requirements Explained

### What Is x86-64-v3?

shadPS4 requires a CPU that supports the **x86-64-v3** microarchitecture level. This includes the AVX2 instruction set, which is critical for performance.

**CPUs that support x86-64-v3:**

| Vendor | First Supporting Architecture | Year |
|--------|------------------------------|------|
| Intel | Haswell (4th gen) | 2013 |
| AMD | Excavator / Zen 1 | 2015 / 2017 |

If your CPU is from 2015 or later, it almost certainly supports x86-64-v3.

!!! tip "Check your CPU support"
    **Windows:** Open CMD and run `wmic cpu get caption`

    **Linux:** Run `cat /proc/cpuinfo | grep avx2`

    If AVX2 appears in the output, your CPU supports x86-64-v3.

### Why Core Count Is Less Important

PS4 emulation on shadPS4 is not heavily multi-threaded in the same way as, for example, rpcs3 (PS3 emulator). The PS4's Jaguar cores were weak, so shadPS4's x86-64 host execution is already far stronger clock-for-clock. The main bottleneck is GPU translation, not CPU thread count.

A fast 6-core CPU will generally outperform a slower 12-core CPU.

## GPU Requirements Explained

### Why Vulkan 1.3 Is Required

The PS4 uses a custom AMD GCN GPU. shadPS4 translates PS4 GPU commands to Vulkan API calls. Vulkan 1.3 is required because it provides:

- Dynamic rendering (reduces overhead)
- Synchronization improvements
- Extended dynamic state

**Check Vulkan support:**

- **Windows:** Download and run `vulkaninfo` from the Vulkan SDK
- **Linux:** Run `vulkaninfo | grep "apiVersion"`
- **Steam Deck:** Vulkan 1.3 is supported natively

### GPU Compatibility Notes

| GPU | Status |
|-----|--------|
| Nvidia GTX 900+ series | Supported (driver 525+) |
| Nvidia RTX series | Supported (best compatibility) |
| AMD RX 400+ series | Supported (Mesa RADV recommended on Linux) |
| Intel Arc A-series | Partially supported (driver maturity improving) |
| Intel UHD / Iris | Insufficient for 3D titles |
| Apple Silicon (MoltenVK) | Not supported -- macOS builds experimental |

## Steam Deck

### Steam Deck Specs

| Component | Steam Deck LCD | Steam Deck OLED |
|-----------|---------------|-----------------|
| **CPU** | Zen 2, 4 cores / 8 threads, up to 3.5 GHz | Zen 2, 4 cores / 8 threads, up to 3.5 GHz |
| **GPU** | RDNA 2, 8 CUs, up to 1.6 GHz | RDNA 2, 8 CUs, up to 1.6 GHz |
| **RAM** | 16 GB LPDDR5 (shared) | 16 GB LPDDR5 (shared) |
| **Display** | 1280x800, 60 Hz | 1280x800, 90 Hz |
| **Storage** | 64/256/512 GB | 512 GB / 1 TB |
| **Vulkan** | 1.3 supported | 1.3 supported |

### Steam Deck Assessment

The Steam Deck meets the **minimum** requirements for PS4 emulation:

- **CPU:** x86-64-v3 compatible (Zen 2 with AVX2) -- PASS
- **GPU:** Vulkan 1.3, RDNA 2 with 8 CUs -- PASS (but limited)
- **RAM:** 16 GB shared between CPU and GPU -- PASS
- **Resolution:** 1280x800 (lower than PS4's 1080p) -- ADVANTAGE (less GPU work)

!!! info "Realistic Expectations"
    The Steam Deck can run many PS4 indie and 2D games at full speed. For AA and AAA 3D games, expect 30 FPS with occasional dips. Some demanding titles may not be playable. The lower native resolution (800p vs 1080p) actually helps, as the GPU has fewer pixels to render.

### Steam Deck Storage Recommendations

PS4 games are large:

| Game Type | Typical Size |
|-----------|-------------|
| Indie | 2-10 GB |
| AA | 15-30 GB |
| AAA | 30-80 GB |

- **Internal SSD** is fastest -- use for games you play regularly
- **microSD A2** cards work well for less demanding titles
- **microSD A1** cards may cause noticeably longer load times

## Operating System Notes

### Windows

- Windows 10 version 1903+ required
- Windows 11 recommended for latest Vulkan driver support
- Ensure Visual C++ Redistributable 2022 is installed

### Linux

- Any distribution with kernel 5.15 or newer
- Mesa 23.0+ recommended for AMD GPUs (includes RADV Vulkan driver)
- Flatpak or AppImage versions available (simplify dependency management)
- Steam Deck runs Arch-based SteamOS 3.x and is fully supported

### macOS

macOS support in shadPS4 is experimental. The MoltenVK translation layer (Vulkan-over-Metal) introduces an additional translation step and significant overhead. Not recommended for serious use.
