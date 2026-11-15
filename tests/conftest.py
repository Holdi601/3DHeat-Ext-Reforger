import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
# The tests never ask GitHub for a newer release.
os.environ["HEAT3D_NO_UPDATE"] = "1"

# 3DHeat GameFiles, the library the readers build on: installed, or found where
# the tool looks for it from a plain checkout.
from heat3d_ext_reforger import library  # noqa: E402

if not library.ensure():
    raise SystemExit(library.MISSING)
