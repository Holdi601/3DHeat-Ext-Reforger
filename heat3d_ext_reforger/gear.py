"""
Arma Reforger's catalogue: every vehicle and weapon prefab of your own install, as `catalog.json`.

Vehicles are the prefabs under `Prefabs/Vehicles/<kind>/<model>/` (not their parts, lights, debris or probes):
each with its model folder, kind (wheeled, tracked, helicopter, boat), the faction its `faction affiliation` names
(followed up the chain of parent prefabs), the model (`.xob`) it is drawn with, and the real vehicle it stands for.
Weapons are the prefabs under `Prefabs/Weapons/` that are weapons (rifles, machine guns, handguns, launchers,
grenades, mortars, heavy and aircraft weapons), with their class. Everything is plain text in the game's archives.
"""

from __future__ import annotations

import re
from pathlib import Path

from .enfusion import EnfusionError, FileSystem

#: Real vehicles by their model folder.
REAL = {
    "brdm2": ("BRDM-2", "ground", "car"), "btr70": ("BTR-70", "ground", "apc"), "lav25": ("LAV-25", "ground", "ifv"),
    "m151a2": ("M151A2", "ground", "car"), "m923a1": ("M923A1", "ground", "truck"), "m998": ("M998 HMMWV", "ground", "car"),
    "mi8mt": ("Mi-8MT", "air", "heli-transport"), "uh1h": ("UH-1H", "air", "heli-transport"),
    "s105": ("Škoda 105", "ground", "car"), "s1203": ("Škoda 1203", "ground", "car"), "t601": ("Trabant 601", "ground", "car"),
    "uaz452": ("UAZ-452", "ground", "car"), "uaz469": ("UAZ-469", "ground", "car"), "ural4320": ("Ural-4320", "ground", "truck"),
    "v2101": ("VAZ-2101", "ground", "car"), "z7211": ("Zetor 7211", "ground", "car"), "bmp1": ("BMP-1", "ground", "ifv"),
    "t72": ("T-72", "ground", "mbt"), "m113": ("M113", "ground", "apc"), "m1025": ("M1025 HMMWV", "ground", "car"),
}
KIND_DOMAIN = {"wheeled": "ground", "tracked": "ground", "helicopters": "air", "planes": "air", "boats": "sea"}
WEAPON_CLASS = {"rifles": "rifle", "machineguns": "lmg", "handguns": "pistol", "launchers": "launcher",
                "grenades": "grenade", "mortars": "mortar", "heavyweapons": "heavy", "aircraftweapons": "aircraft",
                "cannons": "cannon", "explosives": "explosive"}
SKIP_DIRS = re.compile(r"/(VehParts|Lights|Dst|Dbr|Probes|Core|Generic|Conflict_Variants|Attachments)/", re.I)
_PARENT = re.compile(r'^\s*\w+\s*:\s*"(?:\{[0-9A-F]+\})?([^"]+)"', re.M)
_FACTION = re.compile(r'"faction affiliation"\s+"([^"]+)"')
_MODEL = re.compile(r'Object\s+"(?:\{[0-9A-F]+\})?([^"]+\.xob)"')


def _follow(fs: FileSystem, path: str, rx: re.Pattern, depth: int = 0) -> str:
    try:
        text = fs.read(path).decode("utf-8", "replace")
    except (FileNotFoundError, EnfusionError, KeyError):
        return ""
    m = rx.search(text)
    if m:
        return m.group(1)
    parent = _PARENT.search(text)
    if parent and depth < 12:
        return _follow(fs, parent.group(1), rx, depth + 1)
    return ""


def build(fs: FileSystem) -> list[dict]:
    items: list[dict] = []
    for path in sorted(fs.find("Prefabs/Vehicles/", ".et")):
        if SKIP_DIRS.search(path) or path.count("/") != 4:
            continue
        _p, _v, kind, folder, file = path.split("/")
        stem = file[:-3]
        if re.search(r"_base$|tutorial|broken", stem, re.I):
            continue
        real = REAL.get(folder.lower())
        key, domain, cls = real if real else (folder, KIND_DOMAIN.get(kind.lower(), "ground"), "vehicle")
        variant = stem[len(folder):].strip("_").replace("_", " ") if stem.lower().startswith(folder.lower()) else stem
        items.append({
            "id": stem, "kind": "vehicle", "name": f"{key} {variant}".strip() if variant else key, "class": cls,
            "domain": domain, "nation": _follow(fs, path, _FACTION), "key": key, "prefab": path,
            "shape": _follow(fs, path, _MODEL),
        })
    for path in sorted(fs.find("Prefabs/Weapons/", ".et")):
        parts = path.split("/")
        cls = WEAPON_CLASS.get(parts[2].lower()) if len(parts) > 3 else None
        if not cls or SKIP_DIRS.search(path) or re.search(r"_base$|base_", parts[-1][:-3], re.I):
            continue
        stem = parts[-1][:-3]
        name = re.sub(r"^(Rifle|MG|Handgun|Launcher|Grenade|Mortar|Weapon)_", "", stem).replace("_", " ")
        items.append({"id": stem, "kind": "weapon", "name": name, "class": cls, "nation": _follow(fs, path, _FACTION),
                      "key": name, "prefab": path})
    return items


def game_build(install: Path) -> str:
    import time

    exe = next((p for p in (install / "ArmaReforgerSteam.exe", install / "ArmaReforger.exe") if p.is_file()), None)
    return time.strftime("%Y-%m-%d", time.gmtime(exe.stat().st_mtime)) if exe else "unknown"


