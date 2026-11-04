#!/bin/bash
# Autostart for i3 -- from the reference dotfiles, adapted for Linux Mint.
#
# Differences from the reference (which targets Arch):
#   * setxkbmap: reference sets a us,ru layout toggle; kept this machine's
#     existing ctrl:nocaps instead.
#   * xsettingsd: not packaged/installed here, so that step is skipped.
#   * volume keys use pactl, not pamixer (pamixer is not installed on Mint).
#   * wallpaper uses ~/.fehbg, which exists on this machine.

# 1. Keyboard
setxkbmap -option ctrl:nocaps &

# 2. Notification daemon (must come up before anything that notifies)
pgrep -x dunst > /dev/null || dunst &
sleep 0.3

# 3. Wallpaper
[ -x ~/.fehbg ] && ~/.fehbg &

# 4. Compositor
killall -q picom compton xcompmgr
while pgrep -x picom >/dev/null || pgrep -x compton >/dev/null || pgrep -x xcompmgr >/dev/null; do
    sleep 0.1
done
if command -v picom &> /dev/null; then
    picom &
elif command -v compton &> /dev/null; then
    compton &
fi

# 5. Widgets (Eww) -- replaces polybar
killall eww 2>/dev/null
eww daemon
# wait for the daemon's IPC socket before opening the bar, or `open` races it
while ! eww ping &>/dev/null; do sleep 0.1; done
eww open bar

# 6. Monitor scripts
pkill -f fullscreen-monitor
python3 ~/.config/eww/scripts/fullscreen-monitor.py &
