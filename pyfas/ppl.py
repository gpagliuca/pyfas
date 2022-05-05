"""
Ppl class
"""

import os
import re
import pandas as pd
import numpy as np


class Ppl:
    """
    Data extraction for ppl files (OLGA >= 6.0)
    """
    def __init__(self, fname):
        """
        Initialize the ppl attributes
        """
        if fname.endswith(".ppl") is False:
            raise ValueError("not a ppl file")
        self.fname = fname.split(os.sep)[-1]
        self.path = os.sep.join(fname.split(os.sep)[:-1])
        if self.path == '':
            self.abspath = self.fname
        else:
            self.abspath = self.path+os.sep+self.fname
        self._attributes = {}
        self._attributes['branch_idx'] = []
        self.data = {}
        self.label = {}
        self.profiles = {}
        self.geometries = {}
        with open(self.abspath) as fobj:
            for idx, line in enumerate(fobj):
                if 'CATALOG' in line:
                    self._attributes['CATALOG'] = idx
                    nvar_idx = idx+1
                if 'TIME SERIES' in line:
                    self._attributes['data_idx'] = idx
                    break
                if 'CATALOG' in self._attributes:
                    adj_idx = idx-self._attributes['CATALOG']-1
                    if adj_idx > 0:
                        self.profiles[adj_idx] = line
                if 'BRANCH\n' in line:
                    self._attributes['branch_idx'].append(idx+1)
        with open(self.abspath) as fobj:
            self._attributes['nvar'] = int(fobj.readlines()[nvar_idx])
        self._time_series()
        with open(self.abspath) as fobj:
            text = fobj.readlines()
        for branch_idx in self._attributes['branch_idx']:
            branch_raw = text[branch_idx]
            branch = branch_raw.replace("\'", '').replace("\n", '')
            self.extract_geometry(branch, branch_idx+2)

    def _time_series(self):
        with open(self.abspath) as fobj:
            self.time = []
            for line in fobj.readlines()[1+self._attributes['data_idx']::
                                         self._attributes['nvar']+1]:
                self.time.append(float(line))

    def filter_data(self, pattern=''):
        """
        Filter available varaibles
        """
        filtered_profiles = {}
        with open(self.abspath) as fobj:
            for idx, line in enumerate(fobj):
                if 'TIME SERIES' in line:
                    break
                if pattern in line and (idx-self._attributes['CATALOG']-1) > 0:
                    filtered_profiles[idx-self._attributes['CATALOG']-1] = line
        return filtered_profiles

    def _define_branch(self, variable_idx):
        return re.findall(r"'(.+?)'", \
                          self.profiles[variable_idx])[2]

    def extract_geometry(self, branch, branch_begin):
        """
        It adds to self.geometries a specific geometry as (x, y)
        """
        raw_geometry = []
        with open(self.abspath) as fobj:
            for line in fobj.readlines()[branch_begin:]:
                points = []
                for point in line.split(' '):
                    try:
                        points.append(float(point))
                    except ValueError:
                        pass
                raw_geometry.extend(points)
                if ('CATALOG' in line) or ('BRANCH' in line) or ('ANNULUS' in line):
                    break
        xy_geo = raw_geometry
        self.geometries[branch] = (xy_geo[:int(len(xy_geo)/2)],
                                   xy_geo[int(len(xy_geo)/2):])

    def extract(self, variable_idx):
        """
        Extract a specific varaible
        """
        branch = self._define_branch(variable_idx)
        label = self.profiles[variable_idx].replace("\n", "")
        self.label[variable_idx] = label
        self.data[variable_idx] = [[], []]
        with open(self.abspath) as fobj:
            for line in fobj.readlines()[
                    variable_idx+1+self._attributes['data_idx']::
                    self._attributes['nvar']+1]:
                points = []
                for point in line.split(' '):
                    try:
                        points.append(float(point))
                    except ValueError:
                        pass
                self.data[variable_idx][1].append(np.array(points))
        x_st = self.geometries[branch][0]
        x_no_st = [(x0+x1)/2 for x0, x1 in zip(x_st[:-1], x_st[1:])]
        if len(self.data[variable_idx][1][0]) == len(x_st):
            self.data[variable_idx][0] = np.array(x_st)
        else:
            self.data[variable_idx][0] = np.array(x_no_st)

    def to_excel(self, *args):
        """
        Dump all the data to excel, fname and path can be passed as args
        """
        path = os.getcwd()
        fname = self.fname.replace(".ppl", "_ppl") + ".xlsx"
        if len(args) > 0 and args[0] != "":
            path = args[0]
            if os.path.exists(path) == False:
                os.mkdir(path)
        xl_file = pd.ExcelWriter(path + os.sep + fname)
        for idx in self.filter_data(""):
            self.extract(idx)
        labels = list(self.filter_data("").values())
        for prof in self.data:
            data_df = pd.DataFrame()
            data_df["X"] = self.data[prof][0]
            for timestep, data in zip(self.time, self.data[prof][1]):
                data_df[timestep] = data
            myvar = labels[prof-1].split(" ")[0]
            br_label = labels[prof-1].split("\'")[5]
            unit = labels[prof-1].split("\'")[7].replace("/", "-")
            mylabel = "{} - {} - {}".format(myvar, br_label, unit)
            data_df.to_excel(xl_file, sheet_name=mylabel)
        xl_file.save()
