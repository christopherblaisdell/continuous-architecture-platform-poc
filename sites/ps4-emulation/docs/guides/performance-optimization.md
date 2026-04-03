# Performance Optimization

## Getting the Best Performance from shadPS4

PS4 emulation is demanding. Even with shadPS4's native x86-64 execution, GPU emulation through Vulkan requires significant processing power. This guide covers settings and techniques to maximize performance on both PC and Steam Deck.

## Understanding the Bottlenecks

### Why PS4 Emulation Is Demanding

Unlike retro emulation where the host CPU simulates a weaker CPU, PS4 emulation's main bottleneck is **GPU translation**. The PS4 uses AMD GCN (Graphics Core Next) shaders that must be translated to Vulkan in real-time. This means:

- **GPU matters most** -- A strong Vulkan-capable GPU is the primary performance factor
- **Shader compilation** causes stutters the first time new shaders are encountered
- **VRAM** is important -- some games use much of the PS4's shared 8GB GDDR5
- **Single-thread CPU performance** matters for OS/kernel emulation, not core count

### The Shader Cache

The first time you encounter a new visual effect in a game, shadPS4 must compile its shader from GCN to SPIR-V (Vulkan's shader format). This causes a brief stutter. Once compiled, the shader is cached and subsequent encounters are smooth.

**What this means in practice:**

- First 10-30 minutes of a game may have frequent stutters
- Replaying the same areas will be smoother
- The shader cache persists between sessions
- Major shadPS4 updates may invalidate the cache, restarting the process

## PC Optimization

### GPU Driver Settings

=== "Nvidia"
    1. Open **Nvidia Control Panel**
    2. Manage 3D Settings > Add shadPS4 as a program
    3. Set:
        - Power management mode: **Prefer maximum performance**
        - Texture filtering quality: **High performance**
        - Vulkan/OpenGL present method: **Prefer native**
    4. Ensure you're on the **latest Game Ready driver**

=== "AMD"
    1. Open **AMD Software: Adrenalin Edition**
    2. Gaming > Add shadPS4
    3. Set:
        - Anti-Lag: **Disabled** (can cause issues with emulators)
        - Radeon Boost: **Disabled**
        - Image Sharpening: Optional (can improve upscaled output)
    4. On Linux, use **RADV** (Mesa Vulkan driver) rather than AMDVLK

=== "Intel"
    1. Update to the latest Intel GPU driver
    2. Intel Arc GPUs work with Vulkan but expect lower compatibility
    3. Integrated Intel GPUs (UHD/Iris) generally lack the performance for 3D PS4 games

### shadPS4 Settings

| Setting | Impact | Recommendation |
|---------|--------|---------------|
| Internal Resolution | Very High | Start at native (1920x1080), lower if needed |
| Fullscreen | Low | Enable for marginally better performance |
| V-Sync | Medium | Disable for higher FPS, enable to prevent tearing |
| Readback Mode | Medium | Try "Relaxed" mode (added in v0.15.0) for better performance |

### Per-Game Patches

shadPS4 supports game-specific patches that can:

- Unlock framerate (remove 30 FPS caps)
- Change internal rendering resolution
- Fix specific game bugs

Access patches through the QtLauncher's per-game settings. The community maintains patch databases for popular titles.

### Linux-Specific Optimizations

```bash
# Use gamemode for CPU governor optimization (install gamemode first)
gamemoderun ./shadPS4 CUSA00900

# Set Vulkan ICD loader to RADV explicitly (AMD GPUs)
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json ./shadPS4 CUSA00900

# Enable shader disk cache for AMD
RADV_PERFTEST=gpl ./shadPS4 CUSA00900

# Increase file descriptor limits (helps with games that open many files)
ulimit -n 65536
```

## Steam Deck Optimization

### Quick Access Menu Settings

Press the **...** button during gameplay:

| Setting | Indie Games | AA Games | AAA Games |
|---------|-------------|----------|-----------|
| FPS Limit | 60 | 30 | 30 |
| Refresh Rate | 60 Hz | 40 Hz | 30 Hz |
| TDP Limit | 8-10W | 12-14W | 15W |
| GPU Clock | 800 MHz | 1200 MHz | 1600 MHz |
| Half Rate Shading | Off | Off | Try On |
| Scaling Filter | Off | FSR | FSR |

### Using 40 Hz Mode

For games that can't maintain 60 FPS but feel choppy at 30:

1. Set **Refresh Rate** to 40 Hz
2. Set **FPS Limit** to 40 FPS
3. This provides a noticeably smoother experience than 30 FPS while being much less demanding than 60

### MangoHud for Performance Monitoring

MangoHud is pre-installed on Steam Deck and shows real-time performance metrics:

1. In Quick Access Menu, enable the Performance Overlay
2. Set to Level 2 or higher for detailed stats
3. Monitor **GPU usage**, **CPU usage**, **VRAM**, and **frametime**

Key things to watch:

- **GPU at 99%**: Game is GPU-bottlenecked (lower resolution or GPU settings)
- **CPU at 99%**: Game is CPU-bottlenecked (lower TDP won't help, but frame limiting does)
- **Frametime spikes**: Likely shader compilation stutters (will improve over time)

## General Tips

### Do This First

1. **Update GPU drivers** to the absolute latest version
2. **Install firmware modules** -- many games run faster with proper LLE modules
3. **Let shader caches build** -- play through the first area of a game even if it stutters
4. **Close background apps** -- especially on Steam Deck, close any overlay apps or browsers

### Memory Considerations

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| System RAM | 8 GB | 16 GB |
| VRAM | 2 GB | 4+ GB |
| Page file / Swap | 8 GB | 16 GB |

On systems with 8 GB RAM, ensure you have adequate swap space. Some games will exceed 8 GB of combined system + VRAM usage and will crash without swap.

### Storage Speed

While storage speed doesn't affect runtime performance much, it significantly impacts:

- **Game loading times** -- SSD is much faster than HDD
- **Shader cache loading** -- First launch after boot is faster on SSD
- **Save/load operations** -- Instant on SSD, noticeable delay on HDD

For Steam Deck, keep games on the fastest storage available. Internal SSD > A2-rated microSD > A1-rated microSD.

## Troubleshooting Performance Issues

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Constant low FPS | Insufficient GPU | Lower resolution, enable FSR |
| Stutters that improve over time | Shader compilation | Normal -- play through it |
| Stutters that never improve | Driver issue or missing modules | Update drivers, install firmware modules |
| Sudden FPS drops in specific areas | Complex scene overwhelming GPU | Lower settings, wait for shadPS4 updates |
| Crash after 30-60 minutes | Memory leak or RAM exhaustion | Close background apps, increase swap |
| Black screen with audio | GPU driver incompatibility | Try a different driver version |
