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
    os.rmdir('./test_files/trends')


@oscheck
def test_extraction_stripchart_exposed_data():
    usc = Usc(TEST_FLD+"test_case.usc")
    usc.extract_stripchart('overall', expose_data=True)
    df = usc.stripcharts['overall']
    assert df['outlet - Mass Flow'].values[1] == 31439.8
    assert df.index[-1] == 19980.5
    os.remove('./test_files/trends/overall.csv')
    os.rmdir('./test_files/trends')
    usc.close()

@oscheck
def test_profile_extraction_no_exposed_data():
    usc = Usc(TEST_FLD+"test_case_pipe.usc")
    usc.extract_profiles('op-100', expose_data=False)
    df = pd.read_csv('./test_files/profiles/op-100-oil_massflow.csv',
                     index_col=0,
                     na_values=('Shutdown', 'Bad', 'I/O Timeout', 'Scan Timeout'),
                    )
    assert df.index[-2] == '1078 m'
    assert round(df['60.00 min'].values[10], 13) == 6.6632257001663
    assert 'op-100-wat_massflow.csv' in os.listdir('./test_files/profiles')
    path_profiles =  './test_files/profiles'
    [os.remove(path_profiles+os.sep+f) for f in os.listdir(path_profiles)] 
    os.rmdir('./test_files/profiles')
    usc.close()

@oscheck
def test_profile_extraction_exposed_data():
    usc = Usc(TEST_FLD+"test_case_pipe.usc")
    usc.extract_profiles('op-100', expose_data=True)
    path_profiles =  './test_files/profiles'
    df =  usc.profiles['op-100']['oil_massflow']
    assert round(df['60.00 min'].values[10], 13) == 6.6632257001663
    assert df.index[-2] == '1078 m'
    [os.remove(path_profiles+os.sep+f) for f in os.listdir(path_profiles)] 
    os.rmdir('./test_files/profiles')
    usc.close()

@oscheck
def test_save():
    usc = Usc(TEST_FLD+"test_case_pipe.usc")
    usc.save()
    usc.save('save_test.usc')
    usc.close()
    os.remove('./test_files/save_test.usc')
