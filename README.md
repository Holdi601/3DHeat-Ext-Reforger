# 3DHeat Reforger: Arma Reforger worlds as 3D levels

**What is it?** This tool turns an Arma Reforger world, read from your own
install, into a 3D model you can fly over in the
[3DHeat](https://github.com/Holdi601/3DHeat) viewer: the terrain in the colours
of its own ground textures, the sea, and every placed building and object as a
box.

**Why would I use it?** So heat from Arma Reforger has the ground and the
buildings under it, in the game's own metres.

**Example:** `heat3d-reforger-maps world <world> -o world.glb` -> `world.glb`.

**Documentation:** [holdi601.github.io/3DHeat-Ext-Reforger](https://holdi601.github.io/3DHeat-Ext-Reforger/), a page per
command with step-by-step use and example output. Part of
[3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)).

This tool is kept outside the 3DHeat tools on purpose: it reads Bohemia
Interactive's game files. If it ever has to go, nothing else goes with it. The
levels it writes stay on your machine.

## Install

New to the command line? Read [Before you start](https://holdi601.github.io/3DHeat-Ext-Reforger/before-you-start.html) first.

1. Install Python 3.10 or later, and Arma Reforger through Steam.
2. `git clone https://github.com/Holdi601/3DHeat-Ext-Reforger` (or download the
   ZIP) and open a terminal in that folder.
3. Install the command - it brings [3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles),
   the library it reads with - and check that the game is found:

```bash
python -m pip install -e .        # installs heat3d-reforger-maps and GameFiles
heat3d-reforger-maps worlds       # where the game is, and its worlds
```

You should see `Arma Reforger at <the game's folder>: <n> worlds with a terrain`
and a line per world. Without pip, the tool finds GameFiles in
`HEAT3D_GAMEFILES`, in `../../gamefiles` (inside a 3DHeat checkout) or in
`../3DHeat-GameFiles`.

## Commands

| Command | Does | Page |
|---|---|---|
| `worlds [--install FOLDER]` | where the game is, and every world with a terrain | [worlds and world](https://holdi601.github.io/3DHeat-Ext-Reforger/level-arma-reforger.html) |
| `world <world> [-o FILE] [options]` | one world as a `.glb` | [worlds and world](https://holdi601.github.io/3DHeat-Ext-Reforger/level-arma-reforger.html) |
| `identify <file>` | whether a file is an Enfusion archive, terrain, world file or texture | [identify](https://holdi601.github.io/3DHeat-Ext-Reforger/identify.html) |

`enfusion-worlds` and `enfusion-world` are the same two verbs under the names
3DHeat GameFiles gave them; GameFiles' own `enfusion-worlds` and
`enfusion-world` run this tool with the same arguments.

```bash
heat3d-reforger-maps world <world> -o world.glb
heat3d-reforger-maps world <world> --trees                    # vegetation too, as boxes
heat3d-reforger-maps world <world> --texture-size 0           # flat colour, small file
```

| `world` option | Does |
|---|---|
| `-o`, `--out FILE` | the `.glb` to write (default `<world>.glb`, in `$HEAT3D_LEVELS/<game>/` when that is set) |
| `--install FOLDER` | the game's folder, when it is in no Steam library |
| `--ground-spacing METRES` | the terrain's vertex spacing in the file (default 2, the terrain's own) |
| `--texture-size PIXELS` | the ground colour image's larger side (default 4096; 0 for none) |
| `--no-structures` | leave out the placed models |
| `--trees` | also place trees and other vegetation (as boxes) |

Exit status: 0 done; 1 reading failed; 2 the game, the world, the file or
GameFiles not found (the message says which, and what to do). Every option,
as the program prints it: [Command reference](https://holdi601.github.io/3DHeat-Ext-Reforger/cli-reference.html).

## What comes out, and loading it

One glTF binary in the game's own coordinates (x east, y up, z north, metres):
`ground:<world>`, `water:<world>` and `structure:<world>`. Load it in the
viewer's **Background / level** panel
([loading a level](https://holdi601.github.io/3DHeat/levels.html)); the game's
frame is left-handed, and the viewer's *invert world axis* shows it unmirrored.

## Terms

Arma Reforger and its worlds belong to Bohemia Interactive, who do not endorse
this project. Nothing of the game is in this repository or downloaded by it.
The game's licence allows non-commercial use and forbids reverse engineering
the game files: reading your own install is your decision under it, and the
level it writes is yours to view, not to share
([Terms and licence](https://holdi601.github.io/3DHeat-Ext-Reforger/terms.html)).

## Tests

```bash
python -m pip install -e .[test]
python -m pytest
```

On made-up data; the checks against a real install run when Arma Reforger is
installed and skip otherwise, and never write into the repository.

## Licence

MIT ([`LICENSE`](LICENSE)). Third-party software it uses: [`LICENSES.md`](LICENSES.md).
