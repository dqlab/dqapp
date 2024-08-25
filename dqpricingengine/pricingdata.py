# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 00:24:21 2021

@author: dzhu
"""
import pandas as pd

###############################################################################
class PricingDataManager:
    def __init__(self, data_file = ''):
        self.data = pd.DataFrame()
        if data_file != '':
            self.data = pd.read_csv('pricingdata/'+data_file+'.csv')
            self.data.columns = self.data.columns.str.lower()
            
    def add(self, trd_id, value_date, value_ccy, value_id, value):
        self.data = self.data.append({'trade_id': trd_id,
                                      'value_date': value_date,
                                      'value_currency': value_ccy,
                                      'value_id': value_id,
                                      'value': value},
                                      ignore_index=True)
    
    def aggregate(self, portfolio_id, trades, as_of_date, ccy):
        tmp = self.data[(self.data['trade_id'].isin(trades)) & (self.data['value_date']==as_of_date) & (self.data['value_currency']==ccy.upper())].groupby(['value_id']).sum()
        tmp = tmp.reset_index()
        tmp.loc[:,'trade_id'] = [portfolio_id] * len(tmp)
        tmp.loc[:,'value_date'] = [as_of_date] * len(tmp)
        tmp.loc[:,'value_currency'] = [ccy.upper()] * len(tmp)
        self.data = self.data.append(tmp)
        
    def save(self, file_name):
        self.data.to_csv('pricingdata/' + file_name + '.csv', index=False)
        
    def get_present_value(self, trd_id, value_date, value_ccy):
        if trd_id.upper() not in set(self.data.trade_id):
            return 0.0
        if value_date not in set(self.data.value_date):
            return 0.0
        if value_ccy.upper() not in set(self.data.value_currency):
            return 0.0        
        
        pv = self.data[(self.data['trade_id']==trd_id.upper()) & (self.data['value_date']==value_date) & (self.data['value_currency']==value_ccy.upper()) & (self.data['value_id']=='PRESENT_VALUE')]['value'].iloc[0]
        
        return pv
    
    def get_pnl_total(self, trd_id, value_date, value_ccy):
        if trd_id.upper() not in set(self.data.trade_id):
            return 0.0
        if value_date not in set(self.data.value_date):
            return 0.0
        if value_ccy.upper() not in set(self.data.value_currency):
            return 0.0        
        
        pnl = self.data[(self.data['trade_id']==trd_id.upper()) & (self.data['value_date']==value_date) & (self.data['value_currency']==value_ccy.upper()) & (self.data['value_id']=='PNL_TOTAL')]['value'].iloc[0]
        
        return pnl
        