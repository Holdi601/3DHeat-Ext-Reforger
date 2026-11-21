"""
The standalone app on a synthetic Arma Reforger install: its maps, and a map a
DLC adds found as new. The Enfusion reader is replaced by a stand-in that
calls each tiny `addons/data/<map>.pak` one map's archive; the CLI's own
`extract` runs, with the export itself replaced.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from heat3d_ext_reforger import enfusion, levels
from heat3d_ext_reforger.app import entry, paths
from heat3d_ext_reforger.standalone_spec import SPEC


@pytest.fixture
def game(tmp_path, monkeypatch):
    lib = tmp_path / "Steam"
    root = lib / "steamapps" / "common" / "Arma Reforger"
    (root / "addons" / "data").mkdir(parents=True)
    for name in ("Eden", "Arland"):
        (root / "addons" / "data" / f"{name}.pak").write_bytes(name.encode() * 8)

    def worlds(fs):
        return [{"id": p.stem, "world": p.stem, "name": p.stem, "kind": "map", "size": 4096,
                 "sources": [{"path": str(p), "hash": p.stem}]}
                for p in sorted((root / "addons" / "data").glob("*.pak"))]

    def export_one(install, fs, w, folder, args, log=print):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{w['id']}.glb").write_bytes(b"glb")
        (folder / f"{w['id']}.layouts.json").write_text("{}", encoding="utf-8")
        return 0

    monkeypatch.setattr(enfusion.FileSystem, "of_install", staticmethod(lambda install: object()))
    monkeypatch.setattr(levels, "worlds", worlds)
    monkeypatch.setattr(levels, "export_one", export_one)
    monkeypatch.setattr(paths, "steam_roots", lambda: [lib])
    monkeypatch.setattr("heat3d_gamefiles.steam.STEAM_DEFAULTS", ())
    monkeypatch.setattr("heat3d_gamefiles.steam.steam_libraries", lambda: [])
    monkeypatch.setattr("heat3d_ext_reforger.update.startup", lambda *a, **k: None)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_LEVELS", str(tmp_path / "levels"))
    monkeypatch.setenv("HEAT3D_NO_UPDATE", "1")
    return root


def status(capsys) -> dict:
    assert entry.main(SPEC, ["status", "--json"]) == 0
    return json.loads(capsys.readouterr().out)["games"][0]


def test_find_and_maps(game):
    g = SPEC.games[0]
    assert g.find(None) == game
    assert [m.id for m in g.maps(game)] == ["Arland", "Eden"]
    assert g.maps(game)[0].sources == [game / "addons" / "data" / "Arland.pak"]


def test_install_that_gains_a_map(game, tmp_path, capsys):
    g = status(capsys)
    assert g["found"] and g["counts"]["new"] == 2

    assert entry.main(SPEC, ["extract", "--new", "--progress-json"]) == 0
    events = [json.loads(l) for l in capsys.readouterr().out.splitlines() if l.startswith('{"event"')]
    assert events[-1] == {"event": "done", "ok": 2, "failed": 0}
    out = tmp_path / "levels" / "arma-reforger"
    man = json.loads((out / ".heat3d-extract.json").read_text(encoding="utf-8"))
    assert man["entries"]["Eden"]["outputs"] == ["arma-reforger/Eden.glb", "arma-reforger/Eden.layouts.json"]

    # A DLC brings a map: it is new, the extracted ones stay current.
    (game / "addons" / "data" / "Cain.pak").write_bytes(b"cain")
    states = {m["id"]: m["state"] for m in status(capsys)["maps"]}
    assert states == {"Arland": "current", "Cain": "new", "Eden": "current"}
