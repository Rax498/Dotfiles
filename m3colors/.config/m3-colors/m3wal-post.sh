#!/bin/bash

# Kill proses lama dengan benar
pkill -x xsettingsd

# Tunggu proses benar-benar mati
sleep 0.8

# Generate rofi image
convert ~/.config/m3-colors/current_wallpaper -resize 800x -quality 100 ~/.config/m3-colors/current-rofi.jpg &

# Regenerate the real light-mode palette (m3wal itself only ever produces
# whichever single mode --mode/auto picked; this fills in the other one so
# the eww light theme isn't stuck reusing dark colours).
~/.config/m3-colors/hooks/gen-light-colors.py &

# Generate dunstrc
bash ~/.config/dunst/generate-dunstrc.sh &

# Tunggu sebentar biar file warna ke-generate dulu
sleep 0.3

# Start xsettingsd (hanya jika belum running)
pgrep -x xsettingsd > /dev/null || xsettingsd &

dunst &

# Tambahkan ini di wallpaper generator script setelah generate custom.lua
nvim --headless -c "lua require('base46').compile()" -c "qa"

# ── Dolphin color reload ──────────────────────────────────────────────────────
pkill -x dolphin 2>/dev/null || true
notify-send "[kde] Dolphin killed — New color will be applied"

# ── Terminal ANSI contrast ────────────────────────────────────────────────────
# The generator maps term0..term7 onto M3 container roles, which are background
# colours -- as foregrounds they come out at ~1.4:1 contrast and ls/yazi/git
# become unreadable. Rebuild those 16 colours with a contrast floor.
python3 ~/.config/m3-colors/hooks/ansi-contrast.py || true

# Reload i3 config
i3-msg reload &

exit 0
