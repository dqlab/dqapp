# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 00:24:21 2021

@author: dzhu
"""
import pandas as pd
import numpy as np

from riskengine import calculate_expected_shortfall, calculate_value_at_risk
###############################################################################
class RiskDataManager:
    def __init__(self):
        self.data = pd.DataFrame()
        self.data_ivar = dict()     
        
    def add(self, trd_id, value_date, value_ccy, value_id, value):
        self.data = self.data.append({'trade_id': trd_id,
                                      'value_date': value_date,
                                      'value_currency': value_ccy,
                                      'value_id': value_id,
                                      'value': value},
                                      ignore_index=True)
    
    def aggregate(self, portfolio_id, trades, as_of_date, ccy, prob):
        for trade in trades:
            df = self.data[self.data['trade_id']!=trade]
            tmp = df[(df['trade_id'].isin(trades)) & (df['value_date']==as_of_date) & (df['value_currency']==ccy.upper())].groupby(['value_id']).sum()
            self.data_ivar[trade] = tmp['value'].tolist()

        tmp = self.data[(self.data['trade_id'].isin(trades)) & (self.data['value_date']==as_of_date) & (self.data['value_currency']==ccy.upper())].groupby(['value_id']).sum()
        tmp = tmp.reset_index()
        tmp.loc[:, 'trade_id'] = [portfolio_id] * len(tmp)
        tmp.loc[:, 'value_date'] = [as_of_date] * len(tmp)
        tmp.loc[:, 'value_currency'] = [ccy.upper()] * len(tmp)
        self.data = self.data.append(tmp)        
        
        portfolios = trades
        portfolios.append(portfolio_id)
        self.__calc_risk_measures(portfolios, as_of_date, ccy, prob)            
    
    def __calc_risk_measures(self, portfolios, as_of_date, ccy, prob):  
        n = len(portfolios)
        for i in range(n):
            trd = portfolios[i]
            tmp = self.data[(self.data['trade_id']==trd.upper()) & (self.data['value_date']==as_of_date) & (self.data['value_currency']==ccy.upper())]['value'].to_numpy()
            #VaR 
            var, mirror_var = calculate_value_at_risk(tmp, prob, True)
            self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                          'value_id': 'VAR', 'value': var}, ignore_index=True)
            self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                          'value_id': 'MIRROR_VAR', 'value': mirror_var}, ignore_index=True)
            #MVaR
            margin_tmp = 0.99*tmp
            mvar,mirror_mvar = calculate_value_at_risk(margin_tmp, prob, True)
            self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                          'value_id': 'MVAR', 'value': mvar-var}, ignore_index=True)
            self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                          'value_id': 'MIRROR_MVAR', 'value': mirror_mvar-mirror_var}, ignore_index=True)
            #IVaR
            if i < n-1: #not calculate for portfolio
                ivar,mirror_ivar = calculate_value_at_risk(self.data_ivar[trd], prob, True)
                self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                            'value_id': 'IVAR', 'value': ivar-var}, ignore_index=True)
                self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                            'value_id': 'MIRROR_IVAR', 'value': mirror_ivar-mirror_var}, ignore_index=True)         
            #ES
            es, mirror_es = calculate_expected_shortfall(tmp, prob, True)
            self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                          'value_id': 'ES', 'value': es}, ignore_index=True)
            self.data = self.data.append({'trade_id': trd, 'value_date': as_of_date, 'value_currency': ccy.upper(),
                                          'value_id': 'MIRROR_ES', 'value': mirror_es}, ignore_index=True)
            
    def save(self, file_name):
        self.data.to_csv('riskdata/' + file_name + '.csv', index=False)
        