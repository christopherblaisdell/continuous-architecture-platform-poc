# Keyboard and Controller Mapping

## Default Keyboard Controls

shadPS4 maps PS4 controller buttons to keyboard keys by default. These can be customized in the emulator settings.

### Button Mapping

| PS4 Button | Keyboard Key | Action |
|------------|-------------|--------|
| Cross (X) | ++enter++ | Confirm / Accept |
| Circle (O) | ++backspace++ | Cancel / Back |
| Square | ++z++ | Context action |
| Triangle | ++v++ | Context action |
| D-Pad Up | ++up++ | Menu / Movement |
| D-Pad Down | ++down++ | Menu / Movement |
| D-Pad Left | ++left++ | Menu / Movement |
| D-Pad Right | ++right++ | Menu / Movement |
| L1 | ++q++ | Left bumper |
| R1 | ++u++ | Right bumper |
| L2 | ++e++ | Left trigger |
| R2 | ++r++ | Right trigger |
| Left Stick | ++w++ ++a++ ++s++ ++d++ | Movement |
| Right Stick | ++i++ ++j++ ++k++ ++l++ | Camera |
| L3 (stick click) | ++x++ | Left stick press |
| R3 (stick click) | ++n++ | Right stick press |
| Options | ++space++ | Start / Pause |
| Touchpad Button | ++c++ | Touchpad click |
| Touchpad Axis | ++f++ | Touchpad movement |

!!! note "Keyboard Limitations"
    Keyboard controls lack analog input. L2/R2 triggers are binary (fully pressed or not), and stick movement has no gradual sensitivity. A controller is strongly recommended for most games.

## Controller Support

### Native Controller Support

shadPS4 supports standard game controllers natively through SDL2:

| Controller | Support Level | Notes |
|------------|--------------|-------|
| DualShock 4 (DS4) | Full | Touchpad, gyro, lightbar (on supported builds) |
| DualSense (PS5) | Full | Touchpad, adaptive triggers (partial) |
| Xbox One / Series | Full | Standard mapping, no touchpad |
| Xbox 360 | Full | Wired and wireless adapter |
| Nintendo Pro Controller | Good | Standard mapping via SDL2 |
| 8BitDo controllers | Good | Depends on firmware mode |
| Generic USB / Bluetooth | Varies | Must be recognized by SDL2 |

### DualShock 4 and DualSense

Using an actual PlayStation controller provides the most authentic experience:

- **Touchpad** is fully functional for games that require touchpad input
- **Gyroscope** support is being implemented (check release notes for status)
- **Lightbar** can be used for visual feedback on supported platforms
- Connect via **USB** for best reliability, or **Bluetooth** for wireless

!!! tip "DS4 on Linux"
    DualShock 4 controllers are supported natively in the Linux kernel. Just connect via USB or pair via Bluetooth. No additional drivers needed. The controller appears as both a gamepad and a touchpad device.

### Xbox Controllers

Xbox controllers work well but lack a touchpad. For games requiring touchpad input:

- Some games accept alternative inputs (check per-game settings)
- You can map a keyboard key to touchpad alongside your controller
- Very few games make touchpad input mandatory for progression

## Steam Deck Controls

### Default Mapping (Gaming Mode)

When running shadPS4 through Steam Gaming Mode, the Steam Deck's built-in controls map automatically:

| Steam Deck | PS4 Equivalent |
|------------|---------------|
| A / B / X / Y | Cross / Circle / Square / Triangle |
| D-Pad | D-Pad |
| Left Stick | Left Stick |
| Right Stick | Right Stick |
| L1 / R1 | L1 / R1 |
| L2 / R2 | L2 / R2 |
| L4 / R4 (back buttons) | Unassigned (customizable) |
| Left Trackpad | Mouse / Touchpad (configurable) |
| Right Trackpad | Mouse / Right Stick (configurable) |
| STEAM + Left Trigger | Screenshot (Steam overlay) |

### Recommended Steam Deck Layout

For PS4 emulation, configure the back buttons and trackpads:

| Control | Recommended Mapping |
|---------|-------------------|
| L4 (back left) | L3 (left stick click) |
| R4 (back right) | R3 (right stick click) |
| Left Trackpad | Touchpad (for games that need it) |
| Right Trackpad | Right stick (as gyro alternative) |

### Using Gyro on Steam Deck

Steam Deck's gyroscope can simulate right stick movement (useful for aiming):

1. Open the controller layout in Steam
2. Set Gyro to **Right Stick**
3. Set activation to **L2 Soft Pull** or **Touch Right Trackpad**
4. Adjust sensitivity to taste

## Customizing Controls in shadPS4

### Through the QtLauncher

1. Open shadPS4's QtLauncher
2. Go to **Settings** > **Input**
3. Select your controller from the device list
4. Remap buttons as desired
5. Save the configuration

### Per-Game Profiles

Some games benefit from custom control layouts:

- **Racing games**: Remap L2/R2 to analog triggers if using a controller that supports them
- **Platformers**: Consider remapping jump to a face button that feels natural
- **Games with touchpad**: Ensure touchpad or trackpad is mapped correctly

## Hotkeys

| Hotkey | Action |
|--------|--------|
| ++f11++ | Toggle fullscreen |
| ++f10++ | Toggle FPS counter |
| ++escape++ | Exit emulator / close game |

!!! info "Hotkeys may vary by version"
    shadPS4's hotkey assignments can change between releases. Check the current version's documentation or settings menu for the latest bindings.
