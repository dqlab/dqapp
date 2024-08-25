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
def create_fx_spot_template(inst_name,
                            currency_pair,
                            spot_day_convention,
                            calendars,
                            spot_delay,
                            save,
                            loc):
    '''
    @args:
       
    @return:
        
    '''   
    p_type = FX_SPOT        
    p_currency_pair = to_currency_pair(currency_pair)
    p_spot_day_convention = BusinessDayConvention.DESCRIPTOR.values_by_name[spot_day_convention.upper()].number 
    p_calendar = to_calendar_name_list(calendars)
    p_spot_delay = to_period(spot_delay)
    pb_data = dqCreateProtoFxSpotTemplate(p_type, 
                                          inst_name, 
                                          p_currency_pair, 
                                          p_spot_day_convention, 
                                          p_calendar, 
                                          p_spot_delay)
    pb_data_list = dqCreateProtoFxSpotTemplateList([pb_data])
    create_static_data('SDT_FX_SPOT', pb_data_list)
    
    if save:
        save_pb_data(pb_data_list, inst_name, loc)

    return pb_data_list
        
###############################################################################
class FxSpotTemplateManager:
    def __init__(self):
        data_loc = 'staticdata/foreignexchange/instrument/fx_spot/'
        self.data = pd.read_csv(data_loc + 'fx_spot.csv') 
        self.data.columns = self.data.columns.str.lower()
        self.data = self.data.set_index('currency_pair')
        
        for ccy_pair in self.data.index:  
            tmp = self.data.loc[ccy_pair]
            currency_pair = str(ccy_pair)
            spot_day_convention = str(tmp['spot_day_convention'])
            spot_delay = str(tmp['spot_delay'])
            calendars = tmp['calendars']
            calendar_list = calendars.split(',')
            create_fx_spot_template(currency_pair,
                                    currency_pair,
                                    spot_day_convention,
                                    calendar_list,
                                    spot_delay,
                                    True,
                                    data_loc)
            
    def get_spot_delay(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['spot_delay']) 

    def get_spot_day_convention(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['spot_day_convention'])     
    
###############################################################################
if __name__ == "__main__":
    fx_spot_template_manager =  FxSpotTemplateManager()
    print(fx_spot_template_manager.data)
    create_fx_spot_template('USDCNY', 'USDCNY', 'FOLLOWING', ['CAL_CFETS'], '1D', False, '')
    