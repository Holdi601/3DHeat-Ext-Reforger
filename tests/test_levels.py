"""status / all / layouts on made-up data: string table, place names, scenario objectives, fingerprints, manifest."""

from __future__ import annotations

import json
from pathlib import Path

from heat3d_ext_reforger import layouts, levels, manifest
from heat3d_ext_reforger.enfusion import Entry
from heat3d_ext_reforger.enfusionworld import Entity, World


class FakeFS:
    def __init__(self, files: dict[str, bytes], archive: Path = Path("data.pak")) -> None:
        self.data = {k.lower(): v for k, v in files.items()}
        self.names = {k.lower(): k for k in files}
        self.files = {k.lower(): Entry(archive, i * 100, len(v), len(v), 0) for i, (k, v) in enumerate(files.items())}

    def __contains__(self, path: str) -> bool:
        return path.lower() in self.data

    def read(self, path: str) -> bytes:
        if path.lower() not in self.data:
            raise FileNotFoundError(path)
        return self.data[path.lower()]

    def find(self, contains: str, suffix: str = "") -> list[str]:
        return sorted(self.names[p] for p in self.data if contains.lower() in p and p.endswith(suffix.lower()))


TABLE = b'StringTableRuntime {\n Ids {\n  "AR-MapLocation_Gravette"\n  "AR-MapLocation_HuntsmansHeath"\n }\n Texts {\n  "Gravette"\n  "Huntsman\'s Heath"\n }\n}\n'


def _prefab(parent: str, extra: str = "") -> bytes:
    return f'GenericEntity : "{{0000000000000001}}{parent}" {{\n components {{\n  SCR_MapDescriptorComponent "{{1}}" {{\n{extra}  }}\n }}\n}}\n'.encode()


def test_string_table_and_names():
    fs = FakeFS({"Language/localization.en_us.conf": TABLE})
    strings = layouts.string_table(fs)
    assert strings == {"AR-MapLocation_Gravette": "Gravette", "AR-MapLocation_HuntsmansHeath": "Huntsman's Heath"}
    assert layouts._name_of("G_HuntsmansHeath", "", False, strings) == "Huntsman's Heath"
    assert layouts._name_of("C_LocationGravette", "", False, strings) == "Gravette"
    assert layouts._name_of("S_Redon", "#AR-MapLocation_Camurac", True, strings) == "Redon"


def test_places_typed_by_prefab_chain():
    common = "Prefabs/World/Locations/Common"
    fs = FakeFS({
        "Language/localization.en_us.conf": TABLE,
        f"{common}/Urban/LocationUrbanTown.et": _prefab(f"{common}/LocationBase.et", '   MainType "Name Town"\n'),
        f"{common}/Urban/LocationUrbanGeneric_Airport.et": _prefab(f"{common}/LocationBase.et"),
        f"{common}/Natural/LocationNaturalHill.et": _prefab(f"{common}/LocationBase.et"),
        "Prefabs/World/Locations/Test/Gravette.et": _prefab(f"{common}/Urban/LocationUrbanTown.et", '   DisplayName "#AR-MapLocation_Gravette"\n'),
        "Prefabs/World/Locations/Test/Airport.et": _prefab(f"{common}/Urban/LocationUrbanGeneric_Airport.et"),
        "Prefabs/World/Locations/Test/Hill.et": _prefab(f"{common}/Natural/LocationNaturalHill.et"),
        f"{common}/Aquatic/LocationAquaticSeaMinor.et": _prefab(f"{common}/LocationBase.et"),
        # a bay whose own prefab is named after the airport beside it is still a bay
        "Prefabs/World/Locations/Test/Airport_Bay_01.et": _prefab(f"{common}/Aquatic/LocationAquaticSeaMinor.et"),
    })
    w = World([], [], [
        Entity("GenericEntity", "Prefabs/World/Locations/Test/Gravette.et", "C_LocationGravette", {"coords": (10.0, 5.0, 20.0)}, None),
        Entity("GenericEntity", "Prefabs/World/Locations/Test/Airport.et", "G_Airport", {"coords": (30.0, 4.0, 40.0)}, None),
        Entity("GenericEntity", "Prefabs/World/Locations/Test/Hill.et", "H_LongHill", {"coords": (50.0, 90.0, 60.0)}, None),
        Entity("GenericEntity", "Prefabs/World/Locations/Test/Airport_Bay_01.et", "B_MaidensBay", {"coords": (70.0, 0.0, 80.0)}, None),
        Entity("GenericEntity", "Prefabs/Structures/House.et", "house", {"coords": (1.0, 1.0, 1.0)}, None),
    ])
    got = {p["name"]: p for p in layouts.places(fs, {}, w, layouts.string_table(fs))}
    assert got["Gravette"]["type"] == "town" and got["Gravette"]["kind"] == "town" and got["Gravette"]["position"] == [10.0, 5.0, 20.0]
    assert got["Airport"]["type"] == "airfield"
    assert got["Long Hill"]["type"] == "place" and got["Long Hill"]["kind"] == "hill"
    assert got["Maidens Bay"]["type"] == "place" and got["Maidens Bay"]["kind"] == "water"
    assert len(got) == 4


