from pyfas import Tpl

def test_init():
    tpl = Tpl("FC1_rev01.tpl")
    assert tpl.fname == "FC1_rev01.tpl"


