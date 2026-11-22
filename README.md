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

Each game reader is its own small project with its own licence file, releases
and issue tracker, so it can be installed, updated, maintained - or withdrawn
on a rights holder's request - on its own, without affecting the viewer or the
other tools. The levels it writes stay on your machine.

## The standalone program

No Python needed: download the file for your system from the
[latest release](https://github.com/Holdi601/3DHeat-Ext-Reforger/releases/latest)
(`heat3d-reforger-<version>-windows-x64.zip` for Windows,
`heat3d-reforger-<version>-linux-x64.tar.gz` for Arma Reforger under Proton on
Linux and Steam Deck), check it against `SHA256SUMS`, unpack it and start
`heat3d-reforger`. Its window finds your Arma Reforger install, says what is
missing, lists the maps that are new or changed since the last extraction and
extracts the ones you pick into the 3DHeat levels folder, and asks before it
updates itself. `heat3d-reforger --help` lists its commands (every command
below runs through it too). The 3DHeat app's Extractors panel can install and
update it for you. See
[The standalone program](https://holdi601.github.io/3DHeat-Ext-Reforger/#the-standalone-program-no-python-needed).

The window walks through four steps (find the game, choose, work, done) in the 3DHeat look, dark or light. On Windows the program opens only its window, with no console window; in a terminal it prints as usual, and `heat3d-reforger-cli.cmd` in the same folder makes the terminal wait for it and pass on its exit code.

## Quick start for new users (Python)

You need: Windows, [Python](https://www.python.org/downloads/) 3.10 or later
("Add python.exe to PATH" ticked in its installer), Arma Reforger installed
through Steam (found by itself), and about 200 MB of disk space for a small
world like Arland, more for the large ones. No Git is needed.

1. Install the tool (one line, in PowerShell or a command prompt); it brings
   [3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles), the
   library it reads with:

   ```bash
   python -m pip install https://github.com/Holdi601/3DHeat-Ext-Reforger/archive/refs/tags/v0.1.0.zip
   ```

2. List the worlds and export one (a game outside the Steam libraries needs
   `--install "<game folder>"`):

   ```bash
   heat3d-reforger-maps worlds
   heat3d-reforger-maps world Arland -o Arland.glb
   ```

3. The output is `Arland.glb` in the folder you ran it in (about 200 MB, in
   about 10 seconds); `world` ends with its report (`ground`, `structure`,
   `water`). Without `-o` it is `<world>.glb`.
4. Open it in the [3DHeat viewer](https://github.com/Holdi601/3DHeat#quick-start):
   download the viewer (**Code -> Download ZIP**, unpack) and double-click
   `start.bat`; it offers to install [Node.js](https://nodejs.org/) when it is
   missing and opens Chrome or Edge at `http://127.0.0.1:5273`. There,
   **Background / level -> 3D model...** and pick the `.glb`. The game's frame
   is left-handed: **Invert world axis** (under **Camera & scene**) shows it
   unmirrored.

When a new release is out, the tool says so when it starts, shows its notes
and asks: update now, later, or skip this version. It updates without asking
only when you chose that: `--auto-update` (this run), the standalone window's
*Update automatically*, or `HEAT3D_AUTO_UPDATE=1`. `python -m heat3d_ext_reforger.update`
updates on request; `HEAT3D_NO_UPDATE=1` switches the check off.

## Install from a checkout

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
| `catalog [-o FILE] [--game FOLDER]` | every vehicle and weapon prefab of the install (name, class, faction, model, the real vehicle) as `catalog.json`, by default `$HEAT3D_LEVELS/arma-reforger/catalog.json`; for the viewer's unit names and order | - |
| `models [-o LEVELS] [--game FOLDER] [--only ID...] [--force]` | every catalogued vehicle's model as a local model pack in `<levels>/model-packs/arma-reforger/` (a `.glb` per vehicle at three levels of detail: hull, wheels, turret, gun, rotor as the viewer moves them, and the radio antennas as `aerial`, left out of the vehicle's size; hit zones and armour plates by thickness under `dm`); prefabs with the same models share one file. The pack stays on your machine | - |
| `status [--json]` | every map of the install (Everon `Eden`, Arland, Kolguyev `Cain`, newer ones) as `new`, `changed`, `outdated` or `current` against the levels already written (`manifest.json` in the levels folder); `--all-worlds` also lists the editor and test worlds | - |
| `all [--force]` | every map `status` does not call current: `<World>.glb`, `<World>.layouts.json` and its manifest entry | - |
| `extract [ids] [--new] [--changed] [--outdated] [--progress-json]` | the same for chosen maps, one JSON line per map (the standalone program's own `status` and `extract` work the same way from `.heat3d-extract.json`) | - |
| `layouts <world>` | the map's named places, and each scenario's bases, relays, supply caches and spawns, as `<World>.layouts.json` | - |
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

The tool reads the files of your own Arma Reforger install. Nothing of the
game is in this repository or downloaded by it: no game assets, no game code,
no DLLs. The level it writes stays on your machine, to view, not to share
([Terms and licence](https://holdi601.github.io/3DHeat-Ext-Reforger/terms.html)).

3DHeat Reforger is not affiliated with or endorsed by Bohemia Interactive.
Arma Reforger and related names and trademarks belong to their owners.
Rights holders: open an issue at
[github.com/Holdi601/3DHeat-Ext-Reforger/issues](https://github.com/Holdi601/3DHeat-Ext-Reforger/issues) -
we respond quickly and remove anything on request.

## Tests

```bash
python -m pip install -e .[test]
python -m pytest
```

On made-up data; the checks against a real install run when Arma Reforger is
installed and skip otherwise, and never write into the repository.

## Licence

MIT ([`LICENSE`](LICENSE)). Third-party software it uses: [`LICENSES.md`](LICENSES.md).
