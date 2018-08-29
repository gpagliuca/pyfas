
import numpy as np
import pandas as pd

def surge_calc(time_series, liq_flowrate, drain):
    dt = np.diff(time_series)[-1]
    mean_liq_flow = np.mean(np.vstack([liq_flowrate, 
                                       np.hstack([np.zeros(1), 
                                                  liq_flowrate[:-1]])]),
                                                  axis=0)
    surge = (mean_liq_flow-drain)*dt
    surge[surge < 0] = 0
    return np.cumsum(surge)

def unisim_csv(fname):
    with open(fname, 'r') as fobj:
        data = fobj.readlines()
        headers = data[9].split(",")[1:]
        UoMs = data[10].split(",")[1:]
    df = pd.read_csv(fname,
                     skiprows=10,
                     index_col=0,
                     na_values=('Shutdown', 'Bad',
                                'I/O Timeout', 'Scan Timeout', '<Empty>'))
    df.columns = headers
    return df

