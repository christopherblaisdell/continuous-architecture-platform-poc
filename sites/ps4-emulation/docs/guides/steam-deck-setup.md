# Steam Deck Setup Guide

## Running PS4 Games on Steam Deck

The Steam Deck is one of the best devices for PS4 emulation outside of a desktop PC. Its AMD APU with RDNA 2 graphics and native Linux OS make it a natural fit for shadPS4. This guide covers two installation methods: EmuDeck (recommended) and manual installation.

## Method 1: EmuDeck (Recommended)

EmuDeck is a collection of scripts that automatically configures emulators on Steam Deck, including shadPS4. This is the easiest path.

### Step 1: Install EmuDeck

1. Switch to **Desktop Mode** (hold the Power button > Switch to Desktop)
2. Open a web browser and go to [emudeck.com](https://www.emudeck.com/)
3. Download and run the EmuDeck installer
4. Follow the setup wizard -- when prompted for emulators, make sure **shadPS4** is selected
5. EmuDeck will download and configure shadPS4 as an AppImage

### Step 2: Install Games

1. In Desktop Mode, launch shadPS4 from the Applications menu (or from `Emulation/tools/launchers/shadps4.sh`)
2. In shadPS4, click **File > Install Packages (PKG)**
3. Navigate to your PKG files (on SD card or internal storage) and install them

Games are installed to: `Emulation/storage/shadps4/games/`

### Step 3: Add Games to Steam

EmuDeck uses **Steam ROM Manager** to add emulated games to your Steam library with artwork.

1. In Desktop Mode, open Steam ROM Manager (from EmuDeck)
2. Enable the **Sony PlayStation 4 - ShadPS4 (Shortcut)** parser
3. For each installed game in shadPS4:
    - Right-click the game in shadPS4 > **Create Shortcut > Create Desktop Shortcut**
    - Move the `.desktop` file from your Desktop to `Emulation/roms/ps4/shortcuts/`
4. In Steam ROM Manager, click **Preview** then **Save to Steam**
5. Your PS4 games now appear in your Steam library in Game Mode

!!! tip "Remove Special Characters"
    If a desktop shortcut filename contains special symbols (like `(r)` or `(c)`), rename the file to remove them. For example, rename `God Of War(r) Collection.desktop` to `God Of War Collection.desktop`.

### Step 4: Play in Game Mode

Switch back to Game Mode. Your PS4 games should appear in your library under the PlayStation 4 collection. Launch them just like any other game.

### EmuDeck Folder Locations

| Content | Path |
|---------|------|
| shadPS4 binary | `/home/deck/Applications/shadps4-qt.AppImage` |
| Game storage | `Emulation/storage/shadps4/games/` |
| DLC | `Emulation/storage/shadps4/dlc/` |
| Saves | `Emulation/saves/shadps4/saves/` |
| Config | `~/.config/shadps4/` |
| Data | `~/.local/share/shadps4/` |
| Launcher script | `Emulation/tools/launchers/shadps4.sh` |

### Updating shadPS4 via EmuDeck

1. Open the EmuDeck application
2. Go to **Manage Emulators**
3. Find shadPS4 in the list
4. Click **Update**

Alternatively, run `Emulation/tools/binupdate/binupdate.sh`.

---

## Method 2: Manual Installation

If you prefer not to use EmuDeck, you can install shadPS4 manually.

### Step 1: Download shadPS4

1. Switch to Desktop Mode
2. Download the Linux AppImage from [shadps4.net/downloads](https://shadps4.net/downloads)
3. Extract to a convenient location (e.g., `/home/deck/Applications/`)
4. Make it executable:
    ```bash
    chmod +x shadPS4QtLauncher-qt.AppImage
    ```

### Step 2: Create Game Directories

```bash
mkdir -p ~/PS4Games
mkdir -p ~/PS4DLC
```

### Step 3: Install and Configure

1. Launch the AppImage from the file manager or terminal
2. Set your game directory and addon directory in settings
3. Install games via File > Install Packages (PKG)

### Step 4: Add to Steam as Non-Steam Game

1. In Steam (Desktop Mode), click **Games > Add a Non-Steam Game**
2. Browse to the shadPS4 AppImage or create individual launch scripts per game
3. Set controller configuration in Steam's controller settings

---

## Steam Deck Performance Tips

### Control Performance with Steam's Built-in Tools

Press the **...** (Quick Access) button during gameplay to access:

| Setting | Recommended | Purpose |
|---------|-------------|---------|
| Framerate Limit | 30 FPS | Stabilizes framerate, saves battery |
| TDP Limit | 10-15W | Balance between performance and battery |
| GPU Clock | 800-1600 MHz | Lower for simple games, higher for demanding |
| Scaling Filter | FSR | Upscale from lower resolution for better FPS |

### Per-Game Recommendations

| Game Type | FPS Limit | TDP | GPU Clock |
|-----------|-----------|-----|-----------|
| Indie / 2D | 60 FPS | 8-10W | 800 MHz |
| 3D Indie (Hollow Knight, etc.) | 60 FPS | 10-12W | 1000 MHz |
| AA Titles (Yakuza, etc.) | 30 FPS | 12-15W | 1200 MHz |
| AAA Titles (Bloodborne, etc.) | 30 FPS | 15W | 1600 MHz |

### Battery Life Expectations

| Game Category | Expected Battery Life |
|--------------|----------------------|
| Simple indie games | 2.5-3.5 hours |
| Mid-tier 3D games | 1.5-2.5 hours |
| AAA titles | 1-1.5 hours |

### Storage Recommendations

PS4 games are large. A single AAA title can be 40-100 GB.

- **Use a high-speed microSD card** (A2 rated) for game storage
- The Steam Deck's internal SSD is faster but limited in size
- Move games between internal and SD card storage as needed
- Keep the shadPS4 application itself on internal storage for faster loading

---

## Using ES-DE as an Alternative Frontend

If you prefer EmulationStation DE over Steam ROM Manager:

1. EmuDeck installs ES-DE automatically
2. Set the **Alternative Emulator** for PlayStation 4 in ES-DE:
    - On any PS4 game, press Select > Edit This Game's Metadata > Alternative Emulator
    - Choose `shadps4 Shortcut [Standalone]`

See the [EmuDeck documentation](https://emudeck.github.io/emulators/steamos/shadps4/) for more details.

---

## Troubleshooting on Steam Deck

| Problem | Solution |
|---------|----------|
| Game not showing in Game Mode | Re-run Steam ROM Manager and regenerate entries |
| Black screen on launch | Ensure firmware modules are in `sys_modules/` |
| Very low FPS | Lower the GPU clock limit, ensure TDP is set to 15W |
| Controller not working in-game | Check Steam Input settings; PS4 games expect a DualShock 4, which Steam Deck emulates by default |
| Audio crackling | Try setting audio output to 48kHz in SteamOS settings |
| Game launches shadPS4 UI instead of game | Right-click the .desktop file > Properties > remove shadPS4 from "Open With" |
| "Invalid file or folder" in ES-DE | Change Alternative Emulator to `shadps4 Shortcut [Standalone]` |
