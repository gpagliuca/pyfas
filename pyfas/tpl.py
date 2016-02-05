import os
import numpy as np
import pandas as pd


class Tpl:
    """
    Data extraction for tpl files (OLGA >= 6.0)
    """
    def __init__(self, fname):
        """
        Initialize the tpl attributes
        """
        if fname.endswith(".tpl") == False:
            raise ValueError("not a tpl file")
        self.fname = fname
        self._attibutes = {}
        self.data = {}
        self.label = {}
        self.trends = {}
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj):
                if 'CATALOG' in line:
                    self._attibutes['CATALOG'] = idx
                    self._attibutes['nvars'] = idx+1
                if 'TIME SERIES' in line:
                    self._attibutes['data_idx'] = idx
                    break
                if 'CATALOG' in self._attibutes:
                    adj_idx = idx-self._attibutes['CATALOG']-1
                    if adj_idx > 0:
                        self.trends[adj_idx] = line

    def filter_data(self, pattern=''):
        """
        Filter available varaibles
        """
        filtered_trends = {}
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj):
                variable_idx = idx-self._attibutes['CATALOG']-1
                if 'TIME SERIES' in line:
                    break
                if pattern in line and variable_idx > 0:
                    filtered_trends[variable_idx] = line
        return filtered_trends

    def extract(self, variable_idx):
        """
        Extract a specific varaible
        """
        self.time = np.loadtxt(self.fname,
                               skiprows=self._attibutes['data_idx']+1,
                               unpack=True, usecols=(0,))
        data = np.loadtxt(self.fname,
                          skiprows=self._attibutes['data_idx']+1,
                          unpack=True,
                          usecols=(variable_idx,))
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj):
                if idx == 1 + variable_idx+self._attibutes['CATALOG']:
                    metadata = line
                    break
        self.data[variable_idx] = data
        self.label[variable_idx] = line.replace("\'", '').replace("\n", "")

    def to_excel(self, *args):
        """
        Dump all the data to excel, fname and path can be passed as args
        """
        path = os.getcwd()
        fname = self.fname.replace(".tpl", "_tpl") + ".xlsx"
        if len(args) > 0 and args[0] != "":
            path = args[0]
        idxs = self.filter_data("")
        for idx in idxs:
            self.extract(idx)
        df = pd.DataFrame(self.data)
        df.columns = self.label.values()
        df.insert(0, "Time [s]", self.time)
        df.to_excel(path + os.sep + fname)
