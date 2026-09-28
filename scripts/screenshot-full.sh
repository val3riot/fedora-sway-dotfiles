#!/usr/bin/env sh

DIR="$HOME/Immagini/Screenshots"
mkdir -p "$DIR"

FILE="$DIR/screenshot-$(date +'%Y-%m-%d_%H-%M-%S').png"

grim "$FILE"

notify-send \
    "Screenshot salvato" \
    "$FILE"
