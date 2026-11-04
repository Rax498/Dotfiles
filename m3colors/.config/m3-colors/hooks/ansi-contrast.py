#!/usr/bin/env python3
"""Rebuild the 16 ANSI colors with guaranteed contrast against the terminal
background.

The Material You generator maps term0..term7 onto M3 "container"/"on*" roles,
which are meant to be *backgrounds*. Used as foregrounds they are nearly
invisible: on the lofi scheme, `ls` directories came out as #381b78 on a
#141218 background (contrast 1.3:1). Anything that paints with ANSI colours --
ls, yazi, git, fzf, bat -- became unreadable, while nvim was fine because it
uses its own truecolor palette.

This regenerates ANSI 1-6 at the canonical hues, tinted toward the wallpaper's
accent hue so the scheme still feels cohesive, then lifts each colour until it
clears a minimum WCAG contrast ratio against the background.
"""

import colorsys
import json
import os
import re
import sys

CACHE = os.path.expanduser("~/.cache/m3-colors")

# Canonical ANSI hues (degrees) for red, green, yellow, blue, magenta, cyan.
HUES = [2.0, 135.0, 50.0, 250.0, 300.0, 190.0]

ACCENT_TINT = 0.18   # how far each hue is pulled toward the accent hue
MAX_ROTATION = 8.0   # ...but never far enough that yellow reads as orange
SAT_NORMAL = 0.55
SAT_BRIGHT = 0.70
MIN_CONTRAST_NORMAL = 5.5
MIN_CONTRAST_BRIGHT = 8.0
MIN_CONTRAST_DIM = 3.2   # ANSI 8, used for comments and inactive UI


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c * 255))) for c in rgb)


def luminance(rgb):
    def chan(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def blend_hue(hue, accent_hue, amount):
    """Rotate `hue` toward `accent_hue` along the shorter arc."""
    delta = ((accent_hue - hue + 180.0) % 360.0) - 180.0
    shift = delta * amount
    shift = max(-MAX_ROTATION, min(MAX_ROTATION, shift))
    return (hue + shift) % 360.0


def fit_contrast(hue, sat, bg, target, dark_bg):
    """Pick the lightness closest to a pleasant mid-tone that still clears
    `target` contrast against the background."""
    start, step = (0.72, 0.01) if dark_bg else (0.38, -0.01)
    light = start
    best = None
    for _ in range(60):
        rgb = colorsys.hls_to_rgb(hue / 360.0, light, sat)
        if contrast(rgb, bg) >= target:
            best = rgb
            break
        light += step
        if not 0.0 <= light <= 1.0:
            break
    if best is None:
        best = colorsys.hls_to_rgb(hue / 360.0, 0.95 if dark_bg else 0.12, sat)
    return best


def build(bg_hex, fg_hex, accent_hex):
    bg = hex_to_rgb(bg_hex)
    fg = hex_to_rgb(fg_hex)
    dark_bg = luminance(bg) < 0.5
    accent_hue = colorsys.rgb_to_hls(*hex_to_rgb(accent_hex))[0] * 360.0

    normal, bright = [], []
    for hue in HUES:
        h = blend_hue(hue, accent_hue, ACCENT_TINT)
        normal.append(fit_contrast(h, SAT_NORMAL, bg, MIN_CONTRAST_NORMAL, dark_bg))
        bright.append(fit_contrast(h, SAT_BRIGHT, bg, MIN_CONTRAST_BRIGHT, dark_bg))

    # ANSI 0 / 8: neutral greys tinted with the accent hue.
    ansi0 = colorsys.hls_to_rgb(accent_hue / 360.0, 0.16 if dark_bg else 0.24, 0.10)
    ansi8 = fit_contrast(accent_hue, 0.12, bg, MIN_CONTRAST_DIM, dark_bg)

    # ANSI 7 sits one notch below the foreground so bold/bright still reads.
    h7, l7, s7 = colorsys.rgb_to_hls(*fg)
    ansi7 = colorsys.hls_to_rgb(h7, l7 * (0.86 if dark_bg else 1.12), s7)

    return (
        [ansi0] + normal + [ansi7],
        [ansi8] + bright + [fg],
    )


def render(normal, bright, bg_hex, fg_hex):
    names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    out = ["[colors.primary]",
           'background = "%s"' % bg_hex,
           'foreground = "%s"' % fg_hex,
           "", "[colors.normal]"]
    out += ['%s = "%s"' % (n, rgb_to_hex(c)) for n, c in zip(names, normal)]
    out += ["", "[colors.bright]"]
    out += ['%s = "%s"' % (n, rgb_to_hex(c)) for n, c in zip(names, bright)]
    return "\n".join(out) + "\n"


def main():
    scheme_path = os.path.join(CACHE, "colors.json")
    if not os.path.exists(scheme_path):
        sys.exit("ansi-contrast: %s missing, nothing to do" % scheme_path)

    with open(scheme_path) as fh:
        scheme = json.load(fh)
    colors = scheme.get("colors", scheme)

    bg = colors["m3surface"]
    fg = colors["m3onSurface"]
    accent = colors.get("m3primary", fg)

    normal, bright = build(bg, fg, accent)

    target = os.path.join(CACHE, "colors-alacritty.toml")
    with open(target, "w") as fh:
        fh.write(render(normal, bright, bg, fg))

    # Keep the shell-sourced palette and the OSC sequences in step, so anything
    # that reads them (tty, scripts, `source colors.sh`) gets the same colours.
    seq_path = os.path.join(CACHE, "sequences")
    if os.path.exists(seq_path):
        flat = [rgb_to_hex(c) for c in normal] + [rgb_to_hex(c) for c in bright]
        with open(seq_path, "w") as fh:
            for i, hexcode in enumerate(flat):
                fh.write("\033]4;%d;%s\033\\" % (i, hexcode))
            fh.write("\033]10;%s\033\\" % fg)
            fh.write("\033]11;%s\033\\" % bg)

    sh_path = os.path.join(CACHE, "colors.sh")
    if os.path.exists(sh_path):
        text = open(sh_path).read()
        flat = [rgb_to_hex(c) for c in normal] + [rgb_to_hex(c) for c in bright]
        for i, hexcode in enumerate(flat):
            text = re.sub(r"^color%d=.*$" % i, "color%d='%s'" % (i, hexcode),
                          text, flags=re.M)
        open(sh_path, "w").write(text)

    print("ansi-contrast: rebuilt 16 ANSI colours (bg %s, accent %s)" % (bg, accent))


if __name__ == "__main__":
    main()
