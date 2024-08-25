# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 18:42:02 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 01:02:37 2021

@author: dzhu
"""

import pandas as pd

from dqlib.x64.dqlibpy import ProcessRequest
from dqproto import *
from utility import to_currency_pair, to_date
from fxspotmktdatamanager import fx_spot_date_calculator, create_fx_spot_rate

###############################################################################
class FxSpotHistStressedScnManager:
    def __init__(self, 
                 as_of_date, 
                 sim_date,                 
                 stressed_dates,
                 change_type,
                 liquidity_horizon,
                 ccy_pair_manager,
                 fx_spot_hist_data_manager):
        
        self.fx_spot_rates = dict()        
        ccy_pairs = ccy_pair_manager.get_ccy_pairs()        
        for ccy_pair in ccy_pairs:
            spot_date = fx_spot_date_calculator(ccy_pair, sim_date)
            instruments = pd.DataFrame()
            instruments['type'] = ['FX_SPOT']
            instruments['name'] = [ccy_pair]
            instruments['term'] = ['']
            
            if change_type.lower() == 'relative':
                data_type = 'change_in_percent'
            else:
                data_type = 'change'                
            hist_data = fx_spot_hist_data_manager.get_stressed_data(instruments, stressed_dates, data_type)
            base_rate = fx_spot_hist_data_manager.get_hist_data(instruments, as_of_date, 0, 'mid').iat[0, 0]
            for i in range(len(stressed_dates)):
                rate = base_rate
                if change_type == 'relative':
                    rate = base_rate * (1.0 + hist_data.iat[i, 0])
                else:
                    rate = base_rate + hist_data.iat[i, 0]
                fx_spot_rate = create_fx_spot_rate(ccy_pair, rate, sim_date, spot_date)
                self.fx_spot_rates[ccy_pair.upper() + '_' + str(i)] = fx_spot_rate
                
    def get_fx_spot_rate(self, ccy_pair, scn_num):
        return self.fx_spot_rates[ccy_pair.upper() + '_' + str(scn_num)]
    
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
    
    sim_date = '2021-07-23'
    stressed_dates = ['2021-07-07', '2021-07-08', '2021-07-09', '2021-07-12', '2021-07-13', '2021-07-14', '2021-07-15', '2021-07-16', '2021-07-19', '2021-07-20', '2021-07-21', '2021-07-22']    
    change_type = 'relative'
    liquidity_horizon = 1
    fx_spot_hist_stressed_scn_manger = FxSpotHistStressedScnManager(as_of_date, sim_date, stressed_dates, change_type, liquidity_horizon,
                                                   ccy_pair_manager, fx_spot_hist_data_manager)        
    print(fx_spot_hist_stressed_scn_manger.fx_spot_rates)
    print('USDCNY spot:', fx_spot_hist_stressed_scn_manger.get_fx_spot_rate('USDCNY', 1))
    
    