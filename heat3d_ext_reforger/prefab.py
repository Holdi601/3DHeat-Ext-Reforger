"""
Enfusion prefabs (`.et`, text): what the `models` command takes from them.

A prefab is a tree of blocks, `Class [name] [: "{GUID}parent.et"] {`, holding lines `Key value ...` and further
blocks. A prefab inherits from the prefab its root block names; a derived prefab overrides its parent's slots,
hit zones and model line by line. `Prefab` reads one file into blocks and `Chain` follows the parents and answers,
child first:

- `model()`: the `.xob` its `MeshObject` draws;
- `slots()`: the entity slots (`SlotManagerComponent` and the compartment, turret and wheel slot lists), each
  with the node it hangs on (`PivotID`), its `Offset` and `Angles`, and the prefab it holds;
- `hit_zones()`: each hit zone's class and the collider names it covers (`ColliderNames`);
- `weapons()`: the weapons the turret's `WeaponSlotComponent`s hold, with their node and offset.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .enfusion import EnfusionError

_REF = re.compile(r'^"(?:\{[0-9A-Fa-f]{16}\})?([^"]*)"$')
_TOKEN = re.compile(r'"[^"]*"|[^\s"]+')


def ref(value: str) -> str:
    """A resource reference without its GUID: `"{ABC...}Prefabs/x.et"` -> `Prefabs/x.et`."""
    m = _REF.match(value.strip())
    return m.group(1) if m else value.strip().strip('"')


@dataclass
class Block:
    kind: str
    name: str = ""
    parent: str = ""
    props: dict[str, list[str]] = field(default_factory=dict)
    blocks: list["Block"] = field(default_factory=list)

    def walk(self):
        yield self
        for b in self.blocks:
            yield from b.walk()

    def get(self, key: str) -> str:
        v = self.props.get(key)
        return v[0] if v else ""

    def values(self) -> list[str]:
        """Every quoted value in this block's lines (a list block like `ColliderNames { "a" "b" }`)."""
        out = []
        for k, v in self.props.items():
            for x in [k, *v]:
                if x.startswith('"'):
                    out.append(x.strip('"'))
        return out


def parse(text: str) -> Block:
    root = Block("file")
    stack = [root]
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line == "}":
            if len(stack) > 1:
                stack.pop()
            continue
        if line.endswith("{"):
            head = _TOKEN.findall(line[:-1])
            b = Block(head[0] if head else "")
            rest = head[1:]
            if ":" in rest:
                i = rest.index(":")
                b.parent = ref(rest[i + 1]) if i + 1 < len(rest) else ""
                rest = rest[:i]
            rest = [r for r in rest if r != "+"]
            b.name = rest[0].strip('"') if rest else ""
            stack[-1].blocks.append(b)
            stack.append(b)
            continue
        toks = _TOKEN.findall(line)
        if toks:
            stack[-1].props.setdefault(toks[0], toks[1:])
    return root


def _vec(b: Block, key: str) -> tuple[float, float, float] | None:
    v = b.props.get(key)
    if not v or len(v) < 3:
        return None
    try:
        return float(v[0]), float(v[1]), float(v[2])
    except ValueError:
        return None


@dataclass
class Slot:
    name: str
    pivot: str = ""
    offset: tuple = (0.0, 0.0, 0.0)
    angles: tuple = (0.0, 0.0, 0.0)
    prefab: str = ""


_SLOT_KINDS = re.compile(r"SlotInfo$|^EntitySlotInfo$")


class Chain:
    """A prefab and its parents, read through `fs` (anything with `read(path) -> bytes`)."""

    def __init__(self, fs, path: str, depth: int = 16) -> None:
        self.path = path
        self.files: list[Block] = []
        self.texts: list[str] = []
        seen = set()
        while path and depth > 0 and path.lower() not in seen:
            seen.add(path.lower())
            try:
                text = fs.read(path).decode("utf-8", "replace")
            except (FileNotFoundError, KeyError, EnfusionError):
                break
            root = parse(text)
            self.texts.append(text)
            self.files.append(root)
            top = root.blocks[0] if root.blocks else None
            path = top.parent if top else ""
            depth -= 1

    def model(self) -> str:
        for f in self.files:
            for b in f.walk():
                if b.kind == "MeshObject" and b.get("Object"):
                    return ref(b.get("Object"))
        return ""

    def slots(self) -> list[Slot]:
        merged: dict[str, Slot] = {}
        order: list[str] = []
        for f in reversed(self.files):  # parents first, children override
            for b in f.walk():
                if not _SLOT_KINDS.search(b.kind) or not b.name or b.kind.endswith("CompartmentSlot"):
                    continue
                s = merged.get(b.name)
                if s is None:
                    s = merged[b.name] = Slot(b.name)
                    order.append(b.name)
                if b.get("PivotID"):
                    s.pivot = b.get("PivotID").strip('"')
                s.offset = _vec(b, "Offset") or s.offset
                s.angles = _vec(b, "Angles") or s.angles
                if b.get("Prefab"):
                    s.prefab = ref(b.get("Prefab"))
        return [merged[n] for n in order if merged[n].prefab]

    def hit_zones(self) -> dict[str, tuple[str, list[str]]]:
        """{hit zone: (class, collider names)}, child first."""
        out: dict[str, tuple[str, list[str]]] = {}
        for f in self.files:
            for b in f.walk():
                if not b.kind.endswith("HitZone") or not b.name or b.name in out:
                    continue
                names: list[str] = []
                for c in b.blocks:
                    if c.kind == "ColliderNames":
                        names += c.values()
                out[b.name] = (b.kind, names)
        return {k: v for k, v in out.items() if v[1]}

    def weapons(self) -> list[Slot]:
        out = []
        seen = set()
        for f in self.files:
            for b in f.walk():
                if b.kind != "WeaponSlotComponent" or b.name in seen:
                    continue
                seen.add(b.name)
                tmpl = ref(b.get("WeaponTemplate")) if b.get("WeaponTemplate") else ""
                s = Slot(b.name, prefab=tmpl)
                for c in b.blocks:
                    if c.kind == "AttachType":
                        s.pivot = c.get("PivotID").strip('"')
                        s.offset = _vec(c, "Offset") or s.offset
                        s.angles = _vec(c, "Angles") or s.angles
                if tmpl:
                    out.append(s)
        return out

    def first(self, kind: str, key: str) -> str:
        for f in self.files:
            for b in f.walk():
                if b.kind == kind and b.get(key):
                    return b.get(key)
        return ""
