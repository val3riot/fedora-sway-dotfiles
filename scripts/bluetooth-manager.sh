#!/usr/bin/env sh

if swaymsg -t get_tree | grep -q '"app_id": "blueman-manager"'; then
    swaymsg '[app_id="blueman-manager"] focus'
else
    exec blueman-manager
fi
