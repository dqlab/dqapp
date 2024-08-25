# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:58:08 2021

@author: dzhu
"""
import sys
import pandas as pd

###############################################################################
class PortfolioManager:
    def __init__(self):
        self.data = pd.read_csv('trddata/portfolio/portfolio.csv')
        self.data.columns = self.data.columns.str.lower()
        self.data = self.data.set_index('portfolio_id')
        
    def get_portfolio_id(self, portfolio_name):
        portfolio_id = self.data.index[self.data['portfolio_name']==portfolio_name.upper()][0]
        return portfolio_id
    
    def get_sub_portfolios(self, portfolio_id):                
        sub_portfolios =  list(self.data[(self.data['upper_portfolio']==portfolio_id.upper()) & (self.data['portfolio_type']=='PHYSICAL')].index)
        if len(sub_portfolios) == 0:
            return sub_portfolios
        else:
            for sub_id in sub_portfolios:
                sub_portfolios.extend(self.get_sub_portfolios(sub_id))
            return sub_portfolios
        
    def get_trades(self, portfolio_id):        
        trades = list(self.data[(self.data['upper_portfolio']==portfolio_id.upper()) 
                    &(self.data['portfolio_type'].isin(['TRADE','POSITION']))].index)
        #level = int(self.data.loc[portfolio_id]['level'])
        sub_portfolios =  list(self.data[(self.data['upper_portfolio']==portfolio_id.upper()) 
                            & (self.data['portfolio_type']=='PHYSICAL')].index)
        if len(sub_portfolios) == 0:
            return trades
        else:
            for sub_id in sub_portfolios:
                trades.extend(self.get_trades(sub_id))
            return trades
        
        

