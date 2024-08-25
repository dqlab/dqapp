# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 07:53:11 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 12:29:32 2021

@author: dzhu
"""
import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from staticdata import create_static_data
from utility import save_pb_data, to_period, to_calendar_name_list, to_currency_pair

###############################################################################
def create_fx_swap_template(inst_name,
                            currency_pair,
                            start_day_convention,
                            end_day_convention,
                            fixing_offset,
                            fixing_day_convention,
                            calendars,
                            start_convention,
                            save,
                            loc):
    '''
    @args:
       
    @return:
        
    '''   
    p_type = FX_SWAP   
    p_currency_pair = to_currency_pair(currency_pair)
    p_start_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[start_day_convention.upper()].number 
    p_end_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[end_day_convention.upper()].number 
    p_calendar = to_calendar_name_list(calendars)
    p_fixing_offset = to_period(fixing_offset)
    p_fixing_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[fixing_day_convention.upper()].number
    p_start_convention = InstrumentStartConvention.DESCRIPTOR.values_by_name[start_convention.upper()].number
    
    pb_data = dqCreateProtoFxSwapTemplate(p_type,
                                          inst_name, 
                                          p_start_convention,
                                          p_currency_pair, 
                                          p_calendar, 
                                          p_start_day_convention, 
                                          p_end_day_convention, 
                                          p_fixing_offset, 
                                          p_fixing_day_convention)
    
    pb_data_list = dqCreateProtoFxSwapTemplateList([pb_data])
    create_static_data('SDT_FX_SWAP', pb_data_list)
    
    if save:
        save_pb_data(pb_data_list, inst_name, loc)

    return pb_data_list  
        
###############################################################################
class FxSwapTemplateManager:
    def __init__(self):
        data_loc = 'staticdata/foreignexchange/instrument/fx_swap/'
        self.data = pd.read_csv(data_loc + 'fx_swap.csv') 
        self.data.columns = self.data.columns.str.lower()
        self.data = self.data.set_index('currency_pair')        
         
        for ccy_pair in self.data.index:  
            tmp = self.data.loc[ccy_pair]
            currency_pair = str(ccy_pair)
            start_day_convention = str(tmp['start_day_convention'])
            end_day_convention = str(tmp['end_day_convention'])
            calendars = tmp['calendars']
            calendar_list = calendars.split(',')
            fixing_offset = str(tmp['fixing_offset'])
            fixing_day_convention = str(tmp['fixing_day_convention'])
            start_convention = 'SPOT_START'
            create_fx_swap_template(currency_pair,
                                    currency_pair,
                                    start_day_convention,
                                    end_day_convention,
                                    fixing_offset,
                                    fixing_day_convention,
                                    calendar_list,
                                    start_convention,
                                    True,
                                    data_loc)
            
    def get_fixing_offset(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['fixing_offset']) 

    def get_fixing_day_convention(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['fixing_day_convention']) 

    def get_start_day_convention(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['start_day_convention']) 

    def get_end_day_convention(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['end_day_convention'])     
    
    def get_domestic_discount_curve(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper(),'domestic_discount_curve'])  
    
    def get_foreign_discount_curve(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper(),'foreign_discount_curve']) 
    
###############################################################################
if __name__ == "__main__":
    fx_swap_template_manager =  FxSwapTemplateManager()
    print(fx_swap_template_manager.data)
    #create_fx_swap_template('USDCNY', 'USDCNY', 'FOLLOWING', ['CAL_CFETS'], '1D', False, '')
    