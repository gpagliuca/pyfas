import os
import numpy as np
import pandas as pd
import quantities as pq
from pyfas import surge_calc
from pyfas import unisim_csv

TEST_FLD = os.getcwd() + os.sep + "test_files" + os.sep

def test_surge():
    data  = pd.read_csv(TEST_FLD+"QLT.csv", skiprows=1)
    data['m3s'] = data['[m3/h]']/3600
    surge = surge_calc(data['[seconds]'].values, data['m3s'].values, 0.045)
    assert surge[-1] == 1635.4351666666685 

def test_unisim_csv():
    df = unisim_csv(TEST_FLD+"unisim_csv_formatting.csv")
    assert len(df.columns) == 17
    assert df.index[2] == 1205
