import os
import numpy as np
import pandas as pd
import quantities as pq
from pyfas import surge_calc
from pyfas import unisim_csv

TEST_FLD = os.getcwd() + os.sep + "test_files" + os.sep

def test_surge():
    data  = pd.read_csv(TEST_FLD+"QLT.csv", index_col=0, skiprows=1)
    data.columns = ('qlt',)
    t = np.array(data.index) * pq.s
    qlt = np.array(data.qlt) * pq.m**3/pq.h
    drain = 200 * pq.m**3/pq.h
    surge = surge_calc(t, qlt, drain)
    assert surge.units == pq.m**3
    assert surge[-1] == 1005.803 * pq.m**3

def test_unisim_csv():
    df = unisim_csv(TEST_FLD+"unisim_csv_formatting.csv")
    assert len(df.columns) == 17
    assert df.index[2] == 1205
