"""
Arma Reforger's vehicles as a local model pack (`models` command): each vehicle prefab of the catalogue built from
its own models, in the parts the 3DHeat viewer moves.

A vehicle is its prefab's model (`MeshObject`) plus what its slots hold: wheels, the turret, rotors, doors, roofs,
cargo boxes and glass, each hung on its node (`PivotID`) with the slot's offset and angles; a turret's weapons
hang on its gun node. Cockpit panels, seats, lights, characters and items are left out, and so are the interior
and proxy surfaces of each model (materials named `interior`, `decal`, `m_PRT_`, `WaterErase`...).

Parts: what follows a wheel or track node or sits in a wheel slot is `gear`; the turret slot's model (or, without
one, what follows the model's own turret node) is `turret`, pivoting on its turret node; what follows a gun or
barrel node under it, and the weapons, are `gun`, pivoting on the gun node; a helicopter's main rotor is `rotor`.
The rest is the `hull`.

Hit regions (`dm`): each hit zone of the prefabs (`ColliderNames`) as the surface of its colliders, and the
armour of the hull's triangle-mesh colliders split by game material, as `armour_<n>mm` plates with their
thickness.

The model's own frame is x right, y up, z forward (left-handed); the pack's is x forward, y up, z right, so the
triangles' order is turned to keep them facing out.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field

import numpy as np

from .enfusion import EnfusionError
from .prefab import Chain, Slot
from .xob import Xob, colliders

#: Surfaces that are not the vehicle's outside.
SKIP_MATERIAL = re.compile(r"interior|_int(_|$)|decal|m_PRT_|WaterErase|MLOD|shadow|proxy|_LOD", re.I)
#: Slot prefabs that are not part of the outside shape.
SKIP_SLOT = re.compile(r"/Lights/|/Dst/|Character|/Items/|Magazine|Emissive|Probe|Supply|shadow|Sound|VirtualSlot|"
                       r"/Ammo/|Grenade|Launcher|Cockpit|Pedals|Shifter|SteeringWheel|/Seats/|seats|TieDown|antenna|"
                       r"periscope|Coordinator|commander|CoatOfArms|decal", re.I)
GEAR_NODE = re.compile(r"wheel|tire|tyre|track|sprocket|idler|roadwheel", re.I)
TURRET_NODE = re.compile(r"^v_turret(_0?1)?$|^v_turret_?base$|^turret$", re.I)
GUN_NODE = re.compile(r"^v_gun(_0?1)?$|^v_cannon|^v_barrel|^gun$|^v_weapon(_0?1)?$", re.I)
TAIL_NODE = re.compile(r"tail", re.I)
ROTOR_NODE = re.compile(r"^v_rotor$|^v_rotor_main|^v_main_?rotor|^v_mainrotor", re.I)
#: Hit zone classes by the game's class name.
ZONE_GROUP = (("Engine", "engine"), ("Fuel", "fuel"), ("Gearbox", "transmission"), ("Battery", "electrics"),
              ("Wheel", "wheel"), ("Rotor", "rotor"), ("Turret", "turret"), ("Ammo", "ammo"), ("Barrel", "gun"),
              ("Gun", "gun"), ("Crew", "crew"), ("Flammable", "hull"), ("Hull", "hull"))
#: The most triangles a model is read with: the most detailed level of detail within it (the pack simplifies
#: further). Attached models (turrets, weapons, wheels) get less than the vehicle's own.
MAIN_TRIANGLES = 90_000
PART_TRIANGLES = 20_000
GUN_TRIANGLES = 6_000


def angles(a) -> np.ndarray:
    """Enfusion `Angles x y z` (degrees, about x, y, z) as a rotation: yaw, then pitch, then roll."""
    x, y, z = (math.radians(v) for v in a)
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return ry @ rx @ rz


def place(m: np.ndarray, p: np.ndarray) -> np.ndarray:
    return p @ m[:3, :3].T + m[:3, 3]


def frame(p: np.ndarray) -> np.ndarray:
    """Model frame (x right, y up, z forward) to the pack's (x forward, y up, z right)."""
    return np.asarray(p, np.float64)[..., [2, 1, 0]]


@dataclass
class Built:
    parts: dict = field(default_factory=dict)
    pivots: dict = field(default_factory=dict)
    dm: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    models: list = field(default_factory=list)

    def add(self, part: str, v: np.ndarray, f: np.ndarray) -> None:
        if len(f):
            self.parts.setdefault(part, []).append((v, f))

    def add_dm(self, name: str, v: np.ndarray, f: np.ndarray, extras: dict) -> None:
        """A hit region; one of the same name (the hull's and the turret's armour of one thickness) joins it."""
        for k, (n, v0, f0, ex) in enumerate(self.dm):
            if n == name:
                self.dm[k] = (n, *_merge([v0, v], [f0, f]), ex)
                return
        self.dm.append((name, v, f, extras))


