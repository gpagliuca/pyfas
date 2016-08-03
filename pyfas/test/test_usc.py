import os
import pytest
from pyfas import Usc

TEST_FLD = os.getcwd() + os.sep + "test_files" + os.sep

oscheck = pytest.mark.skipif(os.name == 'posix',
                             reason='this module works only on win')
@oscheck
def test_init():
    usc = Usc(TEST_FLD+"test_case.usc")
    assert usc.fname == TEST_FLD+"test_case.usc"
    usc.close()

