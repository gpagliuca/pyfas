import os
import pandas as pd
import pytest
if os.name == 'nt':
    from pyfas import Usc

TEST_FLD = os.getcwd() + os.sep + "test_files" + os.sep

oscheck = pytest.mark.skipif(os.name == 'posix',
                             reason='this module works only on win')
@oscheck
def test_init():
    usc = Usc(TEST_FLD+"test_case.usc")
    assert usc.fname == TEST_FLD+"test_case.usc"
    assert usc.path == os.path.abspath('./test_files') + os.sep
    assert usc.stream_names == ['inlet', 'test_stream', 'outlet']
    assert usc.current_time == 19995.50
    assert usc.ops == ['MIX-100', 'SPRDSHT-1']
    usc.close()

@oscheck
def test_extraction_stripchart_no_exposed_data():
    usc = Usc(TEST_FLD+"test_case.usc")
    usc.extract_stripchart('overall', expose_data=False)
    with open('./test_files/trends/overall.csv') as fobj:
        data = fobj.readlines()
        header = data[9].split(",")[:-1]
        UoMs = data[10].split(",")[:-1]
    df = pd.read_csv('./test_files/trends/overall.csv', 
                     skiprows=10, 
                     index_col=0,
                     usecols=(range(0, len(header))),
                     na_values=('Shutdown', 'Bad', 'I/O Timeout', 'Scan Timeout'),
                    )
    df.columns = header[1:]
    df.UoMs = UoMs[1:]
    assert df['outlet - Mass Flow'].values[1] == 31439.8
    assert df.index[-1] == 19980.5
    assert df.UoMs[1] == '[kg/h]'
    os.remove('./test_files/trends/overall.csv')


@oscheck
def test_extraction_stripchart_exposed_data():
    usc = Usc(TEST_FLD+"test_case.usc")
    usc.extract_stripchart('overall', expose_data=True)
    df = usc.stripcharts['overall']
    assert df['outlet - Mass Flow'].values[1] == 31439.8
    assert df.index[-1] == 19980.5
    os.remove('./test_files/trends/overall.csv')
