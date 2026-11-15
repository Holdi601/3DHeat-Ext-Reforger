"""The command line: the verbs under both names, the options GameFiles passes through, identify, the exit codes."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from heat3d_ext_reforger import cli, library

from .test_enfusion import BC1_RED, edds, glb_json, install, terrain_files, world_bytes

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("verb", ["world", "enfusion-world"])
def test_world_takes_every_option_of_the_gamefiles_verb(tmp_path, verb):
    args = cli.parser().parse_args([
        verb, "Isle", "-o", str(tmp_path / "x.glb"), "--install", str(tmp_path), "--ground-spacing", "4",
        "--texture-size", "0", "--no-structures", "--trees",
    ])
    assert args.verb == verb and args.world == "Isle"
    assert args.out == tmp_path / "x.glb" and args.install == tmp_path
    assert args.ground_spacing == 4.0 and args.texture_size == 0 and args.no_structures and args.trees


def test_world_defaults_match_gamefiles():
    args = cli.parser().parse_args(["world", "Isle"])
    assert args.out is None and args.install is None
    assert args.ground_spacing == 2.0 and args.texture_size == 4096
    assert not args.no_structures and not args.trees


@pytest.mark.parametrize("verb", ["worlds", "enfusion-worlds"])
def test_worlds_says_where_the_game_is_and_lists_its_worlds(tmp_path, capsys, verb):
    root = install(tmp_path)
    assert cli.main([verb, "--install", str(root)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"Arma Reforger at {root}: 1 worlds with a terrain"
    assert out[1].split()[0] == "Isle"


@pytest.mark.parametrize("verb", ["world", "enfusion-world"])
def test_world_writes_the_level(tmp_path, capsys, verb):
    root = install(tmp_path / "game")
    out = tmp_path / "isle.glb"
    assert cli.main([verb, "Isle", "-o", str(out), "--install", str(root), "--texture-size", "64"]) == 0
    nodes = [n["name"] for n in glb_json(out)["nodes"]]
    assert "ground:Isle" in nodes and "structure:Isle" in nodes
    assert f"-> {out}" in capsys.readouterr().out


def test_no_such_world_is_exit_2_with_the_ones_there_are(tmp_path, capsys):
    root = install(tmp_path)
    assert cli.main(["world", "Nowhere", "--install", str(root)]) == 2
    assert "Isle" in capsys.readouterr().err


def test_no_game_is_exit_2_saying_what_to_do(tmp_path, capsys):
    assert cli.main(["worlds", "--install", str(tmp_path / "none")]) == 2
    assert "--install" in capsys.readouterr().err


def test_identify_an_archive(tmp_path, capsys):
    root = install(tmp_path)
    assert cli.main(["identify", str(root / "addons" / "data" / "data.pak")]) == 0
    out = capsys.readouterr().out
    assert "Enfusion archive (.pak)" in out and "files" in out


def test_identify_a_terrain_a_tile_a_world_and_a_texture(tmp_path, capsys):
    files = terrain_files()
    (tmp_path / "Terrain.terr").write_bytes(files["worlds/Isle/Terrain/Terrain.terr"])
    tile = next(name for name in files if name.endswith(".ttile"))
    (tmp_path / "t.ttile").write_bytes(files[tile])
    (tmp_path / "Isle.ent").write_bytes(world_bytes())
    (tmp_path / "a.edds").write_bytes(edds(4, 4, 71, [(b"COPY", BC1_RED)]))
    expect = {"Terrain.terr": "Enfusion terrain (.terr)", "t.ttile": "Enfusion terrain tile (.ttile)",
              "Isle.ent": "Enfusion binary entity file", "a.edds": "Enfusion texture (.edds)"}
    for name, kind in expect.items():
        assert cli.main(["identify", str(tmp_path / name)]) == 0, name
        assert kind in capsys.readouterr().out


def test_identify_turns_away_another_file_quietly(tmp_path, capsys):
    other = tmp_path / "plain.dds"
    other.write_bytes(b"DDS " + bytes(200))
    assert cli.main(["identify", str(other)]) == 2
    out = capsys.readouterr()
    assert out.out == "" and out.err.strip() == "not an Arma Reforger file"


def test_identify_a_missing_file(tmp_path, capsys):
    assert cli.main(["identify", str(tmp_path / "gone.pak")]) == 2
    assert "no such file" in capsys.readouterr().err


def test_without_gamefiles_it_says_what_to_do(tmp_path):
    # A copy of the package alone, nowhere near GameFiles.
    import shutil

    shutil.copytree(ROOT / "heat3d_ext_reforger", tmp_path / "pkg" / "heat3d_ext_reforger",
                    ignore=shutil.ignore_patterns("__pycache__"))
    env = {k: v for k, v in os.environ.items() if k not in ("HEAT3D_GAMEFILES", "PYTHONPATH")}
    r = subprocess.run([sys.executable, "-I", "-c", "import sys; sys.path.insert(0, sys.argv[1]); "
                        "from heat3d_ext_reforger.cli import main; sys.exit(main(['identify', 'gone.pak']))",
                        str(tmp_path / "pkg")], capture_output=True, text=True, env=env)
    if r.returncode != 2 or library.MISSING not in r.stderr:
        pytest.skip("heat3d_gamefiles is installed in this Python, so it is always found")
    assert r.stderr.strip() == library.MISSING
