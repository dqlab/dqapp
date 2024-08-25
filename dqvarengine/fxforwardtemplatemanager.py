# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 07:55:14 2021

@author: dzhu
"""
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from staticdata import create_static_data
from utility import save_pb_data, to_period, to_calendar_name_list, to_currency_pair

###############################################################################
def create_fx_forward_template(inst_name,
                               currency_pair,
                               delivery_day_convention,
                               fixing_offset,
                               fixing_day_convention,
                               calendars,
                               save,
                               loc):
    '''
    @args:
       
    @return:
        
    '''   
    p_type = FX_FORWARD        
    p_currency_pair = to_currency_pair(currency_pair)
    p_delivery_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[delivery_day_convention.upper()].number 
    p_calendar = to_calendar_name_list(calendars)
    p_fixing_offset = to_period(fixing_offset)
    p_fixing_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[fixing_day_convention.upper()].number
    
    pb_data = dqCreateProtoFxForwardTemplate(p_type, 
                                             inst_name, 
                                             p_fixing_offset, 
                                             p_currency_pair, 
                                             p_delivery_day_convention,
                                             p_fixing_day_convention,
                                             p_calendar)
    
    pb_data_list = dqCreateProtoFxForwardTemplateList([pb_data])
    create_static_data('SDT_FX_FORWARD', pb_data_list)
    
    if save:
        save_pb_data(pb_data_list, inst_name, loc)

    return pb_data_list

###############################################################################
class FxForwardTemplateManager:
    def __init__(self):
        data_loc = 'staticdata/foreignexchange/instrument/fx_forward/'
        self.data = pd.read_csv(data_loc + 'fx_forward.csv') 
        self.data.columns = self.data.columns.str.lower()
        self.data = self.data.set_index('currency_pair')
        
        for ccy_pair in self.data.index:  
            tmp = self.data.loc[ccy_pair]
            currency_pair = str(ccy_pair)
            delivery_day_convention = str(tmp['delivery_day_convention'])
            fixing_offset = str(tmp['fixing_offset'])
            fixing_day_convention = str(tmp['fixing_day_convention'])
            calendars = tmp['calendars']
            calendar_list = calendars.split(',')
            create_fx_forward_template(currency_pair, currency_pair, delivery_day_convention, fixing_offset, fixing_day_convention, calendar_list,
                                       True, data_loc)
            
    def get_fixing_offset(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['fixing_offset']) 

    def get_fixing_day_convention(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['fixing_day_convention'])  
    
    def get_domestic_discount_curve(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper(),'domestic_discount_curve'])  
    
    def get_foreign_discount_curve(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper(),'foreign_discount_curve']) 
    
###############################################################################
if __name__ == "__main__":
    fx_fwd_template_manager = FxForwardTemplateManager()
    print(fx_fwd_template_manager.data)
    