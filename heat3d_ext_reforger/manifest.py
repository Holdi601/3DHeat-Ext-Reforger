"""
The levels written so far, as `<levels>/<game>/manifest.json`, and what `status` makes of it.

Each level records its id, the game build it was read from, the fingerprints of the archives it was made from,
the extractor and level-format version that wrote it, when, and its files. `status` compares that with what is
installed now:

* `new`: an installed world with no level yet;
* `changed`: its archives differ from those the level was made from (a game or DLC update);
* `outdated`: written by an older level format of this tool (a newer one reads more);
* `missing`: recorded, but a file of it is gone;
* `current`: nothing to do;
* `removed`: a level whose world is no longer installed (the level is kept).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

NAME = "manifest.json"


def load(folder: Path) -> dict:
    try:
        doc = json.loads((folder / NAME).read_text(encoding="utf-8"))
        if isinstance(doc, dict) and isinstance(doc.get("levels"), dict):
            return doc
    except (OSError, ValueError):
        pass
    return {"format": "3dheat-level-manifest", "version": 1, "levels": {}}


def _rel(folder: Path, p: Path) -> str:
    try:
        return p.resolve().relative_to(folder.resolve()).as_posix()
    except ValueError:
        return str(p)


def record(folder: Path, game: str, tool: str, version: str, level_format: int, level: str, *, build: str,
           sources: list[dict], files: list[Path], **extra) -> dict:
    doc = load(folder)
    doc.update(game=game, tool=tool)
    entry = {
        "id": level, "gameBuild": build, "sources": sources, "extractor": f"{tool} {version}",
        "levelFormat": level_format, "exported": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": [_rel(folder, p) for p in files],
    }
    entry.update(extra)
    doc["levels"][level] = entry
    folder.mkdir(parents=True, exist_ok=True)
    tmp = folder / (NAME + ".part")
    tmp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(folder / NAME)
    return entry


#: Our states as the extractors manager names them: a level whose world is gone is its `missing`; a level whose
#: files are gone is extracted again, as a new one is.
MANAGER_STATE = {"new": "new", "changed": "changed", "outdated": "outdated", "current": "current",
                 "removed": "missing", "missing": "new"}


def manager_status(game: str, label: str, build: str | None, rows: list[dict], version: str, levels: Path) -> dict:
    """`status --json` in the shape the 3DHeat extractors manager reads (`maps.rs`): one game, its maps, counts."""
    maps = []
    counts = dict.fromkeys(("new", "changed", "outdated", "current", "missing"), 0)
    for r in rows:
        state = MANAGER_STATE.get(r["state"], "new")
        counts[state] += 1
        line = {"id": r["id"], "title": r.get("name") or r["id"], "state": state}
        if r.get("extractor"):
            line["extracted_version"] = r["extractor"].rsplit(" ", 1)[-1]
        maps.append(line)
    return {"format": "3dheat-extractor-status", "version": version, "levels": str(levels),
            "games": [{"game": game, "label": label, "found": build is not None, "build": build,
                       "maps": maps, "counts": counts}]}


def pick(rows: list[dict], ids: list[str], *, new: bool, changed: bool, outdated: bool) -> list[str]:
    """The map ids an `extract` asks for: named ones, and those in the chosen states (status order)."""
    known = {r["id"].lower(): r["id"] for r in rows if r["state"] != "removed"}
    chosen: list[str] = []
    for i in ids:
        if i.lower() not in known:
            raise LookupError(f"no map {i!r}; status lists: " + ", ".join(known.values()))
        chosen.append(known[i.lower()])
    states = {s for s, on in (("new", new), ("missing", new), ("changed", changed), ("outdated", outdated)) if on}
    for r in rows:
        if r["state"] in states and r["id"] not in chosen:
            chosen.append(r["id"])
    return chosen


class Progress:
    """`--progress-json`: one JSON line per event - start (total), map (index, id, ok or failed, detail), done."""

    def __init__(self, on: bool) -> None:
        self.on, self.ok, self.failed = on, 0, 0

    def _emit(self, **event) -> None:
        if self.on:
            print(json.dumps(event, ensure_ascii=False), flush=True)

    def start(self, total: int) -> None:
        self._emit(event="start", total=total)

    def map(self, index: int, map_id: str, ok: bool, detail: str = "") -> None:
        if ok:
            self.ok += 1
        else:
            self.failed += 1
        self._emit(event="map", index=index, id=map_id, state="ok" if ok else "failed", detail=detail)

    def fail(self, why: str) -> None:
        self._emit(event="start", total=0)
        self._emit(event="done", ok=0, failed=0, error=why)

    def done(self) -> int:
        self._emit(event="done", ok=self.ok, failed=self.failed)
        return 1 if self.failed else 0


def status(folder: Path, installed: list[dict], level_format: int) -> list[dict]:
    """One row per installed world (`id`, `sources`) and per recorded level no longer installed."""
    doc = load(folder)
    levels = doc["levels"]
    rows = []
    for world in installed:
        entry = levels.get(world["id"])
        row = {k: v for k, v in world.items() if k != "sources"}
        if entry is None:
            row.update(state="new", why="no level yet")
        else:
            had = {s["path"].lower(): s.get("hash") for s in entry.get("sources", [])}
            now = {s["path"].lower(): s.get("hash") for s in world["sources"]}
            missing = [f for f in entry.get("files", []) if not (folder / f).exists()]
            if had != now:
                changed = sorted(set(had) ^ set(now) | {p for p in had.keys() & now.keys() if had[p] != now[p]})
                row.update(state="changed", why="archives differ: " + ", ".join(Path(p).name for p in changed[:4]))
            elif int(entry.get("levelFormat", 0)) < level_format:
                row.update(state="outdated", why=f"level format {entry.get('levelFormat', 0)} < {level_format} ({entry.get('extractor', '')})")
            elif missing:
                row.update(state="missing", why="files gone: " + ", ".join(missing))
            else:
                row.update(state="current", why=f"{entry.get('extractor', '')}, {entry.get('exported', '')}")
            row["exported"] = entry.get("exported", "")
            row["extractor"] = entry.get("extractor", "")
        rows.append(row)
    have = {w["id"] for w in installed}
    for level, entry in levels.items():
        if level not in have:
            rows.append({"id": level, "state": "removed", "why": "world no longer installed (level kept)",
                         "exported": entry.get("exported", "")})
    return rows
