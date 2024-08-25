# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 01:02:37 2021

@author: dzhu
"""

import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_currency_pair, to_date

###############################################################################
def fx_spot_date_calculator(ccy_pair,
                            as_of_date):
    '''
    
    '''
    p_calculation_date = to_date(as_of_date, '%Y-%m-%d')
    p_currency_pair = to_currency_pair(ccy_pair)
    pb_input = dqCreateProtoFxSpotDateCalculationInput(p_calculation_date, 
                                                       p_currency_pair)
    
    req_name = 'FX_SPOT_DATE_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
    pb_output = FxSpotDateCalculationOutput()
    pb_output.ParseFromString(res_msg)
    spot_date = str(pb_output.spot_date.year) + '-' + str(pb_output.spot_date.month) + '-' + str(pb_output.spot_date.day)
    return spot_date 
    
###############################################################################
def create_fx_spot_rate(ccy_pair, 
                        spot_rate, 
                        as_of_date,
                        spot_date):
    '''
    
    '''
    p_value = spot_rate
    p_ccy_pair = to_currency_pair(ccy_pair)
    p_base_currency = p_ccy_pair.right_currency.name
    p_target_currency = p_ccy_pair.left_currency.name
    p_fx_rate = dqCreateProtoForeignExchangeRate(p_value, 
                                                 p_base_currency, 
                                                 p_target_currency)
    p_ref_date = to_date(as_of_date, '%Y-%m-%d')
    p_spot_date = to_date(spot_date, '%Y-%m-%d')
    pb_spot_rate = dqCreateProtoFxSpotRate(p_fx_rate, 
                                           p_ref_date, 
                                           p_spot_date)
    return pb_spot_rate

###############################################################################
class FxSpotMktDataManager:
    def __init__(self, 
                 as_of_date, 
                 ccy_pair_manager,
                 fx_spot_hist_data_manager):
        
        self.fx_spot_rates = dict()        
        ccy_pairs = ccy_pair_manager.get_ccy_pairs()        
        for ccy_pair in ccy_pairs:
            spot_date = fx_spot_date_calculator(ccy_pair, as_of_date)
            instruments = pd.DataFrame()
            instruments['type'] = ['FX_SPOT']
            instruments['name'] = [ccy_pair]
            instruments['term'] = ['']
            fx_spot_rate = fx_spot_hist_data_manager.get_data(instruments, as_of_date, as_of_date)
            self.fx_spot_rates[ccy_pair.upper()] = create_fx_spot_rate(ccy_pair, fx_spot_rate.iat[0, 0], as_of_date, spot_date)
            
    def get_fx_spot_rate(self, ccy_pair):
        return self.fx_spot_rates[ccy_pair.upper()]
    
###############################################################################
from calendarmanager import CalendarManager
from currencypairmanager import CurrencyPairManager
from fxspottemplatemanager import FxSpotTemplateManager
from fxcashhistdatamanager import FxCashHistDataManager

if __name__ == "__main__":
    as_of_date = '2021-07-22'
    calendar_manager = CalendarManager()
    ccy_pair_manager = CurrencyPairManager()
    fx_spot_template_manager = FxSpotTemplateManager()
    fx_spot_hist_data_manager = FxCashHistDataManager()
    
    fx_spot_mkt_data_manger = FxSpotMktDataManager(as_of_date, ccy_pair_manager, fx_spot_hist_data_manager)        
    print(fx_spot_mkt_data_manger.fx_spot_rates)
    print('USDCNY spot:', fx_spot_mkt_data_manger.get_fx_spot_rate('USDCNY'))
    
    