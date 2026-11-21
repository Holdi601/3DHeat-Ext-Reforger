"""
Which worlds of the install are extracted: `status [--json]`, `all`, and the manifest every export records.

A **map** is a world with a world file of its own (`worlds/<World>/<World>.ent`) and a terrain of at least 2 km, outside
the editor's slot worlds: Everon (`Eden`), Arland, Kolguyev (`Cain`) and whatever newer maps an update or DLC brings.
The rest (editor slots, test and showcase worlds) are listed as `test` and exported only with `--all-worlds`.

A world's fingerprint is the SHA-1 of its archives' directory rows for every file under `worlds/<World>/` (path,
archive, offset, sizes): it changes when an update changes any of the world's files, and costs no file reads.
`status` compares it with `<levels>/arma-reforger/manifest.json` (see `manifest.py`).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from . import __version__

PROG = "heat3d-reforger-maps"
GAME = "arma-reforger"
#: Bumped whenever a level written by an older version should be written again (`status` calls it outdated).
LEVEL_FORMAT = 2  # 2: levels with layouts and a manifest entry
#: The real names of the maps whose world folder has a working name.
MAP_NAMES = {"eden": "Everon", "arland": "Arland", "cain": "Kolguyev"}


def levels_folder(args, install: Path) -> Path:
    from heat3d_gamefiles import levelshome

    if getattr(args, "levels", None):
        return Path(args.levels)
    home = levelshome.home(levelshome.game_folder(install))
    return home if home is not None else Path(GAME)


def worlds(fs) -> list[dict]:
    """Every world with a terrain: id, terrain, size, whether it is a map, and its sources."""
    from .enfusionworld import list_worlds, terrain_header, world_file

    out = []
    for world, terr in list_worlds(fs):
        try:
            xs, zs, _b, _n, spacing, _s, _o = terrain_header(fs.read(terr))
            size = max(xs, zs) * spacing
        except Exception:  # noqa: BLE001 - an unreadable terrain is listed, not fatal
            size = 0.0
        has_world = world_file(fs, world) is not None
        kind = "map" if has_world and size >= 2000 and not world.lower().startswith("editor/") else "test"
        stem = world.rsplit("/", 1)[-1]
        out.append({"id": world.replace("/", "_"), "world": world, "terrain": terr, "size": round(size),
                    "kind": kind, "name": MAP_NAMES.get(stem.lower(), stem), "sources": sources(fs, world)})
    # two worlds can share a folder (two terrains): keep the first of an id
    seen, unique = set(), []
    for w in out:
        if w["id"] not in seen:
            seen.add(w["id"])
            unique.append(w)
    return unique


def sources(fs, world: str) -> list[dict]:
    prefix = f"worlds/{world.lower()}/"
    by_archive: dict[Path, list] = {}
    for path, entry in fs.files.items():
        if path.startswith(prefix):
            by_archive.setdefault(entry.archive, []).append((path, entry.offset, entry.stored, entry.size))
    out = []
    for archive, rows in sorted(by_archive.items()):
        h = hashlib.sha1()
        for row in sorted(rows):
            h.update(repr(row).encode())
        out.append({"path": str(archive), "hash": h.hexdigest()})
    return out


def game_build(install: Path) -> str:
    import re

    for lib in (install.parent.parent,):
        try:
            text = (lib / "appmanifest_1874880.acf").read_text(encoding="utf-8", errors="replace")
            m = re.search(r'"buildid"\s+"(\d+)"', text)
            if m:
                return m.group(1)
        except OSError:
            pass
    import time

    exe = next((p for p in (install / "ArmaReforgerSteam.exe", install / "ArmaReforger.exe") if p.is_file()), None)
    return time.strftime("%Y-%m-%d", time.gmtime(exe.stat().st_mtime)) if exe else "unknown"


def record(install: Path, fs, world: str, files: list[Path], folder: Path, **extra) -> None:
    from .manifest import record as write

    w = next((x for x in worlds(fs) if x["world"].lower() == world.lower()), None)
    write(folder, GAME, PROG, __version__, LEVEL_FORMAT, world.replace("/", "_"), build=game_build(install),
          sources=sources(fs, world), files=files, world=world, name=(w or {}).get("name", world), **extra)


def _open(args):
    from .enfusion import FileSystem, find_install

    install = find_install(args.install)
    if install is None:
        print("Arma Reforger not found; pass --install <game folder>", file=sys.stderr)
        return None, None
    return install, FileSystem.of_install(install)


def cmd_status(args) -> int:
    from .enfusion import find_install
    from .manifest import manager_status, status

    if args.json and find_install(args.install) is None:  # the extractors manager wants an answer, not an error
        print(json.dumps(manager_status(GAME, "Arma Reforger", None, [], __version__, Path(args.levels or GAME)), indent=1))
        return 0
    install, fs = _open(args)
    if install is None:
        return 2
    folder = levels_folder(args, install)
    every = worlds(fs)
    listed = [w for w in every if args.all_worlds or w["kind"] == "map"]
    rows = status(folder, listed, LEVEL_FORMAT)
    tests = [w["id"] for w in every if w["kind"] != "map"]
    if args.json:
        doc = manager_status(GAME, "Arma Reforger", game_build(install), rows, __version__, folder)
        doc.update(install=str(install), extractor=f"{PROG} {__version__}", levelFormat=LEVEL_FORMAT,
                   worlds=rows, testWorlds=[] if args.all_worlds else tests)
        print(json.dumps(doc, indent=1))
        return 0
    print(f"Arma Reforger at {install} (build {game_build(install)}); levels in {folder}")
    for r in rows:
        print(f"  {r['state']:<9} {r['id']:<28} {r.get('name', ''):<12} {r['why']}")
    if tests and not args.all_worlds:
        print(f"  ({len(tests)} test and editor worlds not listed: --all-worlds)")
    todo = [r for r in rows if r["state"] in ("new", "changed", "outdated", "missing")]
    print(f"{len(todo)} to extract: {PROG} all" if todo else "every map is extracted and current")
    return 0


def export_one(install: Path, fs, w: dict, folder: Path, args, log=print) -> int:
    from .enfusion import EnfusionError
    from .enfusionworld import export_world

    from . import layouts

    folder.mkdir(parents=True, exist_ok=True)
    out = folder / f"{w['id']}.glb"
    spacing = args.ground_spacing
    if spacing is None:  # the large maps at 4 m: a level a browser tab still loads whole
        spacing = 2.0 if w["size"] <= 8192 else 4.0
    try:
        report = export_world(install, w["world"], out, ground_spacing=spacing, texture=args.texture_size,
                              structures=not args.no_structures, trees=args.trees, log=log)
    except (LookupError, EnfusionError, OSError) as exc:
        print(f"{w['id']}: not exported: {exc}", file=sys.stderr)
        return 1
    files = [out]
    try:
        doc = layouts.build(install, fs, w["world"])
        lpath = folder / f"{w['id']}.layouts.json"
        lpath.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        files.append(lpath)
        places = {lay["id"]: len(lay["objectives"]) + len(lay["spawns"]) for lay in doc["layouts"]}
    except Exception as exc:  # noqa: BLE001 - layouts never cost the level
        places = {"error": str(exc)}
    record(install, fs, w["world"], files, folder, groundSpacing=spacing, structures=report.structures)
    log(f"{w['id']} -> {out}: {report.ground_triangles:,} ground triangles at {spacing:g} m, "
        f"{report.structures:,} structure boxes, {report.water_triangles:,} water triangles; layouts {places}")
    return 0


def cmd_all(args) -> int:
    from .manifest import status

    install, fs = _open(args)
    if install is None:
        return 2
    folder = levels_folder(args, install)
    listed = [w for w in worlds(fs) if args.all_worlds or w["kind"] == "map"]
    rows = {r["id"]: r for r in status(folder, listed, LEVEL_FORMAT)}
    worst = 0
    todo = [w for w in listed if args.force or rows[w["id"]]["state"] in ("new", "changed", "outdated", "missing")]
    for w in todo:
        worst = max(worst, export_one(install, fs, w, folder, args))
    if not todo:
        print("every map is extracted and current")
    return worst


def cmd_extract(args) -> int:
    """The extractors manager's verb: maps by state (--new, --changed, --outdated) or by id, one JSON line each."""
    from .manifest import Progress, pick, status

    progress = Progress(args.progress_json)
    if args.game and args.game != GAME:
        progress.fail(f"no game {args.game!r} here; this tool reads {GAME}")
        return 2
    install, fs = _open(args)
    if install is None:
        progress.fail("Arma Reforger not found")
        return 2
    folder = levels_folder(args, install)
    listed = [w for w in worlds(fs) if args.all_worlds or w["kind"] == "map"]
    rows = status(folder, listed, LEVEL_FORMAT)
    try:
        chosen = pick(rows, args.maps, new=args.new, changed=args.changed, outdated=args.outdated)
    except LookupError as exc:
        progress.fail(str(exc))
        return 2
    by_id = {w["id"]: w for w in listed}
    progress.start(len(chosen))
    for i, map_id in enumerate(chosen):
        try:
            code = export_one(install, fs, by_id[map_id], folder, args)
            progress.map(i, map_id, code == 0, "" if code == 0 else "not exported")
        except Exception as exc:  # noqa: BLE001 - one map failing never stops the others
            progress.map(i, map_id, False, str(exc))
    return progress.done()


