# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 04:06:22 2021

@author: dzhu
"""
import sys
import pandas as pd

###############################################################################
class TrdDataManager:
    def __init__(self):        
        self.trd_data = pd.read_csv('trddata/trade_data.csv')  
        self.trd_data.columns = self.trd_data.columns.str.lower()
        self.trd_data = self.trd_data.set_index('trade_id')
        
    def get_nominal(self, trd_id):
        return float(self.trd_data.loc[trd_id.upper(),'nominal'])
    
    def get_inst_name(self, trd_id):
        return str(self.trd_data.loc[trd_id.upper(),'instrument_name']) 
    
    def get_inst_type(self, trd_id):        
        return str(self.trd_data.loc[trd_id.upper(),'instrument_type']) 
    
    def get_underlying(self, trd_id):
        return str(self.trd_data.loc[trd_id.upper(),'underlying']) 
    
    def get_payoff_ccy(self, trd_id):
        return str(self.trd_data.loc[trd_id.upper(),'payoff_currency'])
    
    def get_maturity(self, trd_id):
        return str(self.trd_data.loc[trd_id.upper(),'maturity'])
    
    def get_trade_date(self, trd_id):
        return str(self.trd_data.loc[trd_id.upper(),'trade_date'])
    
    def get_start_date(self, trd_id):
        return str(self.trd_data.loc[trd_id.upper(),'start_date'])