def cmd_models(args) -> int:
    """Every catalogued vehicle as a local model pack: `<levels>/model-packs/arma-reforger/`."""
    import hashlib
    import os
    import time

    from . import __version__
    from .enfusion import find_install
    from .modelpack import Pack
    from .prefab import Chain
    from .vehicles import Builder, geometry_key, merged_parts

    install = find_install(args.game)
    if install is None:
        print("no Arma Reforger install found: give it with --game <folder>", flush=True)
        return 2
    lv = args.out or os.environ.get("HEAT3D_LEVELS")
    if not lv:
        print("no output folder: pass --out <levels folder> or set HEAT3D_LEVELS", flush=True)
        return 2
    fs = FileSystem.of_install(install)
    t0 = time.monotonic()
    items = [it for it in build(fs) if it["kind"] == "vehicle"]
    if args.only:
        items = [it for it in items if any(o.lower() in it["id"].lower() for o in args.only)]
    pack = Pack(Path(lv) / "model-packs" / "arma-reforger", "arma-reforger", game_build(install),
                f"heat3d-reforger-maps {__version__}")
    builder = Builder(fs)
    print(f"arma-reforger: {len(items)} vehicles", flush=True)
    shared: dict[str, str] = {}
    done = same = failed = 0
    for it in items:
        chain = Chain(fs, it["prefab"])
        fp = hashlib.sha256("\n".join(chain.texts).encode()).hexdigest()[:20]
        if not args.force and pack.fresh(it["id"], fp):
            same += 1
            continue
        try:
            b = builder.build(it["prefab"])
            key = geometry_key(b)
            if key in shared and shared[key] in pack.index["units"]:
                owner = pack.index["units"][shared[key]]
                owner["aliases"] = sorted(set(owner.get("aliases", [])) | {it["id"]})
                pack.index["units"].pop(it["id"], None)
                same += 1
                continue
            pivots = {k: [round(float(x), 4) for x in v] for k, v in b.pivots.items() if not k.startswith("_")}
            e = pack.add(it["id"], merged_parts(b), it["domain"], it["class"], key=it["key"], pivots=pivots,
                         dm=b.dm, fingerprint=fp,
                         extra={"name": it["name"], "nation": it.get("nation", ""), "prefab": it["prefab"]})
            shared[key] = it["id"]
            done += 1
            print(f"  {it['id']}: {e['parts']} {e['tris']} tris, dm {e['dm']}, "
                  f"{e['length']} x {e['width']} x {e['height']} m", flush=True)
        except Exception as exc:  # noqa: BLE001 - one vehicle never stops the rest
            failed += 1
            print(f"  {it['id']}: FAILED {exc}", flush=True)
    for u in list(pack.index["units"]):
        e = pack.index["units"][u]
        e["aliases"] = sorted(a for a in e.get("aliases", []) if a != u)
    pack.save()
    print(f"arma-reforger: {done} written, {same} unchanged or shared, {failed} failed; {pack.bytes / 1e6:.1f} MB; "
          f"{time.monotonic() - t0:.0f} s -> {pack.index_path}")
    return 1 if failed and not done else 0


def cmd_catalog(args) -> int:
    import json
    import os
    import time

    from . import __version__
    from .enfusion import find_install

    install = find_install(args.game)
    if install is None:
        print("no Arma Reforger install found: give it with --game <folder>", flush=True)
        return 2
    fs = FileSystem.of_install(install)
    lv = os.environ.get("HEAT3D_LEVELS")
    out = Path(args.out) if args.out else (Path(lv) / "arma-reforger" / "catalog.json" if lv else Path("catalog.json"))
    t0 = time.monotonic()
    items = build(fs)
    pack = out.parent.parent / "model-packs" / "arma-reforger" / "model-pack.json"
    if pack.is_file():
        units = json.loads(pack.read_text(encoding="utf-8")).get("units", {})
        files = {a: e["file"] for u, e in units.items() for a in [u, *e.get("aliases", [])]}
        for it in items:
            if it["id"] in files:
                it["model"] = f"model-packs/arma-reforger/{files[it['id']]}"
    build_id = game_build(install)
    doc = {"format": "3dheat-catalog", "version": 1, "game": "arma-reforger", "gameBuild": build_id,
           "source": f"heat3d-reforger-maps {__version__}", "items": sorted(items, key=lambda i: (i["kind"], i["id"]))}
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.part")
    tmp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(out)
    kinds: dict[str, int] = {}
    for it in items:
        kinds[it["kind"]] = kinds.get(it["kind"], 0) + 1
    print(f"{len(items)} items {kinds} in {time.monotonic() - t0:.0f} s -> {out}")
    return 0


def add_verbs(sub) -> None:
    p = sub.add_parser("catalog", help="every vehicle and weapon prefab of your install -> catalog.json")
    p.add_argument("-o", "--out", help="the .json to write (default <HEAT3D_LEVELS>/arma-reforger/catalog.json)")
    p.add_argument("--game", help="the Arma Reforger folder")
    p.set_defaults(run=cmd_catalog)
    p = sub.add_parser("models", help="every catalogued vehicle's model -> a local model pack for the viewer")
    p.add_argument("-o", "--out", help="the levels folder (default HEAT3D_LEVELS); the pack goes to "
                                       "<out>/model-packs/arma-reforger/")
    p.add_argument("--game", help="the Arma Reforger folder")
    p.add_argument("--only", nargs="*", help="only vehicles whose id contains one of these")
    p.add_argument("--force", action="store_true", help="write every vehicle again, even unchanged ones")
    p.set_defaults(run=cmd_models)
