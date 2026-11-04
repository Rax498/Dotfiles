#!/usr/bin/env bash
# Launch one bar per connected monitor.
# Kills any running bars first, so running this twice does not stack duplicates.

killall -q polybar
# wait for the old bars to release the IPC socket before spawning new ones
while pgrep -x polybar >/dev/null; do sleep 0.1; done

# Fully detached (stdio redirected, own session) so this script returns
# immediately instead of blocking its caller on an open pipe.
if type "xrandr" >/dev/null 2>&1; then
    for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
        MONITOR=$m setsid polybar --reload toph </dev/null >/dev/null 2>&1 &
    done
else
    setsid polybar --reload toph </dev/null >/dev/null 2>&1 &
fi
