"""Write docs/cli-reference.md from the code itself, so the reference cannot drift.

The options come from the program's own `--help` for every verb; the level's
parts from the part names the code gives them.

    python tools/gen_docs_reference.py          # rewrite the page
    python tools/gen_docs_reference.py --check  # exit 1 when the page is stale
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "cli-reference.md"
COMMAND = "heat3d-reforger-maps"
PACKAGE = "heat3d_ext_reforger"
VERBS = ["worlds", "world", "identify"]


def run(args):
    env = dict(os.environ, HEAT3D_NO_UPDATE="1", COLUMNS="88", PYTHONIOENCODING="utf-8",
               PYTHONPATH=str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    r = subprocess.run([sys.executable, "-m", PACKAGE] + args, capture_output=True, text=True,
                       env=env, encoding="utf-8", cwd=ROOT)
    return (r.stdout or r.stderr).rstrip()


def outputs():
    return ["### `.glb` parts", "",
            "`ground:<world>` (the terrain, in the colours of its supertexture tiles), `water:<world>` (the sea, "
            "at height zero) and `structure:<world>` (a box per placed model; trees and vegetation only with "
            "`--trees`), where `<world>` is the last part of the world's name as `worlds` prints it.", "",
            "`asset.generator`: `heat3d_gamefiles` (the glTF writer of 3DHeat GameFiles).", "",
            "`enfusion-worlds` and `enfusion-world` are the same verbs as `worlds` and `world`, under the names "
            "3DHeat GameFiles gave them.", ""]


def build():
    out = ["---", "title: Command reference", "nav_order: 90", "---", "", "# Command reference", "",
           "Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.",
           "The other pages explain each command step by step.", "",
           f"## `{COMMAND}`", "", "```text", run(["--help"]), "```", ""]
    for v in VERBS:
        out += [f"## `{v}`", "", "```text", run([v, "--help"]), "```", ""]
    out += ["## Output", ""]
    return "\n".join(out + outputs())


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text(encoding="utf-8") == text else 1)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT))
