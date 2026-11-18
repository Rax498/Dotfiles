# Keybindings

Generated from `i3/.config/i3/config`. Do not edit by hand; regenerate with:

    ~/.config/i3/i3-help.sh --list

`Super` is the Windows/logo key. The modifier tells you what a key does:

| Modifier | Meaning |
|---|---|
| `Super` | go to something / main action |
| `Super+Shift` | move it |
| `Super+Alt` | reshape the layout |
| `Super+Ctrl` | system / session |

A key shown as `resize:h` only works inside that mode (`Super+r` enters resize).

```
Super+d                     ~/.config/rofi/launchers/type-6/launcher.sh
Super+Ctrl+k                ~/.config/i3/i3-help.sh
Ctrl+Super+Right            ~/.config/Scripts/ws_cycle.sh next
Ctrl+Super+Left             ~/.config/Scripts/ws_cycle.sh prev
Super+Ctrl+l                lock
XF86AudioRaiseVolume        pactl set-sink-volume @DEFAULT_SINK@ +5% && ~/.config/eww/scripts/volume-popup.sh
XF86AudioLowerVolume        pactl set-sink-volume @DEFAULT_SINK@ -5% && ~/.config/eww/scripts/volume-popup.sh
XF86AudioMute               pactl set-sink-mute @DEFAULT_SINK@ toggle && ~/.config/eww/scripts/volume-popup.sh
XF86AudioPause              playerctl play-pause
XF86AudioPlay               playerctl play-pause
XF86AudioNext               playerctl next
XF86AudioPrev               playerctl previous
XF86AudioStop               playerctl stop
XF86MonBrightnessUp         ~/.config/i3/brightness.sh up && ~/.config/eww/scripts/brightness-popup.sh
XF86MonBrightnessDown       ~/.config/i3/brightness.sh down && ~/.config/eww/scripts/brightness-popup.sh
Super+Shift+Return          DRI_PRIME=1 alacritty
Super+Return                alacritty
Super+Shift+f               nemo
Super+b                     zen
Super+Shift+e               ~/.config/rofi/powermenu/type-5/powermenu.sh
Super+Escape                ~/.config/rofi/powermenu/type-5/powermenu.sh
Super+Alt+space             ~/.config/eww/scripts/toggle-panel.sh start_menu
Super+Ctrl+t                eww open --toggle performance_monitor
Super+z                     ~/.config/eww/scripts/toggle-bar.sh
Super+Shift+b               ~/.config/rofi/wpg-select.sh
Super+Shift+t               ~/.config/rofi/theme-select.sh
Print                       scrot ~/Pictures/Screenshots/screenshot_%Y%m%d_%H%M%S.png
Super+Shift+s               scrot -s ~/Pictures/Screenshots/screenshot_%Y%m%d_%H%M%S.png
Super+Ctrl+Shift+s          scrot -s /tmp/screenshot.png && xclip -selection clipboard -t image/png -i /tmp/screenshot.png
Super+w                     kill
Super+h                     focus left
Super+j                     focus down
Super+k                     focus up
Super+l                     focus right
Super+Left                  focus left
Super+Down                  focus down
Super+Up                    focus up
Super+Right                 focus right
Super+Shift+h               move left
Super+Shift+j               move down
Super+Shift+k               move up
Super+Shift+l               move right
Super+Shift+Left            move left
Super+Shift+Down            move down
Super+Shift+Up              move up
Super+Shift+Right           move right
Super+f                     fullscreen toggle
Super+minus                 scratchpad show
Super+Shift+minus           move scratchpad
Super+Alt+h                 split h
Super+Alt+v                 split v
Super+Alt+w                 layout tabbed
Super+Alt+s                 layout stacking
Super+Alt+e                 layout toggle split
Super+g                     layout toggle tabbed split
Super+a                     focus parent
Super+t                     floating toggle
Super+Shift+space           floating toggle
Super+space                 focus mode_toggle
Super+Shift+v               floating toggle, resize set 500 300, move position center
Super+1                     workspace $ws1
Super+2                     workspace $ws2
Super+3                     workspace $ws3
Super+4                     workspace $ws4
Super+5                     workspace $ws5
Super+6                     workspace $ws6
Super+7                     workspace $ws7
Super+8                     workspace $ws8
Super+9                     workspace $ws9
Super+0                     workspace $ws10
Super+Shift+1               move container to workspace $ws1
Super+Shift+2               move container to workspace $ws2
Super+Shift+3               move container to workspace $ws3
Super+Shift+4               move container to workspace $ws4
Super+Shift+5               move container to workspace $ws5
Super+Shift+6               move container to workspace $ws6
Super+Shift+7               move container to workspace $ws7
Super+Shift+8               move container to workspace $ws8
Super+Shift+9               move container to workspace $ws9
Super+Shift+0               move container to workspace $ws10
Super+Shift+c               reload
Super+Shift+r               restart
resize:h                    resize shrink width 5 px or 5 ppt
resize:j                    resize grow height 5 px or 5 ppt
resize:k                    resize shrink height 5 px or 5 ppt
resize:l                    resize grow width 5 px or 5 ppt
resize:Left                 resize shrink width 10 px or 10 ppt
resize:Down                 resize grow height 10 px or 10 ppt
resize:Up                   resize shrink height 10 px or 10 ppt
resize:Right                resize grow width 10 px or 10 ppt
resize:Return               mode "default"
resize:Escape               mode "default"
resize:Super+r              mode "default"
Super+r                     mode "resize"
voice:Return                mode "default"; pkill -f bridge.sh; pkill voicewm; dunstctl close 999
voice:Escape                mode "default"; pkill -f bridge.sh; pkill voicewm; dunstctl close 999
Super+m                     mode "voice"; ~/.config/eww/scripts/bridge.sh
```
