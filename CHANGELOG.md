# Changelog

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
