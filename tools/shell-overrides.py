#!/usr/bin/env python3
"""Write this theme's shell.<section>.toml overrides.

    python3 tools/shell-overrides.py

A section override REPLACES the whole generated section, so each file restates
every key Omarchy generated and changes only the ones listed in OVERRIDES. Run
this after editing colors.toml. It renders the installed templates from the
palette in a temporary home so existing shell overrides cannot mask changes.
"""
import os
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

THEME = Path(__file__).resolve().parent.parent

# Downwell's interface: opaque cards, a solid accent frame around the chosen
# row (the game's selection box), and a heavier scrim.
SELECTED = {
    'background-alpha': 1.0,
    'scrim': '{darker_background}',
    'scrim-alpha': 0.6,
    'selected-background': '{accent}',
    'selected-background-alpha': 0.14,
    'selected-text': '{accent}',
    'selected-border': '{accent}',
    'selected-border-alpha': 1.0,
    'selected-border-width': 2,
}
OVERRIDES = {
    'menu': SELECTED,
    'launcher': SELECTED,
    'tooltip': {'background-alpha': 1.0},
    # Idle field sits on the muted grey; typing lights the accent frame.
    'lock': {'background-alpha': 0.9, 'border': '{muted}'},
}


def palette():
    keys = {}
    for line in (THEME / 'colors.toml').read_text().splitlines():
        m = re.match(r'\s*([A-Za-z0-9_-]+)\s*=\s*"([^"]*)"', line)
        if m:
            keys[m.group(1)] = m.group(2)
    return keys


def render_stock_shell():
    with TemporaryDirectory() as home:
        state = Path(home) / '.local/state'
        stage = state / 'omarchy/current/next-theme'
        stage.mkdir(parents=True)
        shutil.copyfile(THEME / 'colors.toml', stage / 'colors.toml')
        env = dict(os.environ, HOME=home, XDG_STATE_HOME=str(state),
                   OMARCHY_PATH=os.environ.get('OMARCHY_PATH', '/usr/share/omarchy'))
        subprocess.run(['omarchy-theme-set-templates'], env=env, check=True)
        return (stage / 'shell.toml').read_text()


def sections(text):
    found, name = {}, None
    for line in text.splitlines():
        m = re.match(r'^\s*\[([^\]]+)\]', line)
        if m:
            name = m.group(1)
            found[name] = []
        elif name:
            found[name].append(line)
    return found


def literal(value):
    if isinstance(value, str):
        return '"%s"' % value
    return repr(value)


def main():
    slug = 'downwell-nikaido'
    colors = palette()
    generated = sections(render_stock_shell())
    for section, changes in OVERRIDES.items():
        lines, done = [], set()
        for line in generated[section]:
            m = re.match(r'^(\s*)([a-z-]+)(\s*=\s*)(.*)$', line)
            if m and m.group(2) in changes:
                value = changes[m.group(2)]
                if isinstance(value, str):
                    value = value.format(**colors)
                lines.append(m.group(1) + m.group(2) + m.group(3) + literal(value))
                done.add(m.group(2))
            else:
                lines.append(line)
        while lines and not lines[-1].strip():
            lines.pop()
        width = max((len(m.group(1)) for m in (re.match(r'^\s*([a-z-]+)\s*=', l) for l in lines) if m), default=0)
        for key in changes:
            if key not in done:
                value = changes[key]
                if isinstance(value, str):
                    value = value.format(**colors)
                lines.append(f'{key:<{width}} = {literal(value)}')
        header = [
            f'# {slug} override for [{section}], written by tools/shell-overrides.py.',
            '# A section override REPLACES the whole section, so every generated key is',
            '# restated; hex values are frozen copies of colors.toml - re-run the tool',
            '# after any palette change.',
        ]
        (THEME / f'shell.{section}.toml').write_text('\n'.join(header + lines) + '\n')
        print(f'shell.{section}.toml')


main()
