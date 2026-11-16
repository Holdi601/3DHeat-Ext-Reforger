---
title: Terms and licence
nav_order: 8
---

# Terms and licence

This page says what the tool reads, what it ships and where its sources come
from.

## Bohemia Interactive's game

Arma Reforger and its worlds belong to Bohemia Interactive. 3DHeat Reforger is
not affiliated with or endorsed by Bohemia Interactive; Arma Reforger and
related names and trademarks belong to their owners.

This tool ships nothing of the game - no game assets, no game code, no DLLs -
and downloads nothing: it reads the files of the copy **you** installed, on
your machine, outside the game. It changes nothing in the game, does not run
alongside it and talks to no server. Nothing in the game's files is encrypted,
and nothing is decrypted.

The world it writes stays on your machine: it is for your own use, not to be
shared, published or sold. The repository's `.gitignore` keeps game files and
exports out of version control by file type.

Each game reader is its own small project with its own licence file, releases
and issue tracker, so it can be installed, updated, maintained - or withdrawn
on a rights holder's request - on its own, without affecting the viewer or the
other tools.

Rights holders: open an issue at
[github.com/Holdi601/3DHeat-Ext-Reforger/issues](https://github.com/Holdi601/3DHeat-Ext-Reforger/issues) -
we respond quickly and remove anything on request.

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