class Builder:
    """Builds vehicles from an install's file system, keeping models it has read."""

    def __init__(self, fs) -> None:
        self.fs = fs
        self._xob: dict[str, Xob | None] = {}
        self._mesh: dict[str, list] = {}

    def xob(self, path: str) -> Xob | None:
        key = path.lower()
        if key not in self._xob:
            try:
                self._xob[key] = Xob(self.fs.read(path))
            except (FileNotFoundError, KeyError, EnfusionError):
                self._xob[key] = None
        return self._xob[key]

    def meshes(self, path: str, most: int = MAIN_TRIANGLES) -> list:
        key = (path.lower(), most)
        if key not in self._mesh:
            x = self.xob(path)
            out = []
            if x is not None and x.lods:
                sizes = [sum(s.triangles for s in lod.submeshes) for lod in x.lods]
                level = next((i for i, n in enumerate(sizes) if n <= most), len(sizes) - 1)
                try:
                    out = [m for m in x.mesh(level) if not SKIP_MATERIAL.search(m.material)]
                except EnfusionError:
                    out = []
            self._mesh[key] = out
        return self._mesh[key]

    # --- one vehicle -------------------------------------------------------------------------------------------

    def build(self, prefab: str) -> Built:
        out = Built()
        chain = Chain(self.fs, prefab)
        model = chain.model()
        if not model:
            raise EnfusionError("the prefab names no model")
        x = self.xob(model)
        if x is None:
            raise EnfusionError(f"{model}: not readable")
        out.models.append(model)
        slots = [s for s in chain.slots() if not SKIP_SLOT.search(s.prefab)]
        turret_slot = next((s for s in slots if re.search(r"turret", _leaf(s.prefab), re.I)), None)
        own_turret = turret_slot is None
        self._model(out, model, np.eye(4), "hull", own_turret=own_turret, main=True)
        for s in slots:
            self._slot(out, x, np.eye(4), s, "turret" if s is turret_slot else _role(s.prefab, "hull"))
        self._zones(out, chain, model, np.eye(4))
        return out

    def _pivot(self, x: Xob, at: np.ndarray, s: Slot) -> np.ndarray:
        i = x.node_index(s.pivot) if s.pivot else -1
        m = at @ (x.nodes[i].world if i >= 0 else np.eye(4))
        local = np.eye(4)
        local[:3, :3] = angles(s.angles)
        local[:3, 3] = s.offset
        return m @ local

    def _slot(self, out: Built, x: Xob, at: np.ndarray, s: Slot, role: str, depth: int = 0) -> None:
        if depth > 3:
            return
        chain = Chain(self.fs, s.prefab)
        model = chain.model()
        if not model or self.xob(model) is None:
            return
        m = self._pivot(x, at, s)
        out.models.append(model)
        self._model(out, model, m, role, own_turret=(role == "turret"))
        child = self.xob(model)
        for sub in chain.slots():
            if SKIP_SLOT.search(sub.prefab):
                continue
            self._slot(out, child, m, sub, _role(sub.prefab, role if role != "rotor" else "hull"), depth + 1)
        if role == "turret":
            gun = out.pivots.get("_gun_node", "")
            for w in chain.weapons():
                if not w.pivot:
                    w.pivot = gun
                self._slot(out, child, m, w, "gun", depth + 1)
            self._zones(out, chain, model, m)

    def _model(self, out: Built, model: str, m: np.ndarray, role: str, own_turret: bool, main: bool = False) -> None:
        x = self.xob(model)
        if x is None:
            return
        names = [n.name for n in x.nodes]
        cls = np.array([role] * len(names), dtype=object)
        if role in ("hull", "turret"):
            turret = next((i for i, n in enumerate(names) if TURRET_NODE.search(n)), -1) if own_turret else -1
            gun = -1
            if own_turret:
                gun = next((i for i, n in enumerate(names) if GUN_NODE.search(n) and self._under(x, i, turret)), -1)
            for i, n in enumerate(names):
                if GEAR_NODE.search(n) or self._under_match(x, i, GEAR_NODE):
                    cls[i] = "gear"
                elif main and self._under_match(x, i, ROTOR_NODE) and not self._under_match(x, i, TAIL_NODE):
                    cls[i] = "rotor"
                elif gun >= 0 and self._under(x, i, gun):
                    cls[i] = "gun"
                elif turret >= 0 and self._under(x, i, turret):
                    cls[i] = "turret"
            if turret >= 0 and "turret" not in out.pivots:
                out.pivots["turret"] = frame(place(m, x.nodes[turret].world[:3, 3]))
            if gun >= 0 and "gun" not in out.pivots:
                out.pivots["gun"] = frame(place(m, x.nodes[gun].world[:3, 3]))
                out.pivots["_gun_node"] = names[gun]
            if main:
                rotor = next((i for i, n in enumerate(names) if ROTOR_NODE.search(n)), -1)
                if rotor >= 0 and "rotor" not in out.pivots:
                    out.pivots["rotor"] = frame(place(m, x.nodes[rotor].world[:3, 3]))
        elif role == "rotor" and "rotor" not in out.pivots:
            out.pivots["rotor"] = frame(m[:3, 3])
        most = MAIN_TRIANGLES if main else GUN_TRIANGLES if role == "gun" else PART_TRIANGLES
        for mesh in self.meshes(model, most):
            p = frame(place(m, mesh.positions))
            f = mesh.faces[:, ::-1]  # the frame change mirrors: turn the triangles back outward
            node = np.minimum(mesh.node, len(cls) - 1) if len(cls) else np.zeros(len(p), np.int64)
            vcls = cls[node] if len(cls) else np.array([role] * len(p), dtype=object)
            fcls = vcls[f[:, 0]]
            for part in set(fcls.tolist()):
                out.add(part, p, f[fcls == part])

    @staticmethod
    def _under(x: Xob, i: int, root: int) -> bool:
        if root < 0:
            return False
        while i >= 0:
            if i == root:
                return True
            i = x.nodes[i].parent
        return False

    @staticmethod
    def _under_match(x: Xob, i: int, rx: re.Pattern) -> bool:
        while i >= 0:
            if rx.search(x.nodes[i].name):
                return True
            i = x.nodes[i].parent
        return False

    def _zones(self, out: Built, chain: Chain, model: str, m: np.ndarray) -> None:
        x = self.xob(model)
        if x is None:
            return
        try:
            cols = colliders(x)
        except (EnfusionError, ValueError, IndexError):
            return
        by = {c.name.lower(): c for c in cols}
        for zone, (kind, names) in chain.hit_zones().items():
            vs, fs = [], []
            for n in names:
                c = by.get(n.lower())
                if c is not None and len(c.faces):
                    vs.append(frame(place(m, c.positions)))
                    fs.append(c.faces)
            if not vs:
                continue
            v, f = _merge(vs, fs)
            group = next((g for k, g in ZONE_GROUP if k.lower() in kind.lower()), "module")
            out.add_dm(zone, v, f, {"part": zone, "group": group, "class": kind})
        # The armour: triangle-mesh colliders of the fire geometry, one plate set per game material.
        plates: dict[str, list] = {}
        for c in cols:
            if not re.match(r"UTM_", c.name) or "fire" not in c.layer.lower():
                continue
            for k, mat in enumerate(c.materials):
                sel = c.faces[c.face_material == k]
                if len(sel):
                    plates.setdefault(mat, []).append((frame(place(m, c.positions)), sel))
        for mat, items in plates.items():
            mm = re.search(r"(\d+(?:\.\d+)?)\s*mm", mat)
            label = re.sub(r"\.gamemat$", "", mat.split("/")[-1])
            v, f = _merge([a for a, _ in items], [b for _, b in items])
            ex = {"part": label, "group": "armour" if "armor" in mat.lower() else "structure", "material": label}
            if mm:
                ex["thickness"] = float(mm.group(1))
            out.add_dm(f"armour_{label}", v, f, ex)


