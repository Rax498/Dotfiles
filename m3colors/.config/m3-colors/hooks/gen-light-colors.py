#!/home/rax/.local/share/pipx/venvs/m3wal/bin/python
"""Force-generate a real *light* Material 3 scheme for the current wallpaper.

m3wal only ever computes one scheme per run (whichever `mode` -- light or
dark -- config.mode=auto picks from wallpaper brightness) and writes it to
colors.scss. The eww "-light" stylesheets assume a separate light palette
exists, but previously they imported that same colors.scss, so switching to
the light theme just inherited whatever the last run happened to generate
(usually dark). This script bypasses m3wal's cache (which is keyed by
wallpaper+variant only, not mode, so it can't be trusted to hold a light
scheme) and builds the light scheme directly, writing colors-light.scss
alongside the normal colors.scss. The normal dark/auto pipeline is untouched.
"""
import shutil
from pathlib import Path

from PIL import Image
from material_color_utilities import Variant, hex_from_argb, theme_from_image

from m3wal.m3wal import M3WAL

VARIANT_MAP = {
    "TONALSPOT": Variant.TONALSPOT,
    "VIBRANT": Variant.VIBRANT,
    "EXPRESSIVE": Variant.EXPRESSIVE,
    "NEUTRAL": Variant.NEUTRAL,
    "FIDELITY": Variant.FIDELITY,
    "CONTENT": Variant.CONTENT,
    "MONOCHROME": Variant.MONOCHROME,
}


def main():
    wallpaper = Path("~/.config/m3-colors/current_wallpaper").expanduser().resolve()
    cache_dir = Path("~/.cache/m3-colors").expanduser()
    templates_dir = Path("~/.config/m3-colors/templates").expanduser()

    m3 = M3WAL(str(wallpaper))
    variant_name = m3.config.get("General", "variant", fallback="CONTENT").upper()
    variant_enum = VARIANT_MAP.get(variant_name, Variant.CONTENT)

    # Build the theme directly -- skip generate_scheme()'s cache lookup,
    # since the cache key doesn't include mode and would happily hand back
    # a stale dark-mode result.
    img = Image.open(wallpaper)
    m3.theme = theme_from_image(img, 0, variant_enum)
    m3.source_color = m3.theme.source
    m3.mode = "light"

    colors = m3._extract_colors()
    colors["wallpaper_path"] = str(wallpaper)
    colors["mode"] = "light"
    colors["source_color"] = (
        hex_from_argb(m3.source_color)
        if isinstance(m3.source_color, int)
        else m3.source_color
    )

    out_path = cache_dir / "colors-light.scss"
    m3.apply_template(templates_dir / "colors.scss.template", out_path, colors=colors)
    print(f"[gen-light-colors] wrote {out_path}")

    # Deploy straight to eww's config dir too. This runs from m3wal-post.sh,
    # which fires *after* deploy_configs() already ran for this cycle, so
    # relying on deploy.json alone would leave this one wallpaper-switch
    # behind.
    eww_dest = Path("~/.config/eww/colors-light.scss").expanduser()
    if eww_dest.parent.exists():
        shutil.copy2(out_path, eww_dest)
        print(f"[gen-light-colors] deployed -> {eww_dest}")


if __name__ == "__main__":
    main()
