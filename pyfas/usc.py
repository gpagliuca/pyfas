"""
Surviaval mini-wrapper on unisim files
"""

import os
import shutil
from string import Template
import pandas as pd
from win32com.client import GetObject

STRIPCHART_EXTRACTION_TEMPLATE = Template("""Message "/" "OpenDocument"
FileNamePrompt Yes "$case"
Message "DataLoggerManager.300/DataLogger.200($stripchart)" "View HistoryView"
Message "DataLoggerManager.300/DataLogger.200($stripchart)" "DumpToCSVFile"
FileNamePrompt Yes "$target"
""")

PROFILE_KEYS = {'gas_hol' : 'HistoricalVapHoldupValues',
                'oil_hol' : 'HistoricalLiq1HoldupValues',
                'wat_hol' : 'HistoricalLiq2HoldupValues',
                'gas_massflow' : 'HistoricalVapFlowValues',
                'oil_massflow' : 'HistoricalLiq1FlowValues',
                'wat_massflow' : 'HistoricalLiq2FlowValues',
                'gas_velocity' : 'HistoricalVapVelocityValues',
                'oil_velocity' : 'HistoricalLiq1VelocityValues',
                'wat_velocity' : 'HistoricalLiq2VelocityValues',
                'flow_pattern' : 'HistoricalFlowPatternValues',
                'pressure' : 'HistoricalTemperatureValues',
                'temperature' : 'HistoricalPressureValues'
                }

PROFILE_LENGTH_NON_ST = 'CellAccumulatedLengthString'
PROFILE_LENGTH_ST = 'CellAccumulatedLength1String'
PROFILE_TIME = 'HistoricalTimesString'

class Usc:
    def __init__(self, fname):
        self.case = GetObject(os.path.abspath(fname))
        self.fname = self.case.FullName
        self.integrator = self.case.solver.Integrator
        self.current_time = self.case.solver.Integrator.currenttimevalue
        self.path = self.case.path
        self.fl = self.case.flowsheet
        self.stream_names = [self.fl.Streams[i]() for i in self.fl.Streams]
        self.streams = self.fl.Streams
        self.ops = [self.fl.Operations[i]() for i in self.fl.Operations]
        self.stripcharts = {}
        self.profiles = {}
        self.pipes = {}
        
    def extract_stripchart(self, stripchart_name='overall', expose_data=True):
        """
        Extract a specific stripchard and exposes the data in the namespace
        """
        csv_fname = self.fname.split(os.sep)[-1].replace(".usc", ".csv")
        scp_fname = self.fname.split(os.sep)[-1].replace(".usc", ".SCP")
        d = {'case' : self.fname.__repr__()[1:-1],
            'stripchart': stripchart_name,
            'target': self.path.__repr__()[1:-1] + csv_fname}
        script = STRIPCHART_EXTRACTION_TEMPLATE.substitute(d)
        with open(self.path + scp_fname, 'w') as fobj:
            fobj.write(script)
        self.case.visible = True
        self.case.application.playscript(self.path + scp_fname)
        self.case.visible = False
        os.remove(self.path + scp_fname)
        if expose_data == True:
            self.stripcharts[stripchart_name] = unisim_csv_formatting(csv_fname, path=self.path)
        if os.path.isdir(self.path+'trends') != True:
            os.mkdir(self.path + 'trends')
        target_dir = self.path + 'trends'
            
        shutil.copy(self.path + csv_fname, 
                    self.path + 'trends\\{}.csv'.format(stripchart_name))
        os.remove(self.path + csv_fname)
    
    def extract_profiles(self, pipeline_name, expose_data=True):
        """
        Extract all the profiles of a specific pipeline and exposes the data in the namespace
        """
        compas_pipe = self.__profile_definition(pipeline_name)
        if os.path.isdir(self.path+'profiles') != True:
            os.mkdir(self.path + 'profiles')
        target_dir = self.path + 'profiles'   
        for key in PROFILE_KEYS:
            self.pipes[pipeline_name]['data'][key] = compas_pipe.GetUserVariable(PROFILE_KEYS[key]).Variable()
            temp = {key: value for (key, value) in enumerate(self.pipes[pipeline_name]['data'][key])}
            try:
                df = pd.DataFrame(temp, index=self.pipes[pipeline_name]['grid'])
            except ValueError:
                df = pd.DataFrame(temp, index=self.pipes[pipeline_name]['non_st_grid'])
            df.columns = self.pipes[pipeline_name]['timesteps']
            df.to_csv('{}/{}-{}.csv'.format(target_dir, pipeline_name, key))
            
    def __profile_definition(self, pipeline_name):
        """
        Prepare the profiles extraction from a specific profile
        """
        pipe = self.fl.Operations[pipeline_name]
        profiles_ts = pipe.GetUserVariable(PROFILE_TIME).Variable()
        x_st = pipe.GetUserVariable(PROFILE_LENGTH_ST).Variable()
        x_non_st = pipe.GetUserVariable(PROFILE_LENGTH_NON_ST).Variable()
        ts = pipe.GetUserVariable(PROFILE_TIME).Variable()
        self.pipes[pipeline_name] = {'grid': x_st, 
                                     'non_st_grid': x_non_st,
                                     'timesteps': ts,
                                     'data': {}
                                    }
        return pipe
         
    def run_until(self, endtime, timeunit='minutes', save=True):
        """
        Run a case untile the specifiend endtime
        """
        integrator = self.case.solver.Integrator
        integrator.rununtil(endtime, timeunit)
        self.case.save()
    
    def save(self):
        """
        Save the current case
        """
        self.case.save()
        
    def close(self):
        """
        Close the current case
        """
        self.case.close()