def _leaf(prefab: str) -> str:
    """A prefab's folder and file name (`Wheels/BTR70_wheel_left_01.et`): what its role is read from."""
    return "/".join(prefab.split("/")[-2:])


def _role(prefab: str, default: str) -> str:
    leaf = _leaf(prefab)
    if re.search(r"wheel|track", leaf, re.I):
        return "gear"
    if re.search(r"rotor_?main|main_?rotor", leaf, re.I):
        return "rotor"
    return default


def _merge(vs: list, fs: list) -> tuple[np.ndarray, np.ndarray]:
    at, ff = 0, []
    for v, f in zip(vs, fs):
        ff.append(np.asarray(f, np.int64) + at)
        at += len(v)
    return np.concatenate(vs), np.concatenate(ff)


def merged_parts(b: Built) -> dict:
    return {k: _merge([v for v, _ in items], [f for _, f in items]) for k, items in b.parts.items()}


def fingerprint(fs, b: Built, prefab_texts: list[str]) -> str:
    """What a vehicle is built from: its models' sizes and the prefab texts that place them."""
    h = hashlib.sha256()
    for model in sorted(set(b.models)):
        h.update(model.lower().encode())
        try:
            h.update(str(len(fs.read(model))).encode())
        except (FileNotFoundError, KeyError, EnfusionError):
            pass
    for t in prefab_texts:
        h.update(t.encode())
    return h.hexdigest()[:20]


def geometry_key(b: Built) -> str:
    """Two prefabs with the same models in the same places share one file."""
    h = hashlib.sha256()
    for k in sorted(b.parts):
        for v, f in b.parts[k]:
            h.update(k.encode())
            h.update(np.round(np.asarray(v, np.float64).sum(0), 3).tobytes())
            h.update(str(len(f)).encode())
    for name, v, f, _ex in b.dm:
        h.update(name.encode())
        h.update(str(len(f)).encode())
    return h.hexdigest()[:20]
