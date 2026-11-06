#!/bin/bash
# Toggle the top bar and the screen space i3 reserves for it.
# Decides from whether the bar is actually open, so it cannot get out of sync.
# The flag file only tells fullscreen-monitor.py not to reopen a bar you hid.

FLAG="${XDG_RUNTIME_DIR:-/tmp}/eww-bar-hidden"
BAR_GAP=32   # keep in sync with `gaps top` in ~/.config/i3/config

if eww active-windows | grep -q '^bar:'; then
    touch "$FLAG"
    eww close bar
    i3-msg "gaps top all set 0" >/dev/null
else
    rm -f "$FLAG"
    eww open bar
    i3-msg "gaps top all set $BAR_GAP" >/dev/null
fi
