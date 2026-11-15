"""
Finding 3DHeat GameFiles, the library this tool reads with.

Installed by pip it is simply importable. From a plain checkout it is looked
for in `HEAT3D_GAMEFILES`, then in `../../gamefiles` (this tool inside a 3DHeat
checkout), then in `../3DHeat-GameFiles` (the two cloned side by side), and the
first folder holding `heat3d_gamefiles` goes on `sys.path`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

#: What to say when it is nowhere.
MISSING = (
    "needs 3DHeat GameFiles: pip install git+https://github.com/Holdi601/3DHeat-GameFiles.git, "
    "or set HEAT3D_GAMEFILES to its folder"
)


def candidates() -> list[Path]:
    repo = Path(__file__).resolve().parents[1]
    found = [Path(os.environ["HEAT3D_GAMEFILES"])] if os.environ.get("HEAT3D_GAMEFILES") else []
    return found + [repo.parent.parent / "gamefiles", repo.parent / "3DHeat-GameFiles"]


def ensure() -> bool:
    """True when `heat3d_gamefiles` can be imported, after looking for it if need be."""
    try:
        import heat3d_gamefiles

        # An empty folder of that name on the path imports as a namespace package.
        if getattr(heat3d_gamefiles, "__file__", None):
            return True
        del sys.modules["heat3d_gamefiles"]
    except ImportError:
        pass
    for folder in candidates():
        if (folder / "heat3d_gamefiles" / "__init__.py").is_file():
            sys.path.insert(0, str(folder))
            try:
                import heat3d_gamefiles  # noqa: F401

                return True
            except ImportError:
                sys.path.remove(str(folder))
    return False
