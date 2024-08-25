# -*- coding: utf-8 -*-
"""
Created on Sat Sep 09 21:35:35 2017

@author: Dingqiu
"""
import sys
import json
from google.protobuf.json_format import MessageToJson

###############################################################################
def save_pb_data(pb_data, name, loc):
    '''
    @args:
        1. pb_data: protobuf message
        2. name: string
        3. loc: string; full path of file destination
    @return:
        
    '''
    try:
        filename = loc + '/' 
        filename += name
        #save as bin file
        f=open(filename+'.bin', 'wb')
        f.write(pb_data.SerializeToString())
        f.close()
        #save as txt file
        with open(filename+'.txt', 'w') as outfile:
            json.dump(MessageToJson(pb_data), outfile)
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
