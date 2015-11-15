import numpy as np

class Tpl:
    """
    Data extraction for tpl files (OLGA >= 6.0)
    """
    def __init__(self, fname):
        """
        Initialize the tpl attributes
        """
        self.fname = fname
        self._attibutes = {}
        self.y = {}
        self.label = {}
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj):
                if 'CATALOG' in line:
                    self._attibutes['CATALOG'] = idx
                    self._attibutes['nvars'] = idx+1
                if 'TIME SERIES' in line:
                    self._attibutes['data_idx'] = idx
                    break
        self.filter_trends()

    def filter_trends(self, pattern=''):
        """
        Filter available varaibles
        """
        self.trends = {}
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj):
                if 'TIME SERIES' in line:
                    break
                if pattern in line:
                    self.trends[idx-self._attibutes['CATALOG']-1] = line
        return self.trends

    def extract(self, variable_idx):
        """
        Extract a specific varaible
        """
        time, data = np.loadtxt(self.fname,
                                skiprows=self._attibutes['data_idx']+1,
                                unpack=True,
                                usecols=(0, variable_idx))
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj):
                if idx == 1 + variable_idx+self._attibutes['CATALOG']:
                    metadata = line
                    break
        self.time = time
        self.y[variable_idx] = data
        self.label[variable_idx] = line.replace("\'", '')
