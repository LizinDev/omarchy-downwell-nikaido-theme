# Downwell Nikaido

A dark theme for [Omarchy](https://omarchy.org) 4 (Quattro) in
[Downwell](https://downwellgame.com)'s "Nikaido" palette: an olive-black field, white,
and one gunboot orange. An unofficial fan theme; Downwell is by Moppin, published by
Devolver Digital.

The game draws everything in three colors and nothing in between, so the theme does too
wherever it can: a solid orange window border with square corners and a hard, unblurred
drop shadow, opaque menus, and the chosen row framed in orange the way the game boxes
its selection. Its sister theme, [Downwell](https://github.com/LizinDev/omarchy-downwell-theme),
uses the game's original black/white/red palette.

![preview](preview.png)

## Install

```bash
omarchy theme install https://github.com/LizinDev/omarchy-downwell-nikaido-theme.git
```

## Palette

| Role | Hex | |
|---|---|---|
| background | `#1a1a0c` | the palette's olive-black: terminals, bar, popups, menus |
| foreground | `#e8e7da` | body text, 14.10:1 on background |
| bright_foreground | `#fefefe` | the palette's white: cursor, sprites |
| accent | `#fe9300` | the palette's orange: borders, selected rows, shortcuts |
| selection | `#3d3417` | text selection, btop meters |
| muted | `#5f5e52` | ANSI bright-black, dividers (the palette's `#58584d`, lifted a step) |

ANSI: `#f5453a` red · `#86bb45` green · `#e9c54e` yellow · `#4a8ff0` blue ·
`#d465b9` magenta · `#4cbfbf` cyan. Downwell has no other hues, so these were placed by
hue and kept a notch below the accent's saturation: the orange stays the loudest thing on
screen, as in the source image, where it is the only color that is not black or white.

The accent and `red` (wrong-password border, error text) sit 47.0 dE apart.

## What's here

| File | |
|---|---|
| `colors.toml` | the palette, which generates 17 app configs on its own |
| `hyprland.lua` | solid orange border, square corners, hard offset shadow |
| `shell.{menu,launcher,tooltip,lock}.toml` | opaque cards, orange selection frame, darker scrim |
| `icons.theme` | `Yaru-dark` (Yaru's own accent is orange) |
| `backgrounds/` | see below |
| `preview.png` | theme-switcher tile, a pixel-art palette specimen |
| `unlock.png` | Plymouth boot splash and SDDM logo |
| `tools/` | the scripts that build the backgrounds, previews and shell overrides |

## Backgrounds

Only `4-dither.png` ships: the palette's three bands joined by ordered dither, generated
from `colors.toml`. The other six are built from Downwell's own art and stay local. Every
one uses exactly the theme's three colors:

| | |
|---|---|
| `1-clouds.png` | the cloud sea and heart balloon, the wallpaper the theme was drawn from, re-rendered in exactly the palette's three colors |
| `2-well.png` | a well shaft built from the game's tiles, enemies, gems and HUD |
| `3-title.png` | the DOWNWELL logo over the opening backdrop |
| `5-bros.png` | Super Welltaro Bros.: World 1-1 with gem ? blocks, a slime Goomba, a turtle Koopa and the stone well as the warp pipe |
| `6-terra.png` | Terrawell: a Terraria-style cross-section with the bucket well, the shopkeeper as the Guide, a torchlit tunnel, gem ore and a hotbar |
| `7-isaac.png` | The Welling of Isaac: a basement room with four doors, bubble tears at a fly swarm, a heart pedestal, a tinted gem rock and the minimap |

With your own copy of the game (Steam) and the Omarchywell project checked out at
`~/Projects/Downwell`, rebuild them from `colors.toml`:

```bash
tools/build-backgrounds.sh ~/Projects/Downwell/Wallpaper.png   # omit the argument to skip 1-clouds
```

The scripts read the game's sprites read-only through Omarchywell's
`tools/game_sprites.py`, swap black/white/red for this theme's background, white and
accent (the game's secondary blues and greens fold into the accent or the white), and
scale them 4× on an integer pixel grid.

## Caveats

**Installed from a git clone, this theme loses `hyprland.lua`.** Omarchy drops every
`.lua`, terminal config and `vscode.json` from a cloned theme. The palette and border
color survive (they live in `colors.toml`), but not the square corners and hard shadow.

**`shell.*.toml` overrides replace their whole section.** Their hex values are frozen
copies of `colors.toml`. After changing the palette, apply the theme, run
`python3 tools/shell-overrides.py`, then `omarchy theme refresh`.

## Working on it

Keep the repo outside `~/.config/omarchy/themes` and symlink it in. Omarchy treats a
directory with `.git` inside as a cloned theme and stages it with restrictions; it
never treats a symlink that way.

```bash
ln -s ~/Projects/omarchy-downwell-nikaido-theme ~/.config/omarchy/themes/downwell-nikaido
omarchy theme set downwell-nikaido
```
