import numpy as np
from datetime import timedelta
from datetime import datetime
from win32com.client import Dispatch

def PI_read(server, tag, start=None, end=None, frequency=None):
    """
    Read function for PI server. It has to be executed by python 32 bit.
    """
    pisdk = Dispatch('PISDK.PISDK')
    my_server = pisdk.Servers(server)
    # Not sure if/when the login is necessary
    #con = Dispatch('PISDKDlg.Connections') 
    #con.Login(my_server, '', '', 1, 0)
    time_start = Dispatch('PITimeServer.PITimeFormat')
    time_end = Dispatch('PITimeServer.PITimeFormat')
    sample_point = my_server.PIPoints[tag]
    uom = sample_point.PointAttributes.Item("EngUnits").Value
    description = sample_point.PointAttributes.Item('Descriptor').Value 
    if start != None and end != None:
        # returns a range of values (average)
        time_start.InputString = start.strftime('%m-%d-%Y %H:%M:%S')
        time_end.InputString = end.strftime('%m-%d-%Y %H:%M:%S')
        sample_values = sample_point.Data.Summaries2(time_start, time_end, 
                                                     frequency, 5, 0, None)
        values = sample_values('Average').Value
        data = np.array([x.Value for x in values])
    elif start != None and end == None:
        # returns a single value at the start time
        end = start + timedelta(seconds=1)
        time_start.InputString = start.strftime('%m-%d-%Y %H:%M:%S')
        time_end.InputString = end.strftime('%m-%d-%Y %H:%M:%S')
        sample_values = sample_point.Data.Summaries2(time_start, time_end, 
                                                     frequency, 5, 0, None)
        values = sample_values('Average').Value
        data = [x.Value for x in values][0]
    else:
        # returns the actual value
        data = sample_point.data.Snapshot.Value  
    return description, uom, np.array(data)
