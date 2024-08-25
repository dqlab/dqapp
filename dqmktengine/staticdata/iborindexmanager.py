# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 17:44:24 2021

@author: dzhu
"""
import sys
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from staticdata import create_static_data
from utility import save_pb_data, to_period, to_calendar_name_list
###############################################################################        
def create_ibor_index(index_type,
                      index_name,
                      index_tenor,
                      index_ccy,
                      start_delay,
                      calendar_list,
                      day_count,
                      interest_day_convention,
                      date_roll_convention,
                      ibor_type,
                      save,
                      loc):
    '''
    @args:
       data: pandas.DataFrame
    @return:
        
    '''   
    try:
        if date_roll_convention == 'nan':
            date_roll_convention = 'invalid_date_roll_convention'            
        pb_data = dqCreateProtoIborIndex(InterestRateIndexType.DESCRIPTOR.values_by_name[index_type.upper()].number, 
                                         IborIndexName.DESCRIPTOR.values_by_name[index_name.upper()].number,  
                                         to_period(index_tenor), 
                                         CurrencyName.DESCRIPTOR.values_by_name[index_ccy.upper()].number, 
                                         to_period(start_delay), 
                                         to_calendar_name_list(calendar_list), 
                                         DayCountConvention.DESCRIPTOR.values_by_name[day_count.upper()].number, 
                                         BusinessDayConvention.DESCRIPTOR.values_by_name[interest_day_convention.upper()].number, 
                                         DateRollConvention.DESCRIPTOR.values_by_name[date_roll_convention.upper()].number, 
                                         IborIndexType.DESCRIPTOR.values_by_name[ibor_type.upper()].number)
        
        pb_data_list = dqCreateProtoIborIndexList([pb_data])
        
        create_static_data('SDT_IBOR_INDEX', pb_data_list)
        
        if save:
            save_pb_data(pb_data_list, index_name, loc)
    
        return pb_data_list
    
    except:#catch all exceptions
        e = sys.exc_info()[0]
        print(str(e))        

###############################################################################
class IborIndexManager:
    def __init__(self):
        data_loc = 'staticdata/interestrate/index/'
        self.data = pd.read_csv(data_loc + 'ibor_index.csv')
        self.data.columns = self.data.columns.str.lower()
        self.data = self.data.set_index('name') 
    
        for index_name in self.data.index:  
            tmp = self.data.loc[index_name]
            index_type = str(tmp['type'])
            index_tenor = str(tmp['tenor'])
            index_ccy = str(tmp['ccy'])
            start_delay = str(tmp['start_delay'])
            calendars = tmp['calendar']
            calendar_list = calendars.split(',')
            day_count = str(tmp['day_count_convention'])
            interest_day_convention = str(tmp['interest_day_convention'])
            date_roll_convention = str(tmp['date_roll_convention'])
            ibor_type = str(tmp['ibor_index_type'])
            create_ibor_index(index_type,
                              index_name,
                              index_tenor,
                              index_ccy,
                              start_delay,
                              calendar_list,
                              day_count,
                              interest_day_convention,
                              date_roll_convention,
                              ibor_type, 
                              False, 
                              data_loc)
            
    def get_tenor(self, name):
        return str(self.data.loc[name.upper()]['tenor'])

    def get_currency(self, name):
        return str(self.data.loc[name.upper()]['ccy'])
    
###############################################################################
if __name__ == "__main__":
    ibor_manager=IborIndexManager()
    print(ibor_manager.data)