def cmd_layouts(args) -> int:
    from . import layouts

    install, fs = _open(args)
    if install is None:
        return 2
    folder = levels_folder(args, install)
    folder.mkdir(parents=True, exist_ok=True)
    try:
        from .enfusionworld import find_world

        world, _terr = find_world(fs, args.world)
    except LookupError as exc:
        print(exc, file=sys.stderr)
        return 2
    doc = layouts.build(install, fs, world)
    out = folder / f"{world.replace('/', '_')}.layouts.json"
    out.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    for lay in doc["layouts"]:
        print(f"  {lay['id']:<32} {len(lay['objectives']):>4} places/objectives, {len(lay['spawns']):>4} spawns")
    print(f"-> {out}")
    return 0


def add_verbs(sub) -> None:
    common = [("--install", dict(type=Path, default=None, help="the game's folder, if not in a Steam library")),
              ("--levels", dict(default=None, help="the levels folder (default $HEAT3D_LEVELS/arma-reforger, else ./arma-reforger)")),
              ("--all-worlds", dict(action="store_true", help="also the editor, test and showcase worlds"))]
    p = sub.add_parser("status", help="every map: new, changed, outdated, missing, current or removed")
    p.add_argument("--json", action="store_true", help="as JSON, for the extractors manager")
    for flag, kw in common:
        p.add_argument(flag, **kw)
    p.set_defaults(run=cmd_status)
    p = sub.add_parser("all", help="every map status does not call current: level, layouts, manifest entry")
    for flag, kw in common:
        p.add_argument(flag, **kw)
    p.add_argument("--force", action="store_true", help="every map, current or not")
    p.add_argument("--ground-spacing", type=float, default=None, metavar="METRES",
                   help="terrain vertex spacing (default 2 m, 4 m for maps over 8 km)")
    p.add_argument("--texture-size", type=int, default=4096, metavar="PIXELS")
    p.add_argument("--no-structures", action="store_true")
    p.add_argument("--trees", action="store_true")
    p.set_defaults(run=cmd_all)
    p = sub.add_parser("extract", help="maps by state or id, for the extractors manager")
    p.add_argument("maps", nargs="*", help="map ids, as status lists them")
    for flag, kw in common:
        p.add_argument(flag, **kw)
    p.add_argument("--game", default=None, help="only this game (the extractors manager names it)")
    p.add_argument("--new", action="store_true")
    p.add_argument("--changed", action="store_true")
    p.add_argument("--outdated", action="store_true")
    p.add_argument("--progress-json", action="store_true", help="one JSON line per event (start, map, done)")
    p.add_argument("--ground-spacing", type=float, default=None, metavar="METRES")
    p.add_argument("--texture-size", type=int, default=4096, metavar="PIXELS")
    p.add_argument("--no-structures", action="store_true")
    p.add_argument("--trees", action="store_true")
    p.set_defaults(run=cmd_extract)
    p = sub.add_parser("layouts", help="a world's places, bases, relays and spawns as <World>.layouts.json")
    p.add_argument("world")
    for flag, kw in common[:2]:
        p.add_argument(flag, **kw)
    p.set_defaults(run=cmd_layouts)
