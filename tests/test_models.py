"""The model reader, the prefab reader and the vehicle builder on small models and prefabs made up here."""

import struct

import lz4.block
import numpy as np
import pytest

from heat3d_ext_reforger.enfusion import EnfusionError
from heat3d_ext_reforger.prefab import Chain, parse, ref
from heat3d_ext_reforger.vehicles import Builder, angles, merged_parts
from heat3d_ext_reforger.xob import Xob, colliders


def _form(chunks: list[tuple[bytes, bytes]]) -> bytes:
    body = b"XOB9" + b"".join(t + struct.pack(">I", len(d)) + d for t, d in chunks)
    return b"FORM" + struct.pack(">I", len(body)) + body


def make_xob(nodes, faces, positions, node_of_vertex=None, box=None) -> bytes:
    """A one-level model: `nodes` [(name, parent, (x, y, z))], one submesh (skinned when `node_of_vertex`)."""
    strings = ["paint", "{0000000000000001}paint.emat"] + [n for n, _p, _t in nodes]
    if box:
        strings += [box[0], "FireGeo", "armor_5mm.gamemat"]
    pool = b"".join(s.encode() + b"\0" for s in strings)
    head = bytearray(struct.pack("<I6f", 0, -10, -10, -10, 10, 10, 10))
    head += bytes(44 - len(head))
    head += struct.pack("<HHIII", 1, len(nodes), 1, 0, len(pool)) + pool
    head += struct.pack("<HH", 0, 1)
    children = {i: [k for k, (_n, p, _t) in enumerate(nodes) if p == i] for i in range(len(nodes))}
    for i, (_name, parent, t) in enumerate(nodes):
        sibs = children.get(parent, []) if parent >= 0 else [i]
        nxt = sibs[sibs.index(i) + 1] if sibs.index(i) + 1 < len(sibs) else -1
        first = children[i][0] if children[i] else -1
        head += struct.pack("<I3f4fhh", 2 + i, *t, 0, 0, 0, 1, nxt, first)
    faces = np.asarray(faces, np.uint16)
    pos = np.asarray(positions, np.float32)
    n, a = len(pos), len(faces)
    skinned = node_of_vertex is not None
    bones = sorted(set(node_of_vertex)) if skinned else []
    fmt = bytes([0, 0, 0, 0x1F if skinned else 0x0F])
    lo, hi = pos.min(0), pos.max(0)
    data = faces.tobytes() * 2
    if skinned:
        data += np.concatenate([pos, np.arange(n, dtype=np.uint32).view(np.float32)[:, None]], 1).astype(np.float32).tobytes()
    else:
        data += pos.tobytes()
    per_vertex = 24 if skinned else 20
    data += bytes((per_vertex - (16 if skinned else 12)) * n + 12 * n)
    if skinned:
        for k in range(n):
            data += bytes([bones.index(node_of_vertex[k]), 0, 0, 0]) + struct.pack("<3f", 1, 0, 0)
    packed = lz4.block.compress(data, store_size=False)
    assert len(data) <= 1 << 16
    lods_offset = 12 + 8 + 0  # filled below once the head's size is known
    lod = bytearray(b"LZO4" + struct.pack("<IIfI", 1, 0, 0.5, 0))
    sub = fmt + struct.pack("<6f", *lo, *hi) + bytes(16)
    sub += struct.pack("<HHHHHhHBBBBH", a, n, n, n if skinned else 0, 0, -1, 0, 1, len(bones), 0, 0, 0)
    sub += bytes(20) + bytes(bones)
    head_size = len(head) + len(lod) + 12 + len(sub)
    coll = b""
    if box:
        coll = struct.pack("<BBH9f3fIHHI3f", 3, 0, len(strings) - 2, 1, 0, 0, 0, 1, 0, 0, 0, 1, *box[1], 0,
                           len(strings) - 3, len(strings) - 1, 0, *box[2])
    lods_offset = 12 + 8 + head_size + (8 + len(coll) if coll else 0) + 8
    lod += struct.pack("<III", lods_offset, len(packed) + 4, len(data))
    head += lod + sub
    chunks = [(b"HEAD", bytes(head))]
    if coll:
        chunks.append((b"COLL", coll))
    chunks.append((b"LODS", struct.pack("<I", len(packed) | 0x80000000) + packed))
    return _form(chunks)


CUBE = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
TET = [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]


def test_nodes_levels_and_mesh():
    data = make_xob([("Scene_Root", -1, (0, 0, 0)), ("v_body", 0, (0, 1, 0)), ("v_turret", 1, (0, 0.5, 2))], TET, CUBE)
    x = Xob(data)
    assert [n.name for n in x.nodes] == ["Scene_Root", "v_body", "v_turret"]
    assert [n.parent for n in x.nodes] == [-1, 0, 1]
    assert np.allclose(x.nodes[2].world[:3, 3], [0, 1.5, 2])
    assert x.materials == [("paint", "{0000000000000001}paint.emat")]
    (m,) = x.mesh(0)
    assert m.material == "paint"
    assert np.allclose(m.positions, CUBE)
    assert m.faces.tolist() == TET


def test_skinned_vertices_follow_their_bone():
    data = make_xob([("Scene_Root", -1, (0, 0, 0)), ("v_body", 0, (0, 0, 0)), ("v_turret", 1, (0, 1, 0))], TET, CUBE,
                    node_of_vertex=[1, 1, 2, 2])
    (m,) = Xob(data).mesh(0)
    assert m.node.tolist() == [1, 1, 2, 2]


def test_not_a_model():
    with pytest.raises(EnfusionError):
        Xob(b"FORM\0\0\0\4TERR")


