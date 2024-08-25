# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 10:21:07 2021

@author: dzhu
"""
import sys

from dqproto import *
from utility import to_date

###############################################################################
def create_time_series(data,
                       mode,
                       name):
    '''
    @args:
        
    @return:
        dqproto.TimeSeries
    '''
    p_keys = list()
    values = list()    
    for i in range(len(data)):        
        p_keys.append(to_date(data.iloc[i]['date'], '%Y-%m-%d'))
        values.append(data.iloc[i]['value'])
    
    p_rows = len(values)
    p_cols = 1
    p_data = values
    p_storage_order = Matrix.StorageOrder.ColMajor
    p_values = dqCreateProtoMatrix(p_rows, 
                                   p_cols, 
                                   p_data, 
                                   p_storage_order)
    p_mode = TimeSeries.Mode.DESCRIPTOR.values_by_name[mode.upper()].number
    p_name = name.upper()
    ts = dqCreateProtoTimeSeries(p_keys, 
                                 p_values, 
                                 p_mode, 
                                 p_name)
    return ts
        
