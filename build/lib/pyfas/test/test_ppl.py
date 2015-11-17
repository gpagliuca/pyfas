from pyfas import Ppl

def test_init():
    ppl = Ppl("FC1_rev01.ppl")
    assert ppl.fname == "FC1_rev01.ppl"
    assert ppl._attributes['branch_idx'][0] == 18
    branch = 'tiein_spool'
    assert int(ppl.geometries[branch][0][0]) == 0
    assert int(ppl.geometries[branch][0][-1]) == 265
    assert int(ppl.geometries[branch][1][0]) == -120
    assert int(ppl.geometries[branch][1][11]) == -120

def test_time_series():
    ppl = Ppl("FC1_rev01.ppl")
    assert int(ppl.time[0]) == 0
    assert int(ppl.time[-1]) == 1.8e5

def test_attributes():
    ppl = Ppl("FC1_rev01.ppl")
    assert ppl._attributes['CATALOG'] == 331
    assert ppl._attributes['data_idx'] == 381
    assert 'GG' in ppl.profiles[1]
    assert ppl._attributes['nvar'] == 48

def test_extraction():
    ppl = Ppl("FC1_rev01.ppl")
    ppl.extract(4)
    assert ppl.data[4][1][0][0] == 9.962770e6
    assert ppl.data[4][1][-1][0] == 1.276020e7

def test_filter():
    ppl = Ppl("FC1_rev01.ppl")
    PTs = ppl.filter_profiles('PT')
    assert 'PT' in PTs[4]
    assert 'old_offshore' in PTs[4]
    ppl.profiles
    assert 'GG' in ppl.profiles[1]


