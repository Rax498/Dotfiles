# Dotfiles

My Linux (i3) setup. Each top-level folder is a [GNU Stow](https://www.gnu.org/software/stow/) package: `stow <name>` links it into `~`.

## Theming

All colours come from one [Base16](https://github.com/tinted-theming/home) scheme, applied by [tinty](https://github.com/tinted-theming/tinty). App configs contain no hex colours; they include a generated file.

| App | Generated file | Notes |
|---|---|---|
| alacritty | `~/.config/alacritty/colors.toml` | |
| polybar | `~/.config/polybar/base16.ini` | optional: not started at login (the eww bar is); run `polybar/.config/polybar/launch_polybar.sh` to use it. `colors.ini` maps the palette to the names the bar uses |
| rofi | `~/.config/rofi/colors.rasi` | imported by every rofi style |
| i3 | `~/.config/i3/colors.conf` | palette + `client-colors.conf` |
| dunst | `~/.config/dunst/dunstrc.d/99-colors.conf` | dunst is restarted on apply |
| eww | `~/.config/eww/colors.scss` | `eww/.config/eww/scripts/gen-colors.py` maps the 16 colours to Material names |

`lazygit` is not driven by tinty: `lazygit/.config/lazygit/config.yml` is the fixed Luna theme from [luna.nvim](https://github.com/WTFox/luna.nvim). (Inside nvim, snacks.nvim colours lazygit from the nvim colourscheme instead.)

Generated files are gitignored. Everything that wires tinty to the apps is in `tinty/.config/tinted-theming/tinty/config.toml`.

### Change theme

- `$mod+Shift+t` opens a rofi list of my favourite schemes (`tinty/.config/tinted-theming/tinty/favorites.txt`: add or remove names there).
- Or: `tinty apply base16-gruvbox-dark-hard` (`tinty list` shows all names).
- Apply the new i3 colours with `$mod+Shift+r`. Windows that are already open keep their old colours.
- `$mod+Shift+b` only changes the wallpaper.

### Setup on a new machine

```sh
cargo install tinty --locked
stow tinty alacritty polybar rofi i3 dunst eww
tinty sync                              # downloads schemes and app templates
tinty apply base16-catppuccin-mocha
```

### Add an app

Add an `[[items]]` block to the tinty config (template repo, theme folder, a `hook` that copies the file to a fixed path), include that path from the app's config, and gitignore it.

### Add your own scheme

Put a Base16 `.yaml` file (same format as the ones in `~/.local/share/tinted-theming/tinty/scheme-repos/schemes/base16/`) in `tinty/.local/share/tinted-theming/tinty/custom-schemes/base16/`, run `stow tinty`, and add `base16-<name>` to `favorites.txt`. `luna.yaml` there is an example ([WTFox/luna.nvim](https://github.com/WTFox/luna.nvim)); its palette comes from the theme's alacritty file.

### Scheme from a wallpaper

```sh
tinty generate-scheme --system base16 --save --slug mine --name "Mine" path/to/image.jpg
tinty apply base16-mine
```

## Keybindings

`Super+Ctrl+k` opens a searchable list of every shortcut; the full list is also in
[KEYBINDINGS.md](KEYBINDINGS.md). The modifier tells you
what a key does, and directions are always `h j k l` (arrow keys work too):

| Modifier | Meaning | Examples |
|---|---|---|
| `Super` | go to something / main action | focus `h j k l`, workspace `1-0`, close `w`, float `t`, fullscreen `f` |
| `Super+Shift` | **move** it | move window `h j k l`, send to workspace `1-0`, to scratchpad `minus` |
| `Super+Alt` | reshape the **layout** (i3's stock layout letters) | split `h` / `v`, tabbed `w`, stacking `s`, toggle split `e` |
| `Super+Ctrl` | **system** / session | lock `l`, shortcut help `k`, performance monitor `t` |

Tabs: `Super+Alt+w` makes the container tabbed, `Super+h` / `Super+l` switch tabs,
`Super+Alt+e` goes back to normal tiling. `Super+g` (Omarchy's key) toggles tabs
on and off with one key.

Floating: `Super+t` (or `Super+Shift+space`) floats / unfloats the focused window, any
number of windows can float. `Super+space` switches focus between the floating and
the tiling windows. Hold `Super` and drag: left mouse button moves, right mouse
button resizes.
