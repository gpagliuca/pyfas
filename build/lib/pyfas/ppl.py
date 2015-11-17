import numpy as np


class Ppl:
    """
    Data extraction for ppl files (OLGA >= 6.0)
    """
    def __init__(self, fname):
        """
        Initialize the tpl attributes
        """
        self.fname = fname
        self._attributes = {}
        self._attributes['branch_idx'] = []
        self.data = {}
        self.label = {}
        self.profiles = {}
        self.geometries = {}
        with open(self.fname) as fobj:
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
        with open(self.fname) as fobj:
            self._attributes['nvar'] = int(fobj.readlines()[nvar_idx])
        self._time_series()
        with open(self.fname) as fobj:
            for branch_idx in self._attributes['branch_idx']:
                branch_raw = fobj.readlines()[branch_idx]
                branch = branch_raw.replace("\'", '').replace("\n", '')
                fobj.seek(0)
                self.extract_geometry(branch, branch_idx+2)

    def _time_series(self):
        with open(self.fname) as fobj:
            self.time = []
            for idx, line in enumerate(fobj.readlines()[
                                        1+self._attributes['data_idx']::
                                        self._attributes['nvar']+1]):
                self.time.append(float(line))

    def filter_profiles(self, pattern=''):
        """
        Filter available varaibles
        """
        filtered_profiles = {}
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj):
                if 'TIME SERIES' in line:
                    break
                if pattern in line and (idx-self._attributes['CATALOG']-1) > 0:
                    filtered_profiles[idx-self._attributes['CATALOG']-1] = line
        return filtered_profiles

    def _define_branch(self, variable_idx):
        return self.profiles[variable_idx].split(' ')[3].replace("\'", '')

    def extract_geometry(self, branch, branch_begin):
        """
        It adds to self.geometries a specific geometry as (x, y)
        """
        raw_geometry = []
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj.readlines()[branch_begin:]):
                points = []
                for point in line.split(' '):
                    try:
                        points.append(float(point))
                    except ValueError:
                        pass
                raw_geometry.extend(points)
                if 'CATALOG' in line or 'BRANCH' in line:
                    break
        xy = raw_geometry
        self.geometries[branch] = (xy[:int(len(xy)/2)], xy[int(len(xy)/2):])

    def extract(self, variable_idx):
        """
        Extract a specific varaible
        """
        branch = self._define_branch(variable_idx)
        self.data[variable_idx] = [[], []]
        with open(self.fname) as fobj:
            for idx, line in enumerate(fobj.readlines()[
                                variable_idx+1+self._attributes['data_idx']::
                                self._attributes['nvar']+1]):
                points = []
                for point in line.split(' '):
                    try:
                        points.append(float(point))
                    except ValueError:
                        pass
                self.data[variable_idx][1].append(points)

        X = self.geometries[branch][0]
        X_average = [(x0+x1)/2 for x0, x1 in zip(X[:-1], X[1:])]
        if len(self.data[variable_idx][1][0]) == len(X):
            self.data[variable_idx][0] = X
        else:
            self.data[variable_idx][0] = X_average

