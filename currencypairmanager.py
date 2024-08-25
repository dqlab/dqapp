# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 17:10:28 2021

@author: dzhu
"""
import pandas as pd

###############################################################################
class CurrencyPairManager:
    def __init__(self):
        self.data = pd.read_csv('staticdata/foreignexchange/currency_pair.csv')
        self.data.columns = self.data.columns.str.lower()        
        self.data = self.data.set_index('currency_pair')
        
    def get_quote_type(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['quote_type'])
    
    def get_dependency(self, ccy_pair):
        tmp = str(self.data.loc[ccy_pair.upper()]['dependency'])
        tmp = tmp.split(',')
        return tmp
    
    def get_relationship(self, ccy_pair):
        return str(self.data.loc[ccy_pair.upper()]['relationship'])
    
    def get_ccy_pairs(self):
        return list(self.data[(self.data['quote_type']=='PRIMARY')].index)
    
###############################################################################
if __name__ == "__main__":
    ccy_pair_manager =  CurrencyPairManager()
    print('Ccy pairs:', ccy_pair_manager.get_ccy_pairs())
    print('Quote type of USDCNY', ccy_pair_manager.get_quote_type('USDCNY'))
    print('Dependency of CNYUSD', ccy_pair_manager.get_dependency('CNYUSD'))
    print('Relationship of USDCNY', ccy_pair_manager.get_relationship('USDCNY'))