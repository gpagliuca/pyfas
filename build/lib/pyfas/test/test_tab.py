from pyfas import Tab

def test_type():
    fixed_single = Tab("3P_single-fluid_fixed.tab")
    fixed_multiple = Tab("3P_multi-fluid_fixed.tab")
    keyword_single = Tab("3P_single-fluid_key.tab")
    # keyword_multiple = Tab("3P_multi-fluid_key.tab")

    assert fixed_single.tab_type == 'fixed'
    assert fixed_multiple.tab_type == 'fixed'
    assert keyword_single.tab_type == 'keyword'
    # assert keyword_multiple.tab_type == 'keyword'

def test_fixed_multiple():
    tab = Tab("3P_multi-fluid_fixed.tab")
    assert "GAS ENTROPY" in tab.data.Property[42215]
    tab.export_all()
    assert tab.data.values[61][-1][1] == -.382735E+03

def test_fixed_single():
    tab = Tab("3P_single-fluid_fixed.tab")
    assert "WATER DENSITY" in tab.data.Property[1044]
    tab.export_all()
    assert tab.data.values[11][-1][1] == -.138758E+07

def test_keyword_single():
    tab = Tab("3P_single-fluid_key.tab")
    assert tab.tab_data["properties"][3] == "ROHL"
    assert tab.tab_data["nfluids"] == 1
    #tab.export_all()
    #assert 0

def test_keyword_multiple():
    tab = Tab("3P_multi-fluid_key.tab")
    assert tab.tab_data["nfluids"] == 3
    tab.export_all()
    # assert tab.tab_data["properties"][3] == "ROHL"

