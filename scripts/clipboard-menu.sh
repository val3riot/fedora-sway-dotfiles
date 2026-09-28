#!/usr/bin/env sh

selection="$(cliphist list | rofi -dmenu -i -p "Clipboard" -theme ~/.config/rofi/config.rasi)"

[ -z "$selection" ] && exit 0

printf '%s' "$selection" | cliphist decode | wl-copy
