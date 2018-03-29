"""
Tab class
"""

import os
import re
import itertools as it
import numpy as np
import pandas as pd


class Tab():
    """
    API for the tab files
    """
    def __init__(self, fname):
        self.fname = fname.split(os.sep)[-1]
        self.path = os.sep.join(fname.split(os.sep)[:-1])
        if self.path == '':
            self.abspath = self.fname
        else:
            self.abspath = self.path+os.sep+self.fname
        self.tab_type = self._tab_type()
        self.metadata = {'nfluids': 0, 'fluids': [], 'properties': [],
                         't_points': [], 'p_points': [],
                         't_array': [], 'p_array': []}
        if self.tab_type == 'fixed':
            self._metadata_fixed()
        else:
            self._metadata_keyword()

    def _tab_type(self):
        """
        Private method to define the tab type
        """
        with open(self.abspath) as fobj:
            contents = fobj.readlines()
            for line in contents:
                if 'COMPONENTS' in line:
                    return 'keyword'
            else:
                return 'fixed'

    def _metadata_fixed(self):
        """
        Define the most important tab parametersfor a fixed-type tab file
        """
        # Number of fluids and index of all the phisical properties
        fluids = {}
        props_idx = {}
        with open(self.abspath) as fobj:
            contents = fobj.readlines()
            for idx, line in enumerate(contents):
                if re.findall(r"\'[\w \-\,]*\'", line):
                    if line.split('\'')[-1] not in ('', '\n'):
                        fluid = line.split('\'')[-1].replace("\n", "")
                    else:
                        fluid = 'unknown'
                    fluids[fluid] = [idx, contents[idx+1], contents[idx+2]]
                if idx not in (0, 1) and re.findall(r"[\w\-\/\,]*[()]+", line):
                    prop, unit = line.replace("\n", "").split("(")[0:2]
                    prop = prop[1:-1]
                    props_idx[idx] = (fluid, prop, unit.replace(")", ""))
        self.metadata['nfluids'] = len(fluids)
        # Delete the fluid idx from multiple fluids tab
        for fluid in fluids:
            if self.metadata['nfluids'] != 1:
                fluids[fluid] = [el for idx, el in
                                 enumerate(fluids[fluid]) if idx != 1]
        # Define T and P arrays and all the other patrameters for a fixed tab
        for fluid_idx, fluid in enumerate(fluids):
            p_points, t_points = re.findall(r'[\w+\-\.]+',
                                            fluids[fluid][1])[0:2]
            self.metadata['t_points'].append(int(t_points))
            self.metadata['p_points'].append(int(p_points))
            self.metadata['fluids'].append(fluid)
            # t and p arrays definition
            with open(self.abspath) as fobj:
                contents = fobj.readlines()
                if len(re.findall(r'[\w+\-\.]+', contents[2])) == 2 and\
                   len(re.findall(r'[\w+\-\.]+', contents[3])) == 2:
                    # for tab file like 'Pearl-2-rich-sep2008.tab':
                    # 'WATER-OPTION ENTROPY 'P-2-rich EOS = PR
                    #    42   35    .205826E-01
                    #   .487805E+06    .882353E+01
                    #   .100000E+06   -.500000E+02
                    p_0, t_0 = re.findall(r'[\w+\-\.]+', contents[3])
                    p_step, t_step = re.findall(r'[\w+\-\.]+', contents[2])
                    t_points = self.metadata["t_points"]
                    p_points = self.metadata["p_points"]
                    t_f = float(t_step)*t_points[fluid_idx] + float(t_0)
                    p_f = float(p_step)*p_points[fluid_idx] + float(p_0)
                    self.metadata['t_array'].append(np.arange(float(t_0),
                                                              t_f,
                                                              float(t_step)))
                    self.metadata['p_array'].append(np.arange(float(p_0),
                                                              p_f,
                                                              float(p_step)))
                else:
                    # for tab file like 'Malampaya_export_gas_2011.tab':
                    if self.metadata['nfluids'] != 1:
                        t_p = self._partial_extraction_fixed(fluids[fluid][0],
                                                             3)
                    else:
                        t_p = self._partial_extraction_fixed(fluids[fluid][0],
                                                             2)
                    len_t_array = self.metadata['t_points'][fluid_idx]
                    len_p_array = self.metadata['p_points'][fluid_idx]

        self.metadata['p_array'].append(t_p[:len_p_array])
        self.metadata['t_array'].append(t_p[len_p_array:
                                            len_t_array+len_p_array])
        self.data = pd.DataFrame(props_idx,
                                 index=("Fluid", "Property",
                                        "Unit")).transpose()

    def _partial_extraction_fixed(self, idx, extra_idx=0):
        """
        Private method for a single extraction on a fixed-type tab file
        """
        myarray = np.array([])
        with open(self.abspath) as fobj:
            contents = fobj.readlines()[idx+extra_idx:]
            for line in contents:
                try:
                    vals = re.findall(r' *[\w\-\+\.]*', line)
                    temp = np.array([float(val) for val in vals
                                     if val not in ('', '     ')])
                    myarray = np.hstack((myarray, temp))
                except ValueError:
                    break
        return myarray

    def _export_all_fixed(self):
        """
        Exports all the properties for a fixed-type tab file
        """
        array_ts = []
        array_ps = []
        for array_t, array_p in it.product(self.metadata["t_array"][0],
                                           self.metadata["p_array"][0]):
            array_ts.append(array_t)
            array_ps.append(array_p/1e5)

        array_ts_tot = [array_ts for t in self.data.index]
        array_ps_tot = [array_ps for t in self.data.index]
        values = []
        for idx in self.data.index:
            values.append(self._partial_extraction_fixed(idx+1))
        self.data["Temperature"] = array_ts_tot
        self.data["Pressure"] = array_ps_tot
        self.data["values"] = values

    def _metadata_keyword(self):
        """
        Define the most important tab parameters for a keyword-type tab file
        """
        with open(self.abspath) as fobj:
            for line in fobj:
                if 'PVTTABLE LABEL' in line:
                    label = re.findall(r"\=[\w\ \"]*\,", line)[0][1:-1]
                    self.metadata["fluids"].append(label)

                if 'PRESSURE = (' in line:
                    line = line.split('=')[1]
                    vals = re.findall(r'[\d\-\.eE+]+', line)
                    self.metadata['p_array'] = np.array([float(val) for val in
                                                         vals])
                if 'TEMPERATURE = (' in line:
                    line = line.split('=')[1]
                    vals = re.findall(r'[\d\-\.eE+]+', line)
                    self.metadata['t_array'] = np.array([float(val) for val in
                                                         vals])
                if 'COLUMNS = (' in line:
                    line = line.split('=')[1].replace(" ", "").\
                           replace('(', '').replace(')\n', '')
                    self.metadata['properties'] = line.split(',')
            self.metadata["t_points"] = len(self.metadata["t_array"])
            self.metadata["p_points"] = len(self.metadata["p_array"])
            self.metadata["nfluids"] = len(self.metadata["fluids"])
            self.data = pd.DataFrame(self.metadata["properties"])

    def _export_all_keyword(self):
        """
        Export method for keyword tab files
        """
        data = {}
        for fluid_idx, fluid in enumerate(self.metadata["fluids"]):
            data[fluid] = {}
            with open(self.abspath) as fobj:
                text = fobj.read()
                try:
                    text = text.split("!Phase properties")[1+fluid_idx]
                except IndexError:
                    text = text.split("COLUMNS")[1+fluid_idx]
                try:
                    text = text.split("LABEL")[0]
                except IndexError:
                    pass
                values = re.findall(r"[\.\d\-]+[\.\deE\+\-]+", text)
            nprops = len(self.metadata["properties"])
            for idx, prop in enumerate(self.metadata["properties"]):
                data[fluid][prop] = [float(x) for x in values[idx::nprops]]
        self.data = pd.DataFrame(data)

    def export_all(self):
        """
        It makes all the properties avaiable as data attribute
        """
        if self.tab_type == 'fixed':
            self._export_all_fixed()
        if self.tab_type == 'keyword':
            self._export_all_keyword()
