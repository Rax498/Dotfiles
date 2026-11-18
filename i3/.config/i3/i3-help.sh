#!/bin/bash
# Show every i3 keybinding in a searchable rofi list (Super+Ctrl+k).
# Type to filter, e.g. "tabbed" or "split" for the layout keys.
# `i3-help.sh --list` prints the same list to the terminal instead.

CONFIG="$HOME/.config/i3/config"
THEME="$HOME/.config/rofi/keybinds.rasi"

# Print the bindsym lines of the config. A binding inside `mode "name" { }`
# gets its key prefixed with the mode name ("resize:h"), so mode keys are listed
# and you can tell they only work after entering that mode.
bindings() {
    awk '
        /^[[:space:]]*mode[[:space:]]+"[^"]*"[[:space:]]*\{/ { split($0, q, "\""); mode = q[2]; next }
        /^[[:space:]]*\}/ { mode = ""; next }
        mode == "" && /^bindsym/ { print; next }
        mode != "" && /^[[:space:]]*bindsym[[:space:]]/ {
            sub(/^[[:space:]]*bindsym[[:space:]]+/, "bindsym " mode ":")
            print
        }
    ' "$CONFIG"
}

# One line per binding: key, then command.
list_bindings() {
    bindings |
        sed -e 's/bindsym //g' \
            -e 's/\$mod/Super/g' \
            -e 's/Mod4/Super/g' \
            -e 's/Mod1/Alt/g' \
            -e 's/--no-startup-id //g' \
            -e 's/--release //g' \
            -e 's/exec //g' |
        awk '{
            key = $1                 # first column: the key
            $1 = ""                  # the rest of the line is the command
            printf "%-25s  %s\n", key, $0
        }'
}

if [ "$1" = "--list" ]; then
    list_bindings
else
    list_bindings | rofi -dmenu -i -p " " -theme "$THEME"
fi
