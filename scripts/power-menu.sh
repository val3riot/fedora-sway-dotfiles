#!/usr/bin/env sh

choice="$(printf '%s\n' \
  "󰌾 Lock" \
  "󰤄 Suspend" \
  "󰍃 Logout" \
  "󰜉 Reboot" \
  "󰐥 Shutdown" |
  rofi -dmenu -i -p "Power" -theme ~/.config/rofi/config.rasi \
    -theme-str 'listview { lines: 5; }'
)"

case "$choice" in
  "󰌾 Lock")
    swaylock -f
    ;;
  "󰤄 Suspend")
    systemctl suspend
    ;;
  "󰍃 Logout")
    swaymsg exit
    ;;
  "󰜉 Reboot")
    systemctl reboot
    ;;
  "󰐥 Shutdown")
    systemctl poweroff
    ;;
esac
