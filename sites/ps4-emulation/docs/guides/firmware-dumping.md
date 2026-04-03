# Dumping Firmware & Trophies

## Getting the Files You Need from Your PS4

shadPS4 can optionally load PS4 firmware modules for better game compatibility, and supports the trophy system if you provide the trophy decryption key. Both require a **jailbroken PS4** to obtain.

!!! warning "Legal Notice"
    You must dump these files from your own legally purchased PlayStation 4 console. We do not provide links to firmware files or system software downloads.

## What Is a Jailbroken PS4?

A jailbroken PS4 is a console running custom firmware that allows you to:

- Run homebrew applications
- Dump games and firmware files
- Access the file system via FTP

Jailbreaking is currently available for PS4 consoles on **firmware 11.00 or lower**. The most well-supported jailbreak firmware versions are 9.00 and below.

This guide does not cover the jailbreaking process itself. See community resources for instructions specific to your PS4's firmware version.

## Dumping Firmware Modules

### What Are Firmware Modules?

PS4 firmware modules (`.sprx` files) are system libraries that handle specific functionality. shadPS4 reimplements many of these (HLE mode), but some are not yet reimplemented and need to be loaded directly from the PS4's firmware (LLE mode).

### Required Modules

| Module | Purpose |
|--------|---------|
| libSceCesCs.sprx | Character encoding conversion |
| libSceFont.sprx | Font rendering |
| libSceFontFt.sprx | FreeType font rendering |
| libSceFreeTypeOt.sprx | OpenType font support |
| libSceJpegDec.sprx | JPEG image decoding |
| libSceJpegEnc.sprx | JPEG image encoding |
| libSceJson.sprx | JSON parsing |
| libSceJson2.sprx | JSON parsing v2 |
| libSceLibcInternal.sprx | C standard library |
| libSceNgs2.sprx | Next-gen audio system |
| libScePngEnc.sprx | PNG image encoding |
| libSceRtc.sprx | Real-time clock |
| libSceUlt.sprx | Ultra-lightweight threads |
| libSceAudiodec.sprx | Audio decoding |

### Dumping Steps

1. **Enable FTP on your PS4**
    - Launch the jailbreak payload on your PS4
    - Start an FTP server (most jailbreak tools include one)
    - Note the IP address displayed on screen

2. **Connect via FTP**
    - Open an FTP client on your PC (FileZilla works well)
    - Connect to your PS4's IP address on the displayed port
    - Authentication is typically not required (anonymous access)

3. **Navigate to the system libraries**
    ```
    /system/common/lib/
    ```

4. **Download all .sprx files**
    - Select all files in the directory
    - Download them to a folder on your PC

5. **Place files in shadPS4's sys_modules folder**
    - **QtLauncher**: Right-click any game > Open Folder > Open Log Folder > Go up one directory > find `sys_modules/`
    - **CLI**: The `sys_modules/` folder is in the shadPS4 directory
    - Copy all downloaded `.sprx` files into this folder

!!! tip "Download Everything"
    While only the modules listed above are currently used by shadPS4, downloading all files from `/system/common/lib/` future-proofs your setup. New shadPS4 versions may support additional modules.

## Dumping the Trophy Key

### What Is the Trophy Key?

The trophy key is used to decrypt PS4 trophy data, allowing shadPS4 to unlock and display trophies as you play games. Without it, trophy functionality will not work.

### Dumping Steps

1. **Dump SceShellCore.elf from your PS4**
    - Using FTP, navigate to `/system/vsh/`
    - Download `SceShellCore.elf` to your PC

2. **Extract the trophy key**
    - Download [trophy_key_export.zip](https://github.com/user-attachments/files/21354959/tropy_key_export.zip)
    - This tool was created by `red-prig` (the fpPS4 developer)
    - Extract the ZIP file

3. **Run the extraction tool**
    - **Windows**: Drag `SceShellCore.elf` onto `tropy_key_export.exe`
    - **Linux**: Use Wine to run the tool: `wine tropy_key_export.exe SceShellCore.elf`
    - **macOS**: No native option yet; use a Windows VM or Wine

4. **A command prompt window will display your trophy key**
    - Copy the key string

5. **Enter the key in shadPS4**
    - **QtLauncher**: Go to Settings > enter the trophy key in the appropriate field
    - **CLI**: Add the key to your `config.toml` file

## Dumping Games

### Using Itemzflow (Recommended)

Itemzflow is a user-friendly homebrew app for PS4 that handles game dumping:

1. Install Itemzflow on your jailbroken PS4
2. Navigate to the game you want to dump
3. Select the dump option
4. The game will be dumped to your PS4's internal or external storage
5. Game folders follow the `CUSAxxxxx` naming convention automatically

### Transferring Games to PC

After dumping:

1. **FTP** -- Transfer the game folder via FTP (slow for large games)
2. **USB drive** -- Copy to a USB drive connected to the PS4 (faster)
3. **Network share** -- Set up an SMB share if your PS4's homebrew supports it

### Expected Game Sizes

| Game Type | Typical Size |
|-----------|-------------|
| Indie / Small | 1-5 GB |
| Mid-tier | 10-30 GB |
| AAA | 40-100 GB |
| AAA with DLC | 60-150 GB |

## Dumping Updates and DLC

### Game Updates

1. Ensure the update is installed on your PS4
2. Dump the update using Itemzflow or a similar tool
3. The update folder will be named `CUSAxxxxx-patch` or `CUSAxxxxx-UPDATE`
4. Copy it alongside the base game in your shadPS4 game directory

### DLC

1. Ensure DLC is installed on your PS4
2. Dump the DLC packages
3. Place DLC in your shadPS4 additional content directory:
    - Create a folder with the game's CUSA ID (e.g., `CUSA00900/`)
    - Copy DLC files into that folder

## Verification

After setting up firmware modules, verify they're loaded:

1. Launch a game that requires firmware modules (most 3D games do)
2. Check the shadPS4 log for lines indicating modules are loaded
3. If you see "module not found" errors, verify the file names and placement in `sys_modules/`
