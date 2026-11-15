---
title: Terms and licence
nav_order: 8
---

# Terms and licence

This page is a record of what the licences say, not legal advice.

## Bohemia Interactive's game

Arma Reforger and its worlds belong to Bohemia Interactive, who do not endorse
this project. This tool ships nothing of the game and downloads nothing: it
reads the files of the copy **you** installed, on your machine, outside the
game. It changes nothing in the game, does not run alongside it and talks to no
server. Nothing in the game's files is encrypted, and nothing is decrypted.

The game's licence allows non-commercial use and forbids reverse engineering
the game files. Reading your own install is your decision under it, and the
obligation sits with whoever runs the tool. The world it writes is the game
publisher's content: it is for your own use, not to be shared, published or
sold. The repository's `.gitignore` keeps game files and exports out of version
control by file type.

Bohemia's own route into the game's data is **Arma Reforger Tools** (the
Enfusion Workbench), free on Steam for making mods under Bohemia's modding
terms. This tool does not need it and does not use it; it reads the installed
game's archives directly.

That is why it is a separate package: if Bohemia Interactive ever asks for it
to go, it goes alone, and the viewer, GameFiles and the other tools stay.

## The formats

The Enfusion readers (`enfusion.py`, `enfusionworld.py`) were worked out from
Arma Reforger's own installed files, with nothing else as a source. Bohemia
Interactive publishes its game scripts under the Arma Public Licence, which is
not MIT-compatible; none of them was read for this or copied. How each format
is read, and what it was checked against:
[Arma Reforger worlds](level-arma-reforger.md#how-it-is-read-and-checked).

## Licence and sources

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSE)):
use it, change it, ship it, commercially or not. It builds on
[3DHeat GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) (MIT) and needs
numpy (BSD-3-Clause), Pillow (MIT-CMU) and lz4 (BSD-3-Clause); the tests need
pytest (MIT). See
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Reforger/blob/main/LICENSES.md).
