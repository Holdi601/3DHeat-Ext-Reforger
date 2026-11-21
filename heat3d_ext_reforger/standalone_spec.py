"""
The standalone app's description of this tool (app/spec.py): the Arma
Reforger install it reads, its maps (new ones after an update or a DLC are
found by app/manifest.py), and how one map becomes a level with its layouts.
`python -m heat3d_ext_reforger.standalone_spec` runs the app from a checkout;
the release executables run the same.
"""

from __future__ import annotations

from pathlib import Path

from . import __version__
from .app.spec import Check, GameSpec, MapSource, Spec


def _find(given: str | None) -> Path | None:
    from . import library

    if not library.ensure():
        return None
    from .enfusion import find_install

    return find_install(given)


def _maps(game: Path) -> list[MapSource]:
    """The maps `status` lists (not the editor and test worlds), each with the archives its files are in."""
    from .enfusion import FileSystem
    from .levels import worlds

    fs = FileSystem.of_install(game)
    return [MapSource(w["id"], w["name"], [Path(s["path"]) for s in w["sources"]], note=w["world"])
            for w in worlds(fs) if w["kind"] == "map"]


def _extract(game: Path, m: MapSource, out: Path, log) -> list[Path]:
    from . import cli

    code = cli.main(["extract", m.id, "--install", str(game), "--levels", str(out)])
    if code != 0:
        raise RuntimeError(f"heat3d-reforger-maps extract exited {code}")
    return [p for p in (out / f"{m.id}.glb", out / f"{m.id}.layouts.json") if p.is_file()]


def _build(game: Path) -> str | None:
    from .levels import game_build

    b = game_build(game)
    return None if b == "unknown" else b


def _checks(found: dict, levels: Path) -> list[Check]:
    from . import library

    ok = library.ensure()
    return [Check("gamefiles", "3DHeat GameFiles (the library the readers build on)", ok,
                  "found" if ok else library.MISSING)]


SPEC = Spec(
    id="heat3d-reforger",
    name="3DHeat Reforger",
    repo="Holdi601/3DHeat-Ext-Reforger",
    version=__version__,
    tools={"heat3d-reforger-maps": "heat3d_ext_reforger.cli:main"},
    default_tool="heat3d-reforger-maps",
    description="Arma Reforger maps as 3D levels for the 3DHeat viewer",
    module="heat3d_ext_reforger.standalone_spec",
    games=[GameSpec(
        key="arma-reforger", label="Arma Reforger", find=_find, subdir="arma-reforger", build=_build,
        maps=_maps, extract=_extract,
        existing_outputs=lambda out, m: [out / f"{m.id}.glb"],
        output_version="0.4.0",
        platforms=("windows-x64", "linux-x64"),
    )],
    checks=_checks,
    min_free_gb=5.0,
    notice="Not affiliated with or endorsed by Bohemia Interactive.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))