def test_box_collider():
    data = make_xob([("Scene_Root", -1, (0, 0, 0))], TET, CUBE, box=("UBX_FG_Engine", (0, 1, 2), (0.5, 0.25, 1)))
    (c,) = colliders(Xob(data))
    assert c.name == "UBX_FG_Engine" and c.layer == "FireGeo"
    assert np.allclose(c.positions.min(0), [-0.5, 0.75, 1]) and np.allclose(c.positions.max(0), [0.5, 1.25, 3])
    assert len(c.faces) == 12


PREFAB_BASE = """Vehicle : "{0000000000000002}Prefabs/Core.et" {
 components {
  MeshObject "{01}" {
   Object "{0000000000000003}Assets/Body.xob"
  }
  SlotManagerComponent "{02}" {
   Slots {
    RegisteringComponentSlotInfo Turret {
     PivotID "v_socket"
     Prefab "{0000000000000004}Prefabs/VehParts/Turret/Turret.et"
    }
    EntitySlotInfo Wheel_L01 {
     PivotID "v_wheel"
     Angles 0 180 0
     Prefab "{0000000000000005}Prefabs/VehParts/Wheels/Wheel.et"
    }
   }
  }
  SCR_VehicleDamageManagerComponent "{03}" {
   additionalHitZones {
    SCR_EngineHitZone Engine_01 {
     ColliderNames {
      "UBX_FG_Engine"
     }
    }
   }
  }
 }
}
"""
PREFAB = """Vehicle : "{0000000000000006}Prefabs/Base.et" {
 ID "1"
}
"""
TURRET = """Turret {
 components {
  MeshObject "{01}" {
   Object "{0000000000000007}Assets/Turret.xob"
  }
 }
}
"""
WHEEL = """Wheel {
 components {
  MeshObject "{01}" {
   Object "{0000000000000008}Assets/Wheel.xob"
  }
 }
}
"""


class FS(dict):
    def read(self, path):
        return self[path]


def test_prefab_blocks_and_chain():
    root = parse(PREFAB_BASE)
    assert root.blocks[0].kind == "Vehicle" and root.blocks[0].parent == "Prefabs/Core.et"
    assert ref('"{0000000000000003}Assets/Body.xob"') == "Assets/Body.xob"
    fs = FS({"Prefabs/Vehicle.et": PREFAB.encode(), "Prefabs/Base.et": PREFAB_BASE.encode()})
    chain = Chain(fs, "Prefabs/Vehicle.et")
    assert chain.model() == "Assets/Body.xob"
    slots = {s.name: s for s in chain.slots()}
    assert slots["Turret"].pivot == "v_socket" and slots["Wheel_L01"].angles == (0.0, 180.0, 0.0)
    assert chain.hit_zones() == {"Engine_01": ("SCR_EngineHitZone", ["UBX_FG_Engine"])}


def test_angles_turn_about_y_first():
    assert np.allclose(angles((0, 90, 0)) @ [0, 0, 1], [1, 0, 0])
    assert np.allclose(angles((90, 0, 0)) @ [0, 1, 0], [0, 0, 1])


def test_vehicle_parts_pivots_and_hit_zones():
    body = make_xob([("Scene_Root", -1, (0, 0, 0)), ("v_socket", 0, (0, 2, 1)), ("v_wheel", 0, (1, 0.5, 0))],
                    TET, [[-1, 0, -2], [1, 0, -2], [0, 2, 0], [0, 0, 2]], box=("UBX_FG_Engine", (0, 1, -1), (0.5, 0.5, 0.5)))
    turret = make_xob([("Scene_Root", -1, (0, 0, 0)), ("v_turret_01", 0, (0, 0.2, 0)), ("v_gun_01", 1, (0, 0.3, 0.5))],
                      TET, [[0, 0, 0], [0.5, 0, 0], [0, 0.4, 0], [0, 0.4, 1.5]], node_of_vertex=[1, 1, 2, 2])
    wheel = make_xob([("Scene_Root", -1, (0, 0, 0))], TET, CUBE)
    fs = FS({"Prefabs/Vehicle.et": PREFAB.encode(), "Prefabs/Base.et": PREFAB_BASE.encode(),
             "Prefabs/VehParts/Turret/Turret.et": TURRET.encode(), "Prefabs/VehParts/Wheels/Wheel.et": WHEEL.encode(),
             "Assets/Body.xob": body, "Assets/Turret.xob": turret, "Assets/Wheel.xob": wheel})
    b = Builder(fs).build("Prefabs/Vehicle.et")
    parts = merged_parts(b)
    assert set(parts) == {"hull", "turret", "gun", "gear"}
    # Pack frame: x forward (model z), y up, z right (model x).
    assert np.allclose(b.pivots["turret"], [1, 2.2, 0]) and np.allclose(b.pivots["gun"], [1.5, 2.5, 0])
    gear = parts["gear"][0]
    assert np.allclose(gear.min(0), [-1, 0.5, 0]) and np.allclose(gear.max(0), [0, 1.5, 1])  # turned 180 about y
    (zone,) = [d for d in b.dm if d[0] == "Engine_01"]
    assert zone[3]["group"] == "engine" and np.allclose(zone[1].mean(0), [-1, 1, 0])
    # The frame change mirrors; the triangles are turned so they keep facing the way they did.
    def volume(v, f):
        t = np.asarray(v, float)[np.asarray(f)]
        return np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum()

    v, f = parts["hull"]
    assert np.sign(volume(v, f)) == np.sign(volume([[-1, 0, -2], [1, 0, -2], [0, 2, 0], [0, 0, 2]], TET))
