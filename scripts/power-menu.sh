#!/usr/bin/env sh

choice="$(printf '%s\n' \
  "󰌾 Lock" \
  "󰤄 Suspend" \
  "󰍃 Logout" \
  "󰜉 Reboot" \
  "󰐥 Shutdown" |
  rofi -dmenu -i -p "Power" -theme ~/.config/rofi/config.rasi
)"

case "$choice" in
  "󰌾 Lock")
    /home/valeriot/Progetti/personali/fedora-sway-dotfiles/scripts/lock.sh
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
