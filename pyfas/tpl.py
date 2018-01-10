"""
Tpl class
"""

import os
import re
import numpy as np
import pandas as pd
from collections import OrderedDict


class Tpl:
    """
    Data extraction for tpl files (OLGA >= 6.0)
    """
    def __init__(self, fname):
        """
        Initialize the tpl attributes
        """
        if fname.endswith(".tpl") is False:
            raise ValueError("not a tpl file")
        self.fname = fname.split(os.sep)[-1]
        self.path = os.sep.join(fname.split(os.sep)[:-1])
        if self.path == '':
            self.abspath = self.fname
        else:
            self.abspath = self.path+os.sep+self.fname
        self._attributes = {}
        self.data = {}
        self.label = {}
        self.trends = {}
        self.time = ""
        with open(self.abspath) as fobj:
            for idx, line in enumerate(fobj):
                if 'CATALOG' in line:
                    self._attributes['CATALOG'] = idx
                    self._attributes['nvars'] = idx+1
                if 'TIME SERIES' in line:
                    self._attributes['data_idx'] = idx
                    break
                if 'CATALOG' in self._attributes:
                    adj_idx = idx-self._attributes['CATALOG']-1
                    if adj_idx > 0:
                        self.trends[adj_idx] = line

    def filter_trends(self, pattern=''):
        """
        Filter available trends
        """
        filtered_trends = {}
        with open(self.abspath) as fobj:
            for idx, line in enumerate(fobj):
                variable_idx = idx-self._attributes['CATALOG']-1
                if 'TIME SERIES' in line:
                    break
                if pattern in line and variable_idx > 0:
                    filtered_trends[variable_idx] = line
        return filtered_trends

    def extract(self, *args):
        """
        Extract a specific variable
        """
        self.time = np.loadtxt(self.abspath,
                               skiprows=self._attributes['data_idx']+1,
                               unpack=True, usecols=(0,))
        for variable_idx in args:
            data = np.loadtxt(self.abspath,
                              skiprows=self._attributes['data_idx']+1,
                              unpack=True,
                              usecols=(variable_idx,))
            with open(self.abspath) as fobj:
                for idx, line in enumerate(fobj):
                    if idx == 1 + variable_idx+self._attributes['CATALOG']:
                        try:
                            self.data[variable_idx] = data[:len(self.time)]
                        except TypeError:
                            self.data[variable_idx] = data.base
                        self.label[variable_idx] = line.replace("\'",
                                                                '').replace("\n",
                                                                            "")
                        break

    def view_trends(self, pattern=''):
        """
        Return a pandas df with the available trends
        """
        d = OrderedDict()
        d['Index'] = None
        d['Variable'] = []
        d['Position'] = []
        d['Unit'] = []
        d['Description'] = []
        raw_d = self.filter_trends(pattern)
        d['Index'] = [k for k in raw_d.keys()]
        for st in self.filter_trends(pattern).values():
            st = st.replace('\n', '')
            d['Variable'].append(st.split(' ')[0])
            temp = [x[1:-1] for x in re.findall("\'[\w\(\) \-\:\/]+\'", st)]
            d['Description'].append(temp[-1])
            d['Unit'].append(temp[-2][1:-1])
            pos = " - ".join(temp[: -2]).replace("BRANCH", "Br").replace(":", "")
            d['Position'].append(pos)
        df=pd.DataFrame(d)
        df.index.name = "Filter: {}".format(pattern)
        return df

    def to_excel(self, *args):
        """
        Dump all the data to excel, fname and path can be passed as args
        """
        path = os.getcwd()
        fname = self.fname.replace(".tpl", "_tpl") + ".xlsx"
        idxs = self.filter_trends("")
        for idx in idxs:
            self.extract(idx)
        data_df = pd.DataFrame(self.data)
        data_df.columns = self.label.values()
        data_df.insert(0, "Time [s]", self.time)
        if len(args) > 0 and args[0] != "":
            path = args[0]
            if os.path.exists(path) == False:
                os.mkdir(path)
            data_df.to_excel(path + os.sep + fname)
        else:
            data_df.to_excel(self.path + os.sep + fname)

