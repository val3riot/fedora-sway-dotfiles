# Fedora Sway Dotfiles

Personal user-level dotfiles and desktop helpers for a Fedora workstation running Sway. Configuration packages mirror home-directory paths; there is no installer or Fedora provisioning script.

## Stack

| Component | Role |
| --- | --- |
| Sway | Wayland compositor, tiling workflow and window rules |
| Waybar | Top status bar and entry points for desktop controls |
| Rofi | Application launcher and selection menus |
| Dunst | Desktop notifications |
| Foot | Terminal and floating terminal utilities |
| swaylock / swayidle | Lock-screen configuration and idle actions |
| Blueman | Bluetooth tray applet and graphical device manager |
| Zsh | Interactive shell configuration |

## Features

- Five workspace shortcuts, directional focus/movement, fullscreen and floating toggles.
- Rofi application launcher, clipboard history selection and power menu.
- Floating NetworkManager and audio interfaces using Foot, `nmtui` and `wiremix`.
- Bluetooth helpers for Blueman and a separate Rofi/`bluetoothctl` menu.
- Full-screen and selected-region screenshots, notifications and a wallpaper-backed lock screen.
- Coordinated dark colors across the bar, launcher and window borders.

Some configured actions depend on a missing lock helper; see [Portability and current limitations](#portability-and-current-limitations).

## Installation

The repository does not record an established deployment command. Its eight configuration directories are compatible with GNU Stow: each contains paths relative to `$HOME`. The following is an optional way to link them, not a bundled installer.

Review existing configuration and back it up first. Install the required tools separately, then clone and link the packages:

```sh
git clone https://github.com/val3riot/fedora-sway-dotfiles.git
cd fedora-sway-dotfiles
stow --simulate --verbose --target="$HOME" dunst foot rofi sway swaylock waybar xdg zsh
stow --verbose --target="$HOME" dunst foot rofi sway swaylock waybar xdg zsh
```

GNU Stow must be installed for these commands. Resolve any reported conflicts before applying the links. `assets` and `scripts` stay in the checkout and are not Stow packages. Keep the checkout available while using its symlinks.

Before using the desktop, adapt the personal script/wallpaper paths and review the missing lock helper described below. Linking files does not install dependencies, enable system services, select a login session or change the default shell.

## Repository structure

```text
fedora-sway-dotfiles/
├── assets/     # Wallpaper assets
├── dunst/      # Notification configuration
├── foot/       # Regular terminal and popup profiles
├── rofi/       # Launcher and shared menu theme
├── scripts/    # Desktop utility helpers
├── sway/       # Compositor config and modular conf.d files
├── swaylock/   # Lock-screen appearance
├── waybar/     # Bar modules and CSS
├── xdg/        # User-directory mappings
└── zsh/        # Interactive shell configuration
```

## Dependencies

These are commands/components referenced by the configuration, rather than a verified Fedora package-install list.

### Core

- `sway` / `swaymsg`, `waybar`, a Wayland-capable `rofi`, `foot`, `dunst`.
- `swaybg` for Sway's configured output background; `swaylock` and `swayidle` for lock/idle configuration.
- Inter and JetBrainsMono Nerd Font; the latter supplies the configured icon glyphs.

### Desktop utilities

- NetworkManager with `nmtui` for the network popup.
- `wiremix` for the audio popup; `wpctl` (WirePlumber) for mute control. Waybar uses its `pulseaudio` module, requiring a compatible audio service such as PipeWire's PulseAudio interface.
- `blueman-applet`, `blueman-manager` and BlueZ's `bluetoothctl` for Bluetooth controls.
- `wl-paste`, `wl-copy` and `cliphist` for clipboard history.
- `grim`, `slurp` and `notify-send` for screenshots and notifications.
- `brightnessctl` for backlight adjustment; battery/backlight modules depend on available hardware.
- `systemctl` for suspend, reboot and shutdown; POSIX `sh` and standard utilities including `awk`, `grep`, `stty`, `sleep`, `pkill` and `date`.

### Shell

- `zsh`, with plugins sourced from `/usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh` and `/usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh`.
- GNU Stow only if using the optional linking instructions above.

## Keybindings

Source: [30-keybinds.conf](sway/.config/sway/conf.d/30-keybinds.conf). `Super` is `Mod4`.

| Shortcut | Action |
| --- | --- |
| Super + Enter | Open Foot |
| Super + D | Open Rofi application launcher |
| Super + Shift + Q | Close focused window |
| Super + Shift + C | Reload Sway configuration |
| Super + H / J / K / L | Focus left / down / up / right |
| Super + Shift + H / J / K / L | Move window left / down / up / right |
| Super + F | Toggle fullscreen |
| Super + Space | Toggle floating |
| Super + 1–5 | Switch workspace |
| Super + Shift + 1–5 | Move window to workspace |
| Super + Shift + S | Save selected region under `~/Immagini/` with `grim` and `slurp` |
| Print | Save full screenshot under `~/Immagini/Screenshots/` and notify |
| Super + Ctrl + L | Run `swaylock` directly |
| Super + V | Select clipboard history entry |
| Super + P | Open power menu |
| Power button (`XF86PowerOff`) | Suspend through `systemctl` |

## Waybar

The 32-pixel top bar places workspaces and Sway mode on the left, the focused window title in the center, and network, audio, backlight, battery, clock, tray and a custom power button on the right. Workspaces 1–5 remain visible, with bounded application labels and icon/name rewrites for common applications; these mappings do not install those applications.

- Network click opens the network popup; tooltips show connection details.
- Audio click opens `wiremix`; right-click toggles the default sink's mute state with `wpctl`. Volume scrolling uses a step of 5.
- Backlight scrolling changes brightness by 5% through `brightnessctl`.
- The clock has an alternate date/time format and a calendar tooltip.
- The custom power button opens the Rofi power menu. The tray hosts applets such as Blueman.

A Bluetooth module is defined but omitted from the active module lists. Its configured click command would open `bluetoothctl` in Foot; it does not invoke the Bluetooth helper scripts.

## System popups and menus

Helpers live in [scripts/](scripts/). Network/audio popups use the separate Foot popup profile and Sway app-ID rules to float and center their windows.

| Script | Actual behavior and entry point |
| --- | --- |
| `network-popup.sh` | Waybar network click opens `nmtui` in `foot-network`, after waiting for terminal dimensions to settle. Sway sizes it to 70% of the output width and height. |
| `audio-popup.sh` | Waybar audio click opens `wiremix` in `foot-audio`; Sway requests a centered 1180 × 700 window. |
| `bluetooth-manager.sh` | Focuses an existing `blueman-manager` window or launches it; Sway requests a centered 850 × 600 window. No configured binding/click invokes this helper. |
| `bluetooth-menu.sh` | Standalone Rofi menu: enable/disable Bluetooth, connect/disconnect paired devices, or scan for five seconds and pair, trust and connect a selected device. No configured binding/click invokes it. |
| `clipboard-menu.sh` | Super + V lists `cliphist` entries in Rofi, decodes the selection and copies it with `wl-copy`. |
| `power-menu.sh` | Super + P / Waybar power button offers lock, suspend, logout, reboot and shutdown. Lock calls the absent `scripts/lock.sh`; the other entries call `systemctl` or `swaymsg exit`. |
| `screenshot-full.sh` | Print creates `~/Immagini/Screenshots/`, captures with `grim` and calls `notify-send` with the saved path. |

Sway startup launches Dunst, `blueman-applet`, and separate text/image `wl-paste` watchers feeding `cliphist`. Waybar is restarted on configuration reload through `exec_always`.

## Appearance

Sway, Waybar and Rofi use dark backgrounds around `#16181d`, pale text `#d8dee9`, a warm `#d08770` accent and rose `#d16d7a` urgency colors. Dunst and swaylock also use blue `#7aa2d6` accents. Foot uses a separate dark `#11111b` background with pastel terminal colors.

Sway uses Inter 10, 3-pixel default borders, 10-pixel inner gaps and 8-pixel outer gaps. Other components use JetBrainsMono Nerd Font. Waybar has a 45%-opaque background and rounded workspace buttons; Rofi is centered at 42% width with a translucent background, 2-pixel accent border and rounded corners. Foot background opacity is 0.88 normally and 0.92 for popups. Dunst places rounded notifications at the top right.

## Wallpapers

[assets/wallpapers/main.jpg](assets/wallpapers/main.jpg) is the only tracked image. Sway applies it to all outputs with `fill`; swaylock uses it with the same scaling. Both references are absolute personal paths and need review on another machine. No desktop screenshot is included in the repository.

## Zsh and XDG

[.zshrc](zsh/.zshrc) configures 50,000-entry shared history, duplicate/leading-space history filtering, automatic directory changes and case-insensitive completion with menu selection. It sources autosuggestions and syntax highlighting from system paths and prepends a hard-coded personal `.local/bin` directory to `PATH`. No custom prompt is configured.

[user-dirs.dirs](xdg/.config/user-dirs.dirs) maps Desktop, Downloads, Templates, Public, Documents, Music, Pictures and Videos to English directory names under `$HOME`.

## Portability and current limitations

- Sway keybindings, Waybar actions, wallpaper configuration, swaylock and Zsh contain personal absolute paths or assume `~/Progetti/personali/fedora-sway-dotfiles`. Cloning elsewhere requires adapting these references; Stow does not rewrite them.
- `scripts/lock.sh` is absent. Both the power menu's lock entry and swayidle's 30-minute/before-sleep lock commands reference it. The direct Super + Ctrl + L binding runs `swaylock` independently.
- The configured idle schedule also powers off outputs after 60 minutes (restoring them on activity) and requests suspend after 90 minutes. The missing helper prevents relying on the configured automatic lock actions.
- The keyboard layout is Italian. Touchpad tap, natural scrolling and disable-while-typing are enabled.
- Region screenshots require `~/Immagini/` to exist; the full-screen helper creates its own destination there. These paths differ from XDG's configured `~/Pictures` directory.
- Battery/backlight controls and fixed popup sizes should be reviewed for the target hardware/display. No specific output name is pinned: wallpaper and idle output commands target all outputs.

## What this repository is not

This repository contains user-level dotfiles and desktop helpers. It is not a full Fedora provisioning framework or a complete workstation installer.
