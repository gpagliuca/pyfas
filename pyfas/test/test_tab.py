import os
from pyfas import Tab

TEST_FLD = os.getcwd() + os.sep + "test_files" + os.sep

def test_type():
    fixed_single = Tab(TEST_FLD+"3P_single-fluid_fixed.tab")
    keyword_single2 = Tab(TEST_FLD+"3P_single-fluid_key2.tab")
    fixed_multiple = Tab(TEST_FLD+"3P_multi-fluid_fixed.tab")
    keyword_single = Tab(TEST_FLD+"3P_single-fluid_key.tab")
    keyword_multiple = Tab(TEST_FLD+"3P_multi-fluid_key.tab")

    assert fixed_single.tab_type == 'fixed'
    assert fixed_multiple.tab_type == 'fixed'
    assert keyword_single.tab_type == 'keyword'
    assert keyword_multiple.tab_type == 'keyword'

def test_fixed_multiple():
    tab = Tab(TEST_FLD+"3P_multi-fluid_fixed.tab")
    assert "GAS ENTROPY" in tab.data.Property[42215]
    assert tab.data.Property[42215] == "GAS ENTROPY"
    tab.export_all()
    assert tab.data.values[61][-1][1] == -.382735E+03

def test_fixed_single():
    tab = Tab(TEST_FLD+"3P_single-fluid_fixed.tab")
    assert "WATER DENSITY" in tab.data.Property[1044]
    assert tab.data.Property[1044] == "WATER DENSITY"
    tab.export_all()
    assert tab.data.values[11][-1][1] == -.138758E+07

def test_keyword_single():
    tab = Tab(TEST_FLD+"3P_single-fluid_key.tab")
    assert tab.metadata["properties"][3] == "ROHL"
    assert tab.metadata["nfluids"] == 1
    tab.export_all()

def test_keyword_multiple():
    tab = Tab(TEST_FLD+"3P_multi-fluid_key.tab")
    assert tab.metadata["nfluids"] == 3
    tab.export_all()
    assert tab.metadata["properties"][3] == "ROHL"

def test_keyword_single2():
    tab = Tab(TEST_FLD+"3P_single-fluid_key2.tab")
    assert tab.metadata["properties"][2] == "ROG"
    assert tab.metadata["nfluids"] == 1
    tab.export_all()
    assert tab.data.values[9][0][2] == 2.01195861
    assert tab.metadata['properties'][-1] == 'SEHL'

