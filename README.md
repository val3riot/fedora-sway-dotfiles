# Fedora Sway Dotfiles

Personal configuration for a Fedora workstation with Sway, Zsh, tmux and Neovim. Each configuration directory is a GNU Stow package, with paths relative to `$HOME`.

## Installation

On Fedora 44 or newer:

```sh
sudo dnf install \
  git stow curl unzip fontconfig sway swaybg swayidle swaylock waybar rofi foot dunst \
  NetworkManager NetworkManager-tui blueman bluez \
  pipewire pipewire-pulseaudio wireplumber wiremix \
  wl-clipboard cliphist grim slurp libnotify brightnessctl \
  zsh zsh-autosuggestions zsh-syntax-highlighting rsms-inter-fonts \
  tmux neovim ripgrep
```

Install [JetBrainsMono Nerd Font](https://github.com/ryanoasis/nerd-fonts/releases) for terminal text and icons:

```sh
font_archive="$(mktemp --suffix=.zip)"
curl --fail --location \
  https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/JetBrainsMono.zip \
  --output "$font_archive" &&
mkdir -p "$HOME/.local/share/fonts/JetBrainsMono" &&
unzip -n "$font_archive" -d "$HOME/.local/share/fonts/JetBrainsMono" &&
fc-cache -f "$HOME/.local/share/fonts/JetBrainsMono"
```

Clone the repository and preview the links before applying them. Back up existing configurations and resolve any Stow conflicts first.

```sh
git clone https://github.com/val3riot/fedora-sway-dotfiles.git
cd fedora-sway-dotfiles
stow --simulate --verbose --target="$HOME" dunst foot nvim rofi sway swaylock tmux waybar xdg zsh
stow --verbose --target="$HOME" dunst foot nvim rofi sway swaylock tmux waybar xdg zsh
```

You can link individual packages with `stow --target="$HOME" tmux nvim`. Keep the checkout available: the configuration files are symlinks into it. Stow does not install dependencies or configure system services, the login session or the default shell.

### Neovim file picker

Neovim uses the bundled Netrw tree and one plugin, [mini.pick](https://github.com/nvim-mini/mini.pick). Install it once; the destination must not already exist:

```sh
mkdir -p "${XDG_DATA_HOME:-$HOME/.local/share}/nvim/site/pack/dotfiles/start"
git clone https://github.com/nvim-mini/mini.pick.git \
  "${XDG_DATA_HOME:-$HOME/.local/share}/nvim/site/pack/dotfiles/start/mini.pick"
git -C "${XDG_DATA_HOME:-$HOME/.local/share}/nvim/site/pack/dotfiles/start/mini.pick" \
  checkout --detach 8c1f75f8ddd8c9f75d07ed2ab5718d2c3cb65a66
```

The plugin is pinned to a tested revision; no automatic downloads or updates. File search uses `ripgrep`, includes hidden files and respects ignore rules. No language servers or completion plugins are configured.

## Configuration

| Directory | Purpose |
| --- | --- |
| `sway/` | Compositor, workspaces, keyboard, startup and idle actions |
| `waybar/` | Status bar: network, audio, brightness, battery and power menu |
| `rofi/` | Application launcher and shared menu theme |
| `dunst/` / `swaylock/` | Notifications and lock screen |
| `foot/` | Terminal and popup profiles |
| `zsh/` / `xdg/` | Shell preferences and user-directory mappings |
| `tmux/` | Terminal sessions, panes, mouse and Wayland clipboard |
| `nvim/` | Minimal editor with file search, tree and clipboard shortcuts |
| `kate/` | Experimental GUI editor setup for Java and frontend; see [Kate setup](docs/kate.md) |
| `scripts/` / `assets/` | Desktop helpers and wallpaper; kept in the checkout |

Waybar opens network/audio popups and the power menu. Bluetooth uses Blueman; additional Bluetooth helpers are in `scripts/`. The desktop uses dark colors, Inter and JetBrainsMono Nerd Font.

## Shortcuts

Keep these tables in sync with the configuration when adding or changing shortcuts.

### Sway

Source: [30-keybinds.conf](sway/.config/sway/conf.d/30-keybinds.conf). `Super` is the Windows/Super key.

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

### tmux

Source: [tmux.conf](tmux/.config/tmux/tmux.conf). Press `Ctrl+b`, release it, then press the key below.

| Key after prefix | Action |
| --- | --- |
| `c` | New window in the current directory |
| `1`–`9` | Select a window |
| `\|` / `-` | Split side by side / top and bottom |
| `h` / `j` / `k` / `l` | Focus left / down / up / right pane |
| `z` | Toggle pane zoom |
| `[` | Enter scrollback/copy mode |
| `d` | Detach and keep the session running |
| `r` | Reload configuration |

In copy mode: move with arrows or `h/j/k/l`, `v` starts selection, `y` copies to the Wayland clipboard, `q` exits. Mouse selection also copies; hold Shift to select through Foot instead.

Start with `tmux new -s dev`; return with `tmux attach -t dev`. Sessions survive closing the terminal, but not a reboot.

### Neovim

Source: [init.lua](nvim/.config/nvim/init.lua). Start from the project root with `nvim .`. Press Escape before normal-mode shortcuts such as `Space f`.

| Shortcut | Action |
| --- | --- |
| `i` / Escape | Write / return to normal mode |
| Arrow keys | Move, including while writing |
| `v`, then movement | Select text; Escape cancels |
| `Ctrl+c` / `Ctrl+x` with a selection | Copy / cut |
| `Ctrl+v` | Paste, also while writing or over a selection |
| `Ctrl+s` | Save |
| `Ctrl+z` | Undo in normal or insert mode |
| Space, then `f` | Find files |
| Space, then `e` | Toggle the file tree |
| Enter in the tree | Expand directory / open file |
| `Ctrl+w`, then `w` | Switch between tree and editor |
| Space, then Right / Left | Widen / narrow the current panel |
| Space, then Up / Down | Increase / decrease the current panel's height |
| `/text`, then Enter | Search in file; `n` / `N` for next / previous |
| `:q`, then Enter | Close window; warns about unsaved changes |

The tree opens on the left, including with `nvim .`. Resize panels by dragging the divider with the mouse or using the shortcuts above after Escape. `Space e` hides the tree.

In the file picker: type to filter, arrows to select, Enter to open, Escape to cancel. Editing shortcuts apply to text buffers. Clipboard access requires `wl-clipboard` and an active Wayland session.

### Kate (experimental)

Setup and dependencies: [Kate](docs/kate.md). Open a project with `kate /path/to/project`.

| Shortcut | Action |
| --- | --- |
| `Ctrl+c` / `Ctrl+x` / `Ctrl+v` | Copy / cut / paste |
| `Ctrl+s` / `Ctrl+z` | Save / undo |
| `Ctrl+Alt+o` | Quick open files |
| `Ctrl+f` / `Ctrl+Shift+f` | Search in file / across files |
| `Ctrl+click` on a symbol | Go to definition with LSP |
| `F2` | Rename symbol with LSP |

## Machine-specific notes

- Adapt personal absolute paths in Sway, Waybar, swaylock and Zsh if cloning outside `~/Progetti/personali/fedora-sway-dotfiles`. Wallpaper: [main.jpg](assets/wallpapers/main.jpg).
- Sway uses an Italian keyboard layout. Lock after 30 minutes, screen off after 60, suspend after 90. Login-screen configuration is separate.
- Screenshots use `~/Immagini/` and `~/Immagini/Screenshots/`, while XDG maps pictures to `~/Pictures`. Create `~/Immagini/` before using region capture.
- Review battery/backlight modules and popup sizes for your hardware.
