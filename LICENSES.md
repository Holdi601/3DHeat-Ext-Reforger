# Third-party licences

This tool is MIT licensed ([`LICENSE`](LICENSE)). What it uses, and under
which licence; each package's own source is what counts, not this file.

| Software | Licence | How it is used |
|---|---|---|
| 3DHeat GameFiles (`heat3d-gamefiles`) | MIT | a dependency, installed by pip: the glTF writer, the Steam library search, the levels folder, block-compressed texture headers |
| numpy | BSD-3-Clause | a dependency: terrain heights, placement |
| Pillow | MIT-CMU (HPND) | a dependency: decoding the ground colour textures |
| lz4 | BSD-3-Clause | a dependency: the LZ4 levels of `.edds` textures |
| pytest | MIT | development only: the tests |

The licences were read off the package metadata in September 2026. Where a
component's terms changed after that, the source is what counts.

## The formats, and where they were learned

The Enfusion readers (`enfusion.py`, `enfusionworld.py`) were worked out from
Arma Reforger's own installed files, with nothing else as a source; nothing in
the game is encrypted. Bohemia Interactive publishes its game scripts under
the Arma Public Licence, which is not MIT-compatible; none of them was read for
this or copied.

## The game's files

Arma Reforger belongs to Bohemia Interactive. This repository holds no file of
the game and no level made from one - no game assets, no game code, no DLLs;
the tool reads the copy the user installed, on the user's machine, and the
level it writes stays there. See
[Terms and licence](https://holdi601.github.io/3DHeat-Ext-Reforger/terms.html).

Each game reader is its own small project with its own licence file, releases
and issue tracker, so it can be installed, updated, maintained - or withdrawn
on a rights holder's request - on its own, without affecting the viewer or the
other tools.

3DHeat Reforger is not affiliated with or endorsed by Bohemia Interactive.
Arma Reforger and related names and trademarks belong to their owners.
Rights holders: open an issue at
[github.com/Holdi601/3DHeat-Ext-Reforger/issues](https://github.com/Holdi601/3DHeat-Ext-Reforger/issues) -
we respond quickly and remove anything on request.
