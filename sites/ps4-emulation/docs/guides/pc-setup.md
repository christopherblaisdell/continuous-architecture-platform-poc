# PC Setup Guide (Windows & Linux)

## Installing shadPS4 on Your Computer

This guide walks you through setting up shadPS4 on a Windows or Linux desktop PC. For Steam Deck, see the [Steam Deck Setup Guide](steam-deck-setup.md).

## Prerequisites

Before installing, make sure your system meets the [minimum requirements](../reference/system-requirements.md).

### Windows Requirements

- Windows 10 or later (64-bit)
- **Microsoft Visual C++ 2022 Redistributable** -- [Download here](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- Up-to-date GPU drivers:
    - Nvidia: [nvidia.com/drivers](https://www.nvidia.com/en-us/drivers)
    - AMD: [amd.com/support/download](https://www.amd.com/en/support/download/drivers.html)
    - Intel: [intel.com/download-center](https://www.intel.com/content/www/us/en/download-center/home.html)

### Linux Requirements

- Ubuntu 22.04 or equivalent (64-bit)
- Vulkan 1.3 capable GPU drivers
- For AMD GPUs: Mesa 23.0+ with RADV driver recommended
- For Nvidia GPUs: Proprietary driver 535+ recommended

!!! warning "Update ALL GPU Drivers"
    Update drivers for **all** graphics devices in your system, including integrated graphics. Outdated drivers on unused GPUs can interfere with shadPS4's Vulkan usage.

## Step 1: Download shadPS4

### Option A: QtLauncher (Recommended for Most Users)

The QtLauncher provides a graphical interface for managing and launching games.

1. Go to [shadps4.net/downloads](https://shadps4.net/downloads)
2. Download **shadPS4 Qt Launcher** for your OS
3. Extract the archive to a location of your choice

### Option B: CLI Release (Advanced Users)

The core emulator without a GUI, for command-line usage.

1. Go to [shadps4.net/downloads](https://shadps4.net/downloads)
2. Download **shadPS4** release for your OS
3. Extract the archive

!!! warning "Avoid Privileged Directories"
    Do not extract shadPS4 to `Program Files`, `System32`, or any directory requiring admin privileges. This can cause emulation issues or prevent shadPS4 from running.

## Step 2: First Launch

=== "Windows (QtLauncher)"
    1. Install [Visual C++ 2022](https://aka.ms/vs/17/release/vc_redist.x64.exe) if not already installed
    2. Open the extracted folder
    3. Run `shadPS4QtLauncher.exe`
    4. Follow the initial setup wizard to set your game and addon directories

=== "Linux (QtLauncher)"
    1. Open the extracted folder
    2. Make the AppImage executable: `chmod +x shadPS4QtLauncher-qt.AppImage`
    3. Run `./shadPS4QtLauncher-qt.AppImage`
    4. Follow the initial setup wizard

=== "Linux (CLI)"
    ```bash
    chmod +x shadPS4
    ./shadPS4 --help    # View all available options
    ./shadPS4 CUSA00900  # Launch a game by its CUSA ID
    ```

## Step 3: Install Firmware Modules

Some games require PS4 firmware modules for proper functionality. See the [Firmware Dumping Guide](firmware-dumping.md) for instructions on obtaining these files.

Once you have the firmware files, place them in shadPS4's `sys_modules` folder:

- **QtLauncher**: Right-click any game > Open Folder > Open Log Folder > Go up one directory > `sys_modules/`
- **CLI**: The `sys_modules/` folder is in the same directory as the shadPS4 binary

## Step 4: Install Games

!!! warning "Legal Requirement"
    You must dump games from your own legally purchased PS4 console. See the [Firmware Dumping Guide](firmware-dumping.md) for information about dumping.

### Dumping Games from Your PS4

1. You need a **jailbroken PS4** (firmware 9.00 or lower is most common for jailbreaking)
2. Install a game dumping tool like **Itemzflow** on your PS4
3. Dump your games -- they will be in a folder named `CUSAxxxxx` (e.g., `CUSA00900` for Bloodborne)
4. Transfer the game folders to your PC

### Installing Dumped Games

=== "QtLauncher"
    1. In the QtLauncher, go to **File > Install Packages (PKG)**
    2. Select your `.pkg` file or game folder
    3. The game will appear in your library

=== "CLI"
    1. Copy the game's `CUSAxxxxx` folder to your designated game directory
    2. Launch with: `./shadPS4 CUSA00900`

### Installing Updates

1. Dump the update from your PS4 (folder named `CUSAxxxxx-patch` or `CUSAxxxxx-UPDATE`)
2. Copy it to the same game installation directory
3. The QtLauncher will show the updated version

### Installing DLC

1. Navigate to your set additional content directory
2. Create a folder with the same name as your game (e.g., `CUSA00900`)
3. Copy your dumped DLC folders into it

## Step 5: Configure and Play

### Global Settings

The QtLauncher provides a settings UI. Key options:

| Setting | Recommended Value |
|---------|------------------|
| Graphics Backend | Vulkan (only option) |
| Fullscreen | Personal preference (F11 to toggle) |
| Internal Resolution | Native (increase only if performance allows) |
| Enable Motion Controls | On (if using DualShock 4 / DualSense) |

### Per-Game Settings

Right-click a game in the QtLauncher to access per-game settings. This is useful for:

- Adjusting resolution per game
- Enabling/disabling specific patches
- Setting game-specific control mappings

### CLI Usage Patterns

```bash
# Launch a game by CUSA ID (searches game install folders)
shadPS4 CUSA00900

# Launch with fullscreen
shadPS4 --fullscreen true CUSA00900

# Launch a specific ELF directly
shadPS4 /path/to/game/eboot.bin

# Pass arguments to the game
shadPS4 CUSA00900 -- -flag1 -flag2
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Vulkan not found" | Update GPU drivers to latest version |
| Immediate crash on launch | Install Visual C++ 2022 (Windows) or check Vulkan support |
| Black screen after loading | Try adding firmware modules to `sys_modules/` |
| Low performance | See [Performance Optimization](performance-optimization.md) |
| Controller not detected | Xbox/DualShock controllers should work automatically; check USB connection |
| Game not appearing in library | Verify folder name follows `CUSAxxxxx` format |

## Next Steps

- [Dump firmware modules](firmware-dumping.md) for better compatibility
- [Optimize performance](performance-optimization.md) for smoother gameplay
- Check the [Playable Games](../compatibility/playable-games.md) list to see what works well
