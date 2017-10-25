import os
import pandas as pd
import pytest
if os.name == 'nt':
    from pyfas import SFC

oscheck = pytest.mark.skipif(os.name == 'posix',
                             reason='this module works only on win')
@oscheck
def test_init():
    sfc = SFC(dll_path="../../../SFC_dlls")

@oscheck
def test_run():
    sfc = SFC(dll_path="../../../SFC_dlls")
    case = sfc.default_input()
    df = sfc.run(**case)
    dp_fr = df["Frictional pressure gradient (> 0 for dp_f/dx < 0) [N/m3]"]
    hol = df["Liquid volume fraction [fraction]"]
    assert dp_fr.values[0] == 9.0885599681982274
    assert hol.values[0] == 0.090909090909090912

