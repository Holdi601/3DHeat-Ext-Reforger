"""
heat3d-reforger-maps worlds   [--install folder]
heat3d-reforger-maps world    <world> [-o world.glb] [--install folder] [--ground-spacing m]
                              [--texture-size px] [--no-structures] [--trees]
heat3d-reforger-maps identify <file>

`worlds` lists the worlds of the installed Arma Reforger that have a terrain,
`world` writes one of them as a `.glb`, `identify` says whether a file is one
of the Enfusion files the tool reads. `enfusion-worlds` and `enfusion-world`
are the same verbs under the names 3DHeat GameFiles gave them; GameFiles runs
this tool with them.

Exit status: 0 done, 1 failed, 2 nothing to read (no install found, no such
world, not an Enfusion file, 3DHeat GameFiles missing); the message says what
to do.
"""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

from . import __version__, library

PROG = "heat3d-reforger-maps"

#: The verbs, and the names 3DHeat GameFiles gave them.
VERBS = {
    "worlds": ("enfusion-worlds", "list the worlds of an installed Arma Reforger"),
    "world": ("enfusion-world", "export an Arma Reforger world: terrain, its colour, the sea, building boxes"),
}


def _identify(path: Path) -> str | None:
    """An Enfusion archive, terrain, terrain tile, world file or texture, described; None for anything else."""
    from .enfusion import EnfusionError, read_directory
    from .enfusionworld import _form_chunks, read_world, terrain_header

    size = path.stat().st_size
    lines = [f"{path.name}  ({size:,} bytes)"]
    with path.open("rb") as handle:
        head = handle.read(160)
    try:
        if head[:4] == b"FORM" and head[8:12] == b"PAC1":
            entries = read_directory(path)
            packed = sum(1 for e in entries.values() if e.method == 1)
            lines.append("  Enfusion archive (.pak)")
            lines.append(f"    files      {len(entries):,}, {packed:,} of them zlib-compressed")
            lines.append(f"    holds      {sum(e.size for e in entries.values()):,} bytes unpacked")
            return "\n".join(lines)
        if head[:4] == b"FORM" and head[8:12] == b"TERR":
            data = path.read_bytes()
            tags = [tag for tag, _ in _form_chunks(data)]
            if b"HEAD" in tags:
                xs, zs, block, blocks, spacing, _scale, _offset = terrain_header(data)
                lines.append("  Enfusion terrain (.terr)")
                lines.append(f"    vertices   {xs:,} x {zs:,}, {spacing:g} m apart")
                lines.append(f"    tiles      {blocks} x {blocks} blocks each, a block {block} x {block} vertices")
                return "\n".join(lines)
            if b"HGHT" in tags:
                lines.append("  Enfusion terrain tile (.ttile)")
                lines.append("    chunks     " + ", ".join(t.decode("latin-1") for t in tags))
                return "\n".join(lines)
            return None
        if head[:4] == b"EBIN":
            world = read_world(path.read_bytes())
            lines.append("  Enfusion binary entity file (a world's .ent)")
            lines.append(f"    entities   {len(world.entities):,}")
            lines.append(f"    resources  {len(world.guids):,} GUIDs, {len(world.names):,} names")
            return "\n".join(lines)
        if head[:4] == b"DDS " and path.suffix.lower() == ".edds" and len(head) >= 148 and head[84:88] == b"DX10":
            height, width = struct.unpack_from("<II", head, 12)
            (mips,) = struct.unpack_from("<I", head, 28)
            (dxgi,) = struct.unpack_from("<I", head, 128)
            mips = max(1, mips)
            with path.open("rb") as handle:
                handle.seek(148)
                records = [struct.unpack("<4sI", handle.read(8)) for _ in range(mips)]
            if 148 + 8 * mips + sum(s for _t, s in records) != size:
                return None
            kinds = sorted({t.decode("latin-1").strip() for t, _s in records})
            lines.append("  Enfusion texture (.edds)")
            lines.append(f"    size       {width} x {height}, {mips} levels, DXGI format {dxgi}")
            lines.append(f"    levels     stored as {', '.join(kinds)}")
            return "\n".join(lines)
    except (EnfusionError, struct.error, IndexError, UnicodeDecodeError):
        return None
    return None


def _identify_verb(args) -> int:
    if not args.path.exists():
        print(f"no such file: {args.path}", file=sys.stderr)
        return 2
    try:
        found = _identify(args.path)
    except OSError as exc:
        print(exc, file=sys.stderr)
        return 1
    if found is None:
        print("not an Arma Reforger file", file=sys.stderr)
        return 2
    print(found)
    return 0


def parser() -> argparse.ArgumentParser:
    """The verbs with exactly the options of GameFiles' `enfusion-worlds` and `enfusion-world`."""
    from . import enfusionworld

    ap = argparse.ArgumentParser(
        prog=PROG,
        description="Arma Reforger worlds (Enfusion) from your own install into 3DHeat levels.",
        epilog="What you point it at is subject to the game's own licence; the levels it writes are for your own use.",
    )
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="verb", required=True)
    # The options are the ones enfusionworld declares, taken from it rather than restated.
    declared = argparse.ArgumentParser().add_subparsers(dest="verb")
    enfusionworld.add_verbs(declared)
    for name, (old, text) in VERBS.items():
        sub.add_parser(name, aliases=[old], help=text, parents=[declared.choices[old]], add_help=False)
    from . import gear

    gear.add_verbs(sub)
    from . import levels

    levels.add_verbs(sub)
    p = sub.add_parser("identify", help="say whether a file is an Enfusion archive, terrain, world file or texture")
    p.add_argument("path", type=Path)
    return ap


def _world_check(args) -> int | None:
    """Exit 2 with what to do when the game or the world is not there; None to go on."""
    from .enfusion import EnfusionError, FileSystem, find_install
    from .enfusionworld import find_world, list_worlds

    install = find_install(args.install)
    if install is None:
        print("Arma Reforger not found; pass --install <game folder>", file=sys.stderr)
        return 2
    try:
        fs = FileSystem.of_install(install)
        if args.verb == "enfusion-worlds":
            print(f"Arma Reforger at {install}: {len(list_worlds(fs))} worlds with a terrain")
        else:
            find_world(fs, args.world)
    except LookupError as exc:
        print(exc, file=sys.stderr)
        return 2
    except EnfusionError as exc:
        print(exc, file=sys.stderr)
        return 1
    return None


def main(argv: list[str] | None = None) -> int:
    if not library.ensure():
        print(library.MISSING, file=sys.stderr)
        return 2
    args = parser().parse_args(argv)
    if args.verb == "identify":
        # A quiet probe: GameFiles asks every installed game tool in turn.
        return _identify_verb(args)
    try:
        from . import update

        update.startup("heat3d_ext_reforger")
    except Exception:  # an update check never stops an export
        pass
    if args.verb in ("catalog", "models", "status", "all", "layouts", "extract"):
        return args.run(args)
    from . import enfusionworld

    args.verb = VERBS.get(args.verb, (args.verb,))[0]
    stop = _world_check(args)
    if stop is not None:
        return stop
    return enfusionworld.run(args)


if __name__ == "__main__":
    sys.exit(main())
