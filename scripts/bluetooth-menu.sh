#!/usr/bin/env sh

ROFI_THEME="$HOME/.config/rofi/config.rasi"

power_state="$(bluetoothctl show | awk '/Powered:/ {print $2}')"

if [ "$power_state" != "yes" ]; then
    action="$(
        printf '%s\n' \
            "󰂯 Enable Bluetooth" \
            "Cancel" |
        rofi -dmenu -i -p "Bluetooth" -theme "$ROFI_THEME"
    )"

    case "$action" in
        "󰂯 Enable Bluetooth")
            bluetoothctl power on >/dev/null 2>&1
            ;;
    esac

    exit 0
fi

paired_devices="$(
    bluetoothctl devices Paired |
    while read -r _ mac name; do
        if bluetoothctl info "$mac" | grep -q "Connected: yes"; then
            printf '󰂱 %s\t%s\n' "$name" "$mac"
        else
            printf '󰂯 %s\t%s\n' "$name" "$mac"
        fi
    done
)"

choice="$(
    {
        [ -n "$paired_devices" ] && printf '%s\n' "$paired_devices"

        printf '%s\n' \
            "──────────────" \
            "󰑐 Scan devices" \
            "󰂲 Disable Bluetooth"
    } |
    rofi -dmenu -i -p "Bluetooth" -theme "$ROFI_THEME"
)"

[ -z "$choice" ] && exit 0

case "$choice" in
    "󰑐 Scan devices")
        bluetoothctl scan on >/dev/null 2>&1 &
        scan_pid=$!

        sleep 5

        discovered="$(
            bluetoothctl devices |
            while read -r _ mac name; do
                printf '󰂯 %s\t%s\n' "$name" "$mac"
            done
        )"

        kill "$scan_pid" 2>/dev/null || true
        bluetoothctl scan off >/dev/null 2>&1

        selection="$(
            printf '%s\n' "$discovered" |
            rofi -dmenu -i -p "Bluetooth devices" -theme "$ROFI_THEME"
        )"

        [ -z "$selection" ] && exit 0

        mac="$(printf '%s' "$selection" | awk -F '\t' '{print $2}')"

        [ -z "$mac" ] && exit 0

        bluetoothctl pair "$mac"
        bluetoothctl trust "$mac"
        bluetoothctl connect "$mac"
        ;;

    "󰂲 Disable Bluetooth")
        bluetoothctl power off >/dev/null 2>&1
        ;;

    "──────────────")
        exit 0
        ;;

    *)
        mac="$(printf '%s' "$choice" | awk -F '\t' '{print $2}')"

        [ -z "$mac" ] && exit 0

        if bluetoothctl info "$mac" | grep -q "Connected: yes"; then
            bluetoothctl disconnect "$mac" >/dev/null 2>&1
        else
            bluetoothctl connect "$mac" >/dev/null 2>&1
        fi
        ;;
esac
