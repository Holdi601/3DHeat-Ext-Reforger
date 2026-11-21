from heat3d_ext_reforger.gear import _FACTION, _MODEL, _PARENT, REAL


def test_prefab_text_patterns():
    text = (
        'Vehicle : "{543A50BF3A42AD47}Prefabs/Vehicles/Core/Wheeled_Base.et" {\n'
        ' "faction affiliation" "US"\n'
        '  Object "{0123456789ABCDEF}Assets/Vehicles/X/X_base.xob"\n'
        "}"
    )
    assert _PARENT.search(text).group(1) == "Prefabs/Vehicles/Core/Wheeled_Base.et"
    assert _FACTION.search(text).group(1) == "US"
    assert _MODEL.search(text).group(1) == "Assets/Vehicles/X/X_base.xob"
    assert REAL["lav25"][0] == "LAV-25"
