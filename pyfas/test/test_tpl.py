from pyfas import Tpl

def test_init():
    tpl = Tpl("FC1_rev01.tpl")
    assert tpl.fname == "FC1_rev01.tpl"

def test_attributes():
    tpl = Tpl("FC1_rev01.tpl")
    assert tpl._attibutes['CATALOG'] == 331
    assert tpl._attibutes['data_idx'] == 421
    assert 'VOLGB' in tpl.trends[1]

def test_extraction():
    tpl = Tpl("FC1_rev01.tpl")
    tpl.extract(3)
    assert int(tpl.time[1]) == 60
    assert tpl.y[3][0] == 9.973410e6
    assert 'Pressure' in tpl.label[3]

def test_filter():
    tpl = Tpl("FC1_rev01.tpl")
    PTs = tpl.filter_trends('PT')
    assert 'PT' in PTs[3]
    assert 'POSITION' in PTs[3]
    assert 'TIEIN' in PTs[3]
    tpl.filter_trends()
    assert 'VOLGB' in tpl.trends[1]

