# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:05:57 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:32:29 2021

@author: dzhu
"""
import pandas as pd

###############################################################################
class FxOptionMktConventionManager:
    def __init__(self):
        data_loc = 'staticdata/foreignexchange/market/'
        
        self.mkt_convention = pd.read_csv(data_loc +'fx_option_mkt_convention.csv')
        self.mkt_convention.columns = self.mkt_convention.columns.str.lower()
        self.mkt_convention = self.mkt_convention.set_index('currency_pair')
                
    def get_mkt_convention(self, ccy_pair):
        return self.mkt_convention.loc[ccy_pair.upper()].to_dict()
    
    def get_ccy_pairs(self):
        return list(set(self.mkt_convention.index))
    
###############################################################################
if __name__ == "__main__":
    fx_option_mkt_convention_manager = FxOptionMktConventionManager()
    print(fx_option_mkt_convention_manager.mkt_convention) 
    print('mkt_convention:', fx_option_mkt_convention_manager.get_mkt_convention('usdcny'))
    print('ccy pairs:', fx_option_mkt_convention_manager.get_ccy_pairs())