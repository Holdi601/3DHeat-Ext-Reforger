---
title: Command reference
nav_order: 90
---

# Command reference

Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.
The other pages explain each command step by step.

## `heat3d-reforger-maps`

```text
usage: heat3d-reforger-maps [-h] [--version]
                            {worlds,enfusion-worlds,world,enfusion-world,identify} ...

Arma Reforger worlds (Enfusion) from your own install into 3DHeat levels.

positional arguments:
  {worlds,enfusion-worlds,world,enfusion-world,identify}
    worlds (enfusion-worlds)
                        list the worlds of an installed Arma Reforger
    world (enfusion-world)
                        export an Arma Reforger world: terrain, its colour, the sea,
                        building boxes
    identify            say whether a file is an Enfusion archive, terrain, world file
                        or texture

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

What you point it at is subject to the game's own licence; the levels it writes are
for your own use.
```

## `worlds`

```text
usage: heat3d-reforger-maps worlds [-h] [--install INSTALL]

options:
  -h, --help         show this help message and exit
  --install INSTALL  the game's folder, if not in a Steam library
```

## `world`

```text
usage: heat3d-reforger-maps world [-h] [-o OUT] [--install INSTALL]
                                  [--ground-spacing METRES] [--texture-size PIXELS]
                                  [--no-structures] [--trees]
                                  world

positional arguments:
  world                 the world's name as `enfusion-worlds` lists it

options:
  -h, --help            show this help message and exit
  -o, --out OUT         the .glb (default: <world>.glb, in $HEAT3D_LEVELS/<game> when
                        that is set)
  --install INSTALL     the game's folder, if not in a Steam library
  --ground-spacing METRES
                        terrain vertex spacing in the file (default 2, the terrain's
                        own)
  --texture-size PIXELS
                        the ground colour image's larger side (default 4096; 0 for
                        none)
  --no-structures       leave out the placed models
  --trees               also place trees and other vegetation (as boxes)
```

## `identify`

```text
usage: heat3d-reforger-maps identify [-h] path

positional arguments:
  path

options:
  -h, --help  show this help message and exit
```

## Output

### `.glb` parts

`ground:<world>` (the terrain, in the colours of its supertexture tiles), `water:<world>` (the sea, at height zero) and `structure:<world>` (a box per placed model; trees and vegetation only with `--trees`), where `<world>` is the last part of the world's name as `worlds` prints it.

`asset.generator`: `heat3d_gamefiles` (the glTF writer of 3DHeat GameFiles).

`enfusion-worlds` and `enfusion-world` are the same verbs as `worlds` and `world`, under the names 3DHeat GameFiles gave them.
