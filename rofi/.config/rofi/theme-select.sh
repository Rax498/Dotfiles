#!/bin/bash
# Pick a colour scheme from my favourites and apply it with tinty.
# To add or remove a scheme, edit favorites.txt (`tinty list` shows all names).
TINTY="$HOME/.cargo/bin/tinty"
FAVORITES="$HOME/.config/tinted-theming/tinty/favorites.txt"

scheme=$(rofi -dmenu -i -p "theme" < "$FAVORITES")
[ -n "$scheme" ] && "$TINTY" apply "$scheme"
