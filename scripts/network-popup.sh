#!/usr/bin/env sh
# Follow Sway's output scale rather than the monitor's physical DPI.
# Notify nmtui immediately when Sway applies the floating window size.
exec foot --app-id=foot-network \
    -c "${XDG_CONFIG_HOME:-$HOME/.config}/foot/foot-popup.ini" \
    -o dpi-aware=no \
    -o resize-delay-ms=0 \
    --window-size-chars=100x30 \
    sh -c '
        # nmtui lays out its dialogs at startup. Wait for the terminal
        # dimensions to settle after Sway maps and resizes the window.
        previous=
        stable=0
        attempts=0
        while [ "$stable" -lt 3 ] && [ "$attempts" -lt 20 ]; do
            sleep 0.1
            size=$(stty size)
            if [ "$size" = "$previous" ]; then
                stable=$((stable + 1))
            else
                stable=0
            fi
            previous=$size
            attempts=$((attempts + 1))
        done
        exec nmtui
    '
