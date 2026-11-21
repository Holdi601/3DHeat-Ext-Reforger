"""
A world's places and its scenarios' objectives as `<World>.layouts.json`.

* Layout `world`: the map's named places, the entities of `Prefabs/World/Locations/...` in the world file. Each
  is named by its map label (`#AR-MapLocation_<Name>` in the English string table, `Language/localization.en_us.conf`)
  and typed by its map descriptor's `MainType` up its prefab chain: cities, towns, villages and settlements are
  `town`; airports `airfield`; military bases and hospitals `base` kind `military`; hills, bays, lakes, harbours,
  castles and the rest `place` with their kind.
* One layout per scenario world built on the map (`worlds/MP/CTI_Campaign_<World>.ent` - Conflict -, combat ops,
  Game Master, capture and hold): its military bases (`base`, airbases as `airfield`), radio relays (`objective`
  kind `relay`), supply caches and named location compositions (`objective`), capture areas (`capture_zone`) and
  spawn points (`spawn`; ambient patrol and vehicle spawns with rule `ambient`), each with its faction and team
  (1 US, 2 USSR, 3 FIA).

Positions are the level's own frame - the game's metres, x east, y up, z north - the same as `<World>.glb`. Only
entities placed at the top of a world are read: what sits inside a composition is placed relative to it.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import __version__

_PARENT = re.compile(r'^\s*\w+\s*:\s*"(?:\{[0-9A-F]+\})?([^"]+)"', re.M)
_DISPLAY = re.compile(r'DisplayName\s+"([^"]*)"')
_MAINTYPE = re.compile(r'MainType\s+"([^"]*)"')
_QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
TEAMS = {"US": 1, "USSR": 2, "FIA": 3}
TOWN_TYPES = {"name city": "city", "name town": "town", "name village": "village", "name settlement": "settlement",
              "city": "city", "town": "town", "village": "village", "settlement": "settlement"}


def string_table(fs) -> dict[str, str]:
    """English texts by id from the text string table (parallel `Ids` and text lists)."""
    path = next((p for p in fs.names.values() if p.lower() == "language/localization.en_us.conf"), None)
    if path is None:
        return {}
    text = fs.read(path).decode("utf-8", "replace")
    blocks: list[tuple[str, list[str]]] = []
    for m in re.finditer(r"^ (\w+) \{\n(.*?)^ \}", text, re.M | re.S):
        blocks.append((m.group(1), [s.replace('\\"', '"') for s in _QUOTED.findall(m.group(2))]))
    ids = next((v for k, v in blocks if k.lower() == "ids"), None)
    if not ids:
        return {}
    texts = next((v for k, v in blocks if k.lower() != "ids" and len(v) == len(ids)), None)
    return dict(zip(ids, texts)) if texts else {}


class _Prefabs:
    def __init__(self, fs) -> None:
        self.fs = fs
        self.cache: dict[str, tuple[str, str, list[str]]] = {}

    def info(self, path: str) -> tuple[str, str, list[str]]:
        """(display name, main type, chain of prefab paths) of a prefab, following its parents."""
        if path in self.cache:
            return self.cache[path]
        display = main = ""
        chain: list[str] = []
        cur = path
        for _ in range(12):
            if not cur or cur in chain:
                break
            chain.append(cur)
            try:
                text = self.fs.read(cur).decode("utf-8", "replace")
            except (FileNotFoundError, KeyError, Exception):  # noqa: BLE001 - a missing parent ends the chain
                break
            if not display:
                m = _DISPLAY.search(text)
                display = m.group(1) if m else ""
            if not main:
                m = _MAINTYPE.search(text)
                main = m.group(1) if m else ""
            parent = _PARENT.search(text)
            cur = parent.group(1) if parent else ""
        self.cache[path] = (display, main, chain)
        return self.cache[path]


def _label(key: str, strings: dict[str, str]) -> str:
    key = key.lstrip("#")
    return strings.get(key, "") if key.startswith("AR-") else key


def _pretty(name: str) -> str:
    """`G_HuntsmansHeath` -> `Huntsmans Heath`, `C_LocationGravette` -> `Gravette`."""
    name = re.sub(r"^[A-Z]_(Location_?)?", "", name)
    name = name.replace("_", " ")
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name).strip()


def _name_of(entity_name: str | None, prefab_display: str, shared: bool, strings: dict[str, str]) -> str:
    if entity_name:
        stem = re.sub(r"^[A-Z]_(Location_?)?", "", entity_name)
        for key in (stem, stem.replace("_", "")):
            text = strings.get(f"AR-MapLocation_{key}")
            if text:
                return text
    if prefab_display and not shared:
        text = _label(prefab_display, strings)
        if text:
            return text
    return _pretty(entity_name) if entity_name else _label(prefab_display, strings)


def _faction(path: str) -> str:
    m = re.search(r"_(USSR|US|FIA|RNGD)(?:_|\.|$)", path)
    return m.group(1) if m else ""


def _p(e) -> list[float] | None:
    c = e.props.get("coords")
    if not (isinstance(c, tuple) and len(c) == 3):
        return None
    return [round(float(v), 2) for v in c]


def _heading(e) -> float:
    a = e.props.get("angles")
    return round(float(a[1]) % 360, 1) if isinstance(a, tuple) and len(a) == 3 else 0.0


def places(fs, guids: dict[str, str], world, strings: dict[str, str]) -> list[dict]:
    prefabs = _Prefabs(fs)
    rows = []
    uses: dict[str, int] = {}
    for e in world.entities:
        path = guids.get((e.prefab or "").upper(), e.prefab or "")
        if e.parent is None and path.startswith("Prefabs/World/Locations/"):
            uses[path] = uses.get(path, 0) + 1
            rows.append((e, path))
    out = []
    for e, path in rows:
        pos = _p(e)
        if pos is None:
            continue
        display, main, chain = prefabs.info(path)
        # the kind is the shared ancestor's (Locations/Common/...), never words in the place's own prefab name
        common = [p for p in chain if "/locations/common/" in p.lower()]
        kinds = " ".join(common).lower()
        main_l = main.lower()
        name = _name_of(e.name, display, uses[path] > 1, strings) or _pretty(re.sub(r"_\d+$", "", Path(path).stem))
        entry = {"name": name, "position": pos}
        if main_l in TOWN_TYPES or any(k in kinds for k in ("urbancity", "urbantown", "urbanvillage", "urbansettlement")):
            kind = TOWN_TYPES.get(main_l) or next(v for k, v in (("urbancity", "city"), ("urbantown", "town"),
                                                               ("urbanvillage", "village"), ("urbansettlement", "settlement")) if k in kinds)
            entry.update(type="town", kind=kind)
        elif "airport" in kinds or "airfield" in kinds:
            entry.update(type="airfield", team=None, kind="airport")
        elif "militaryhospital" in kinds:
            entry.update(type="base", team=None, kind="military-hospital")
        elif "militarybase" in kinds:
            entry.update(type="base", team=None, kind="military")
        else:
            m = re.search(r"Generic_(\w+)\.et|Natural(Hill|Island)\.et|/(Aquatic)/", " ".join(common))
            kind = (m.group(1) or m.group(2) or "water").lower() if m else ("natural" if "natural" in kinds else "place")
            entry.update(type="place", kind=kind)
        out.append(entry)
    return out


def scenario(fs, guids: dict[str, str], world, strings: dict[str, str]) -> tuple[list[dict], list[dict], dict]:
    objectives, spawns, dropped = [], [], {}

    def drop(why: str) -> None:
        dropped[why] = dropped.get(why, 0) + 1

    for e in world.entities:
        path = guids.get((e.prefab or "").upper(), e.prefab or "")
        low, cls = path.lower(), (e.cls or "").lower()
        relevant = ("militarybase" in low or "relayradio" in low or "spawnpoint" in low or "spawnpoint" in cls
                    or "/compositions/locations/" in low or "capture" in low or "capturearea" in cls)
        if not relevant:
            continue
        if e.parent is not None:
            drop("inside a composition")
            continue
        pos = _p(e)
        if pos is None:
            drop("no position")
            continue
        faction = _faction(path)
        team = TEAMS.get(faction)
        if "relayradio" in low:
            objectives.append({"type": "objective", "kind": "relay", "team": team, "name": _pretty(e.name or "") or "radio relay",
                               "position": pos})
        elif "militarybase" in low and "logic" not in low:
            name = _pretty(re.sub(r"^(Conflict)?(Military)?Base", "", e.name or "")) or "base"
            kind = "airfield" if re.search(r"(?i)air(field|port|base)", e.name or "") else "base"
            objectives.append({"type": kind, "kind": "military", "team": team, "name": name, "position": pos,
                               "heading": _heading(e)})
        elif "capture" in low or "capturearea" in cls:
            objectives.append({"type": "capture_zone", "team": team, "name": _pretty(e.name or "") or "capture area",
                               "letter": (e.name or "")[-1:].upper() if e.name else "", "position": pos})
        elif "/compositions/locations/" in low:
            stem = Path(path).stem
            m = re.match(r"SupplyCache_(\w+?)_(?:FIA|US|USSR)", stem)
            if m:
                objectives.append({"type": "objective", "kind": "supply_cache", "team": team, "name": _pretty(m.group(1)),
                                   "position": pos})
            else:
                label = _pretty(re.sub(r"^Base_|_(FIA|US|USSR)_\d+$", "", stem))
                objectives.append({"type": "objective", "kind": "location", "team": team, "name": label, "position": pos})
        else:  # spawn points
            ambient = "ambient" in low
            vehicle = "vehicle" in low
            spawns.append({"type": "vehicle_spawn" if vehicle else "spawn", "team": team, "faction": faction,
                           "position": pos, "heading": _heading(e), "rule": "ambient" if ambient else "team",
                           "name": e.name or Path(path).stem})
    return objectives, spawns, dropped


def scenario_files(fs, world: str) -> list[str]:
    stem = world.rsplit("/", 1)[-1].lower()
    out = []
    for path in fs.find("worlds/", ".ent"):
        low = path.lower()
        name = low.rsplit("/", 1)[-1][:-4]
        if low.startswith(f"worlds/{world.lower()}/") or "/editor/" in low or name.startswith("rally_"):
            continue
        if re.search(rf"(^|_){re.escape(stem)}\d*$", name):
            out.append(path)
    return sorted(out)


def build(install: Path, fs, world: str) -> dict:
    from .enfusionworld import read_world, resource_paths, world_file

    guids = resource_paths(install)
    strings = string_table(fs)
    stem = world.rsplit("/", 1)[-1]
    layouts = []
    base = world_file(fs, world)
    if base:
        layouts.append({"id": "world", "name": stem, "mode": "world", "aliases": [stem], "objectives":
                        places(fs, guids, read_world(fs.read(base)), strings), "zones": [], "spawns": []})
    for path in scenario_files(fs, world):
        try:
            w = read_world(fs.read(path))
        except Exception as exc:  # noqa: BLE001 - one unreadable scenario never costs the others
            layouts.append({"id": Path(path).stem, "name": Path(path).stem, "mode": Path(path).stem, "aliases": [],
                            "objectives": [], "zones": [], "spawns": [], "error": str(exc)})
            continue
        objectives, spawns, dropped = scenario(fs, guids, w, strings)
        mode = Path(path).stem
        nice = re.sub(rf"_?{re.escape(stem)}\d*$", "", mode).replace("CTI_Campaign", "Conflict").replace("_", " ").strip()
        layouts.append({"id": mode, "name": nice or mode, "mode": mode, "aliases": [path], "objectives": objectives,
                        "zones": [], "spawns": spawns, "dropped": dropped})
    return {"format": "3dheat-layouts", "version": 1, "game": "arma-reforger", "level": world.replace("/", "_"),
            "source": f"heat3d-reforger-maps {__version__}", "units": "m", "up": "y",
            "teams": {str(v): k for k, v in TEAMS.items()}, "layouts": layouts}
