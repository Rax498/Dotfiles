#!/bin/bash
# Pick a base16 colour scheme in rofi and apply it with tinty.
TINTY="$HOME/.cargo/bin/tinty"

scheme=$("$TINTY" list | grep '^base16-' | rofi -dmenu -i -p "theme")
[ -n "$scheme" ] && "$TINTY" apply "$scheme"
