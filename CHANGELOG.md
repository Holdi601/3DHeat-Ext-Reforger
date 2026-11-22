# Changelog

## 0.6.0

- Its own icon: the 3DHeat cube with a text badge for its game (letters in 3DHeat's colours), as the
  program, window, taskbar and docs icon.
- A new window: the 3DHeat look in dark and light (follows the system, switchable), the logo and
  icon, sharp at any display scaling. Four steps: find the game (each requirement with its fix),
  choose (maps ticked when there is something to do, filters, search; jobs with their fields
  inline), work (progress, time left, cancel), done (open in 3DHeat, open the output folder, and
  for a failure what went wrong and what to do, copy details, report a problem).
- No console window on Windows: the program is a window program. From a terminal it still prints
  as before; `heat3d-reforger-cli.cmd` beside it waits for it in a terminal and passes its exit code.
- The update offer in the same look: Update now / Later / Skip this version, and "Update
  automatically" from the dialog.
- CI draws every page and dialog of the window (on Linux under a virtual display) and checks the
  Windows build is a window program.

## 0.5.0

- A standalone program for Windows and Linux (no Python needed), built by CI with a `SHA256SUMS` file. Without
  arguments it opens a window: what is found and what is missing (install, disk space), the levels folder, the
  maps as new / changed by a game update / extracted by an older version / up to date, and extraction of the
  picked ones one at a time into `<levels>/arma-reforger/` (the level and its layouts), and updates.
- Each map it extracts is also recorded in `<levels>/arma-reforger/.heat3d-extract.json` (extractor version, game
  build, size and SHA-256 of the archives its files are in), which its `status --json` and
  `extract --new` / `--changed` / `--outdated` / `<map>...` / `--progress-json` read; `manifest.json` and the
  tool's own `status`, `all` and `extract` stay as they were.
- Updates ask first (update now / later / skip this version) unless automatic updates were chosen
  (`--auto-update`, the window's checkbox, or `HEAT3D_AUTO_UPDATE=1`).
- The install is also found in every Steam library Steam's own settings list on Windows.

## 0.4.0

- `status [--json]`: every map of the install (Everon `Eden`, Arland, Kolguyev `Cain`, and any newer one) as `new`,
  `changed` (an update changed the world's files), `outdated` (written by an older level format), `current` or no
  longer installed, against `<levels>/arma-reforger/manifest.json`. Editor, test and showcase worlds only with
  `--all-worlds`. `--json` answers in the shape the 3DHeat extractors manager reads.
- `all` and `extract [ids] [--new] [--changed] [--outdated] [--progress-json]`: the maps not yet current, each as
  `<World>.glb` and `<World>.layouts.json`, recorded in the manifest (id, game build, the world's fingerprints,
  extractor and level-format version, files). Maps over 8 km at 4 m ground spacing, the rest at 2 m.
- `layouts <world>`: the map's named places (towns by size, airports, military bases, hills, bays, lakes, named by
  their English map labels) and one layout per scenario world built on it (Conflict, Game Master, combat ops,
  capture and hold): military bases, airbases, radio relays, supply caches, capture areas and spawn points with
  their faction.
- Installs are also found in the Linux, Flatpak and Snap Steam libraries (Proton).

## 0.3.2

- `models`: thin posts and masts up to 5 cm about their axis (was 3 cm) are found by their shape as aerials too,
  drawn and left out of the vehicle's size: the LAV-25 is 2.71 m tall in the pack, not 3.02 m.

## 0.3.1

- `models`: radio antennas, whips and masts no longer make vehicles look taller than they are. They are found by
  name (a node or material called antenna, aerial or whip) or by shape (a thin, long, mostly upright piece, with the
  small bits along it, reaching above everything else) and written as their own part `aerial` (on a turret they
  stay with the turret). The size in the pack (`box`, `length`, `width`, `height`) leaves them out.
- `models`: only running gear is `gear`. Steering wheels, dials, spare tyres and the adjusting wheels of a gun sight
  were taken for wheels; a helicopter with a pilot's sight had a stray `gear` part.
- The size in the pack is measured on the full-detail model.

## 0.3.0

- `models`: every catalogued vehicle's model from your own install as a local model pack
  (`<levels>/model-packs/arma-reforger/`), drawn by the 3DHeat viewer in place of its figures. Each vehicle is built
  from its prefab: the body model and what its slots hold (wheels, turret, main rotor, doors, roofs, glass) on their
  nodes, the turret's weapons on its gun node; parts hull, gear, turret (yaw pivot), gun (pitch pivot) and rotor.
  The prefabs' hit zones (engine, fuel tanks, gearbox, battery...) and the hull's armour plates by thickness go under
  `dm`. Variants with the same models share one file.
- A reader for Enfusion models (`.xob`): node tree, levels of detail, triangle meshes with their materials and skin
  bones, and the collision shapes (boxes, convex hulls, capsules, triangle meshes with their game materials).
- `catalog` links each vehicle to its file in the model pack when there is one.

## 0.2.0

- `catalog`: every vehicle and weapon prefab of your install as `catalog.json`: each vehicle's name, class,
  faction (followed up its parent prefabs), model and the real vehicle it stands for; each weapon's class. The
  viewer names Arma Reforger units by it and draws them with another game's local model of the same vehicle.

## 0.1.0

- First version, moved out of 3DHeat GameFiles with its history (GameFiles'
  `enfusion-worlds` and `enfusion-world` now run this tool): an Arma Reforger
  world from your own install as a 3DHeat level - the terrain in its own
  colours, the sea and every placed model as a box. `worlds` and `world` take
  the same options and defaults as in GameFiles, and answer to the GameFiles
  names `enfusion-worlds` and `enfusion-world` too.
- `worlds` says where the game was found; a world that is not there is exit 2,
  with the names there are.
- `identify <file>`: an Enfusion archive, terrain, terrain tile, world file or
  texture described; exit 2 and `not an Arma Reforger file` for anything else.
- Installs with one pip line from the release zip, no Git needed (GameFiles comes from its own release zip); a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

## Docs

Where each feature is documented
([holdi601.github.io/3DHeat-Ext-Reforger](https://holdi601.github.io/3DHeat-Ext-Reforger/)):

| Feature | Page |
|---|---|
| Installing, GameFiles, a first run | [Before you start](docs/before-you-start.md) |
| Listing worlds and exporting one (`worlds`, `world` and every option), the parts, how each format is read and checked | [Arma Reforger worlds](docs/level-arma-reforger.md) |
| `identify` | [Identifying a file](docs/identify.md) |
| Bohemia Interactive's game, what the tool reads, the format sources, why it is its own project | [Terms and licence](docs/terms.md) |
| Every option and part name, generated | [Command reference](docs/cli-reference.md) |
| Release checklist for the docs | [Maintaining these docs](docs/maintaining.md) |
