"""
Enfusion models (`.xob`, `FORM`/`XOB9`): the node tree, the levels of detail and their triangle meshes.

Read from the files themselves; nothing here comes from the engine's tools. What the reader takes from a model:

- `HEAD`: the model's bounds, then a string pool (`u32` size at 56, strings from 60, each null-terminated), a
  table of two `u16` pool indices per material (name, resource path), the node tree, and one block per level of
  detail. Counts: `u16` materials at 44, `u16` nodes at 46, `u32` levels at 48.
- A node is 36 bytes: `u32` name (pool index), translation (3 `f32`), rotation quaternion (x, y, z, w), `i16` next
  sibling and `i16` first child (-1: none). Node 0 is the root; transforms are relative to the parent. Positions
  are metres with x to the model's right, y up and z forward.
- A level of detail: `LZO4`, `u32` submeshes, `u32` 0, `f32` switch distance, `u32` bone boxes,
  then the file offset, packed size and unpacked size of its data in the `LODS` chunk (LZ4 blocks, each with a
  `u32` length whose top bit marks the last). A submesh record: `u8[4]` vertex format, bounds (6 `f32`), 16 bytes,
  `u16` triangles, `u16` vertices, `u16` vertices with seams, `u16` skin records, `u16` 0, `i16` -1, `u16`
  material, `u8` UV sets, `u8` bones, `u8`, `u8`, `u16`, five `f32` per UV set (its range), and the submesh's
  bones (node indices). After the submeshes, the bone boxes: 28 bytes each (`u16` node, `u16`, bounds).
- A submesh's data, in order: two triangle lists of `u16` indices (the first over its vertices, the second over
  the seam-split ones), then the vertex streams and, last, 16 bytes per skin record (four `u8` bone slots, three
  `f32` weights; the fourth weight is what is left). Positions come first, 12 bytes each, or 16 when the submesh
  is skinned (the fourth `u32` is the vertex's skin record). The other streams' sizes follow from the format.

Only geometry is read: positions, the first triangle list, and which node each vertex follows.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass, field

import numpy as np

from .enfusion import EnfusionError, unlz4_blocks


@dataclass
class Node:
    name: str
    parent: int
    local: np.ndarray
    world: np.ndarray = field(repr=False)


@dataclass
class Submesh:
    fmt: bytes
    bounds: tuple
    triangles: int
    vertices: int
    split: int
    skins: int
    material: int
    uv_sets: int
    bones: list[int]

    @property
    def skinned(self) -> bool:
        return bool(self.fmt[3] & 0x10)

    def stream_bytes(self) -> int:
        """Bytes of the vertex streams and skin records after the two triangle lists."""
        f = self.fmt[3]
        per_vertex = 20 + 4 * bool(f & 0x80) + 4 * bool(f & 0x20) + 4 * bool(f & 0x10)
        per_split = 12 + 8 * bool(f & 0x80)
        return per_vertex * self.vertices + per_split * self.split + 16 * self.skins


@dataclass
class Lod:
    distance: float
    offset: int
    packed: int
    size: int
    submeshes: list[Submesh]


@dataclass
class Mesh:
    """One submesh of a level: positions (n, 3), triangles (m, 3) and the node each vertex follows."""

    submesh: Submesh
    material: str
    positions: np.ndarray
    faces: np.ndarray
    node: np.ndarray


def _quat(q) -> np.ndarray:
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def _chunks(data: bytes):
    at = 12
    while at + 8 <= len(data):
        tag, length = struct.unpack_from(">4sI", data, at)
        yield tag, at + 8, length
        at += 8 + length


class Xob:
    """A model read from its bytes; `mesh(level)` unpacks one level of detail."""

    def __init__(self, data: bytes) -> None:
        if data[:4] != b"FORM" or data[8:12] != b"XOB9":
            raise EnfusionError("not a model (FORM/XOB9)")
        self.data = data
        head = next((data[a : a + n] for tag, a, n in _chunks(data) if tag == b"HEAD"), None)
        if head is None or len(head) < 60:
            raise EnfusionError("a model without HEAD")
        try:
            self._read_head(head)
        except (struct.error, IndexError, ValueError) as exc:
            raise EnfusionError(f"a model's HEAD does not read: {exc}") from exc

    def _read_head(self, h: bytes) -> None:
        values = struct.unpack_from("<6f", h, 4)
        self.bounds = (np.array(values[:3]), np.array(values[3:]))
        nmat, nnode = struct.unpack_from("<HH", h, 44)
        (nlod,) = struct.unpack_from("<I", h, 48)
        (size,) = struct.unpack_from("<I", h, 56)
        pool = [s.decode("utf-8", "replace") for s in h[60 : 60 + size].split(b"\0")[:-1]]
        at = 60 + size
        table = struct.unpack_from(f"<{2 * nmat}H", h, at)
        at += 4 * nmat
        self.materials = [(pool[table[2 * i]], pool[table[2 * i + 1]]) for i in range(nmat)]
        raw = []
        for _ in range(nnode):
            (name,) = struct.unpack_from("<I", h, at)
            f = struct.unpack_from("<7f", h, at + 4)
            sib, child = struct.unpack_from("<hh", h, at + 32)
            local = np.eye(4)
            local[:3, :3] = _quat(f[3:])
            local[:3, 3] = f[:3]
            raw.append((pool[name] if name < len(pool) else f"node{len(raw)}", sib, child, local))
            at += 36
        parent = [-1] * nnode
        stack = [(0, -1)] if nnode else []
        seen = set()
        while stack:
            i, p = stack.pop()
            while 0 <= i < nnode and i not in seen:
                seen.add(i)
                parent[i] = p
                if raw[i][2] >= 0:
                    stack.append((raw[i][2], i))
                i = raw[i][1]
        self.nodes: list[Node] = []
        for i, (name, _s, _c, local) in enumerate(raw):
            p = parent[i]
            world = self.nodes[p].world @ local if 0 <= p < i else local
            self.nodes.append(Node(name, p, local, world))
        self.lods: list[Lod] = []
        for _ in range(nlod):
            if h[at : at + 4] != b"LZO4":
                raise EnfusionError("a level of detail without its LZO4 mark")
            n, _z, dist, nbox, off, packed, unpacked = struct.unpack_from("<IIfIIII", h, at + 4)
            at += 32
            subs = []
            for _ in range(n):
                fmt = h[at : at + 4]
                bounds = struct.unpack_from("<6f", h, at + 4)
                at += 44
                a, b, c, d, _e, _f, mat, uvs, nb = struct.unpack_from("<HHHHHhHBB", h, at)
                at += 20 + 20 * uvs
                bones = list(h[at : at + nb])
                at += nb
                subs.append(Submesh(fmt, bounds, a, b, c, d, mat, uvs, bones))
            at += 28 * nbox
            self.lods.append(Lod(dist, off, packed, unpacked, subs))

    def node_index(self, name: str) -> int:
        low = name.lower()
        return next((i for i, n in enumerate(self.nodes) if n.name.lower() == low), -1)

    def mesh(self, level: int = 0) -> list[Mesh]:
        lod = self.lods[level]
        raw = unlz4_blocks(self.data[lod.offset : lod.offset + lod.packed], lod.size)
        out = []
        at = 0
        for k, s in enumerate(lod.submeshes):
            lists = 12 * s.triangles
            stride = 16 if s.skinned else 12
            end = at + lists + s.stream_bytes()
            if end > len(raw):
                raise EnfusionError(f"submesh {k} of level {level} runs past its data")
            faces = np.frombuffer(raw, np.uint16, 3 * s.triangles, at).reshape(-1, 3).astype(np.int64)
            pos = np.frombuffer(raw, np.float32, s.vertices * stride // 4, at + lists).reshape(-1, stride // 4)
            positions = pos[:, :3].astype(np.float64)
            lo, hi = np.array(s.bounds[:3]), np.array(s.bounds[3:])
            pad = 1e-3 + 1e-4 * float(np.abs(hi - lo).max())
            if len(positions) and not (np.all(positions >= lo - pad) and np.all(positions <= hi + pad)):
                raise EnfusionError(f"submesh {k} of level {level}: positions outside its bounds")
            if len(faces) and faces.max() >= s.vertices:
                raise EnfusionError(f"submesh {k} of level {level}: an index past its vertices")
            node = np.zeros(s.vertices, np.int64)
            if s.skinned and s.skins and s.bones:
                skin = pos[:, 3].view(np.uint32).astype(np.int64)
                recs = np.frombuffer(raw, np.uint8, 16 * s.skins, end - 16 * s.skins).reshape(-1, 16)
                slots = recs[:, :4].astype(np.int64)
                w3 = recs[:, 4:16].copy().view(np.float32).reshape(-1, 3)
                weights = np.concatenate([w3, (1 - w3.sum(1))[:, None]], 1)
                best = slots[np.arange(len(recs)), weights.argmax(1)]
                bones = np.array(s.bones + [0], np.int64)
                best = bones[np.minimum(best, len(s.bones))]
                node = best[np.minimum(skin, len(recs) - 1)]
            elif s.bones:
                node[:] = s.bones[0]
            name = self.materials[s.material][0] if s.material < len(self.materials) else ""
            out.append(Mesh(s, name, positions, faces, node))
            at = end
        if at != len(raw):
            raise EnfusionError(f"level {level}: {len(raw) - at} bytes left after its submeshes")
        return out


@dataclass
class Collider:
    """A collision shape of the model: its name (`UBX_`, `UCX_`, `UCL_`, `UTM_`...), layer, the node it follows,
    and its surface in model space with the game material of each triangle."""

    name: str
    layer: str
    node: int
    positions: np.ndarray
    faces: np.ndarray
    materials: list[str]
    face_material: np.ndarray


def _box(half: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    s = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], np.float64) * half
    f = np.array([[0, 2, 1], [1, 2, 3], [4, 5, 6], [5, 7, 6], [0, 1, 4], [1, 5, 4],
                  [2, 6, 3], [3, 6, 7], [0, 4, 2], [2, 4, 6], [1, 3, 5], [3, 7, 5]], np.int64)
    return s, f


def _hull(p: np.ndarray) -> np.ndarray:
    try:
        from scipy.spatial import ConvexHull

        return ConvexHull(p).simplices.astype(np.int64)
    except Exception:  # noqa: BLE001 - flat or tiny shapes: no surface
        return np.zeros((0, 3), np.int64)


def colliders(x: Xob) -> list[Collider]:
    """The model's collision shapes (`COLL`). A record: `u8` shape (3 box, 4 convex, 7 capsule, `0x80` bit: a
    triangle mesh), `u8` node, `u16` layer name, a 3x3 rotation and a translation, `u32`, `u16` name, `u16` game
    material, `u32`; then a box's half extents, a capsule's radius and half length, a convex's counts (`u16`
    vertices, faces, edges, indices) and vertices, or a mesh's `u16` vertices, `u16` triangles, `u32` materials,
    (`u16` material, `u16` last triangle) per material, the vertices and `u16` triangles."""
    data = x.data
    body = next((data[a : a + n] for tag, a, n in _chunks(data) if tag == b"COLL"), b"")
    head = next(data[a : a + n] for tag, a, n in _chunks(data) if tag == b"HEAD")
    (size,) = struct.unpack_from("<I", head, 56)
    pool = [s.decode("utf-8", "replace") for s in head[60 : 60 + size].split(b"\0")[:-1]]
    names = {i for i, s in enumerate(pool) if re.match(r"U[A-Z]{2}_", s)}
    found: dict[int, Collider] = {}
    for i in names:
        key = struct.pack("<H", i)
        at = body.find(key, 56)
        while at >= 0:
            o = at - 56
            if o + 76 <= len(body) and (body[o] & 0x7F) in (1, 2, 3, 4, 5, 6, 7, 8) and o not in found:
                c = _collider(body, o, pool)
                if c is not None:
                    found[o] = c
            at = body.find(key, at + 1)
    return [found[o] for o in sorted(found)]


def _collider(b: bytes, o: int, pool: list[str]) -> Collider | None:
    shape, node, layer = b[o], b[o + 1], struct.unpack_from("<H", b, o + 2)[0]
    rot = np.array(struct.unpack_from("<9f", b, o + 4), np.float64).reshape(3, 3)
    if layer >= len(pool) or not np.allclose(rot @ rot.T, np.eye(3), atol=1e-3):
        return None
    move = np.array(struct.unpack_from("<3f", b, o + 40), np.float64)
    name, mat = struct.unpack_from("<HH", b, o + 56)
    if name >= len(pool):
        return None
    mats = [pool[mat] if mat < len(pool) else ""]
    fm = None
    try:
        if shape & 0x80:
            nv, nt, nm = struct.unpack_from("<HHI", b, o + 64)
            if nm > 256:
                return None
            tab = struct.unpack_from(f"<{2 * nm}H", b, o + 72)
            at = o + 72 + 4 * nm
            p = np.frombuffer(b, np.float32, 3 * nv, at).reshape(-1, 3).astype(np.float64)
            f = np.frombuffer(b, np.uint16, 3 * nt, at + 12 * nv).reshape(-1, 3).astype(np.int64)
            if len(f) and f.max() >= nv:
                return None
            mats = [pool[tab[2 * k]] if tab[2 * k] < len(pool) else "" for k in range(nm)]
            fm = np.zeros(len(f), np.int64)
            start = 0
            for k in range(nm):
                fm[start : tab[2 * k + 1] + 1] = k
                start = tab[2 * k + 1] + 1
        elif shape == 3:
            p, f = _box(np.array(struct.unpack_from("<3f", b, o + 64), np.float64))
        elif shape == 7:
            r, half = struct.unpack_from("<2f", b, o + 64)
            p, f = _box(np.array([r, half + r, r], np.float64))
        elif shape == 4:
            nv = struct.unpack_from("<H", b, o + 64)[0]
            if not 4 <= nv <= 4096:
                return None
            p = np.frombuffer(b, np.float32, 3 * nv, o + 72).reshape(-1, 3).astype(np.float64)
            f = _hull(p)
        else:
            return None
    except (struct.error, ValueError):
        return None
    if not np.all(np.isfinite(p)) or np.abs(p).max(initial=0) > 1e4:
        return None
    p = p @ rot.T + move
    return Collider(pool[name], pool[layer], node, p, f, mats, fm if fm is not None else np.zeros(len(f), np.int64))
