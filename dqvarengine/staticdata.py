# -*- coding: utf-8 -*-
"""

"""
import sys
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *

'''#############################Load Src Static Data########################'''
def load_src_static_data(data_type, data_name):
    '''
    @args:
        1. data_type: string
        2. data_name: string
    @return:
        pandas.DataFrame
    '''
    src_data = pd.read_csv('staticdata/' + data_type + '/' + data_name + '.csv')
    src_data.columns = src_data.columns.str.lower()
    return src_data

'''#############################Create Static Data##########################'''
def create_static_data(data_type, pb_data):
    '''
    @args:
        1. data_type: string
        2. pb_data: protobuf message
    @return:
        boolean - True, False
    '''
    try:
        tmp_file = 'dqlib/tmp.bin'
        tmp = open(tmp_file,'wb')
        tmp.write(pb_data.SerializeToString())
        tmp.close()
        
        pb_input = dqCreateProtoCreateStaticDataInput(StaticDataType.DESCRIPTOR.values_by_name[data_type.upper()].number,
                                                      tmp_file)
        
        req_name = 'CREATE_STATIC_DATA'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
        
        pb_output = CreateStaticDataOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.success
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
'''#############################Create Static Data##########################'''
def load_static_data(data_type, data_name, loc):
    '''
    @args:
        1. data_type: string
        2. data_name: string
        3. loc: string; full path of file (*.bin) location
    @return:
        boolean - True, False
    '''
    try:     
        filename = loc + '/' 
        filename += data_name
        filename += '.bin'
        pb_input = dqCreateProtoCreateStaticDataInput(StaticDataType.DESCRIPTOR.values_by_name[data_type.upper()].number,
                                                      filename)
        req_name = 'CREATE_STATIC_DATA'
        res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
        pb_output = CreateStaticDataOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.success
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))        
###############################################################################