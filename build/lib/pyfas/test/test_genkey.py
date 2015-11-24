import pyfas as fa
import os

def test_init():
    genkey = fa.Genkey("PEN-HP-WPL-002-MaxGas-DP-02.genkey")
    assert genkey.fname == "PEN-HP-WPL-002-MaxGas-DP-02.genkey"
    genkey_tmp = fa.Genkey("PEN-HP-WPL-002-MaxGas-DP-02_template.genkey")
    assert genkey_tmp.variables == ["$source_flow", "$valve_op"]

def test_write():
    genkey_tmp_write = fa.Genkey("PEN-HP-WPL-002-MaxGas-DP-02_template.genkey")
    values = {"source_flow": 10, "valve_op": 0.5}
    genkey_tmp_write.write_genkey(values, "mytest.genkey")
    with open("mytest.genkey") as fobj:
        assert 'OPENING=0.5' in fobj.readlines()[278]
    os.remove("mytest.genkey")