def test_scenario_objectives():
    w = World([], [], [
        Entity("GenericEntity", "Prefabs/Systems/MilitaryBase/ConflictMilitaryBase.et", "MilitaryBaseLevie", {"coords": (1.0, 2.0, 3.0), "angles": (0.0, 90.0, 0.0)}, None),
        Entity("GenericEntity", "Prefabs/Systems/MilitaryBase/ConflictMilitaryBase.et", "MilitaryBaseAirfield", {"coords": (4.0, 5.0, 6.0)}, None),
        Entity("GenericEntity", "Prefabs/Systems/MilitaryBase/ConflictRelayRadio.et", "Relay1", {"coords": (7.0, 8.0, 9.0)}, None),
        Entity("GenericEntity", "Prefabs/Compositions/Locations/Eden/SupplyCache_Morton_FIA_01.et", None, {"coords": (1.0, 1.0, 1.0)}, None),
        Entity("SCR_SpawnPoint", "Prefabs/MP/Campaign/CampaignSpawnpoint_FIA.et", None, {"coords": (2.0, 2.0, 2.0)}, None),
        Entity("GenericEntity", "Prefabs/Systems/AmbientVehicles/AmbientVehicleSpawnpoint_US.et", None, {"coords": (3.0, 3.0, 3.0)}, None),
        Entity("GenericEntity", "Prefabs/MP/Campaign/CampaignSpawnpoint_US.et", None, {"coords": (0.5, 0.5, 0.5)}, 0),
    ])
    objectives, spawns, dropped = layouts.scenario(FakeFS({}), {}, w, {})
    kinds = {(o["type"], o.get("kind"), o["name"]) for o in objectives}
    assert ("base", "military", "Levie") in kinds and ("airfield", "military", "Airfield") in kinds
    assert ("objective", "relay", "Relay1") in kinds and ("objective", "supply_cache", "Morton") in kinds
    assert [(s["type"], s["team"], s["rule"]) for s in spawns] == [("spawn", 3, "team"), ("vehicle_spawn", 1, "ambient")]
    assert dropped == {"inside a composition": 1}


def test_scenario_files():
    fs = FakeFS({p: b"" for p in ("worlds/Eden/Eden.ent", "worlds/Eden/EmptyEden.ent", "worlds/MP/CTI_Campaign_Eden.ent",
                                  "worlds/GameMaster/GM_Eden.ent", "worlds/Rally_Eden_Base.ent", "worlds/CaptureAndHold/CAH_Arland1.ent",
                                  "worlds/Editor/Slots/AssetImages/Eden_AssetImages.ent")})
    assert layouts.scenario_files(fs, "Eden") == ["worlds/GameMaster/GM_Eden.ent", "worlds/MP/CTI_Campaign_Eden.ent"]
    assert layouts.scenario_files(fs, "Arland") == ["worlds/CaptureAndHold/CAH_Arland1.ent"]


def test_fingerprint_and_status(tmp_path):
    fs = FakeFS({"worlds/Eden/Eden.ent": b"a", "worlds/Eden/Eden/Eden.terr": b"bb", "worlds/Arland/Arland.ent": b"c"})
    eden = levels.sources(fs, "Eden")
    assert len(eden) == 1 and eden[0]["path"] == "data.pak"
    assert levels.sources(fs, "Arland")[0]["hash"] != eden[0]["hash"]
    folder = tmp_path / "levels"
    installed = [{"id": "Eden", "sources": eden}]
    assert manifest.status(folder, installed, levels.LEVEL_FORMAT)[0]["state"] == "new"
    (folder).mkdir()
    (folder / "Eden.glb").write_bytes(b"glb")
    manifest.record(folder, levels.GAME, levels.PROG, "0", levels.LEVEL_FORMAT, "Eden", build="1", sources=eden, files=[folder / "Eden.glb"])
    assert manifest.status(folder, installed, levels.LEVEL_FORMAT)[0]["state"] == "current"
    assert manifest.status(folder, installed, levels.LEVEL_FORMAT + 1)[0]["state"] == "outdated"
    fs2 = FakeFS({"worlds/Eden/Eden.ent": b"a", "worlds/Eden/Eden/Eden.terr": b"bbb"})
    assert manifest.status(folder, [{"id": "Eden", "sources": levels.sources(fs2, "Eden")}], levels.LEVEL_FORMAT)[0]["state"] == "changed"
    (folder / "Eden.glb").unlink()
    assert manifest.status(folder, installed, levels.LEVEL_FORMAT)[0]["state"] == "missing"
    assert [r["state"] for r in manifest.status(folder, [], levels.LEVEL_FORMAT)] == ["removed"]
    assert json.loads((folder / "manifest.json").read_text())["levels"]["Eden"]["files"] == ["Eden.glb"]
