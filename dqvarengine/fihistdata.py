# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:49:26 2021

@author: dzhu
"""
import sys
import pandas as pd

from utility import to_datetime

###############################################################################
class BondHistDataManager:
    def __init__(self, bond_yield_curve_sd_manager, bond_sprd_curve_sd_manager):
        self.loc = 'mktdata/histdata/fixedincome/bond/'

        bonds = bond_yield_curve_sd_manager.get_curve_bonds()
        bonds.extend(bond_sprd_curve_sd_manager.get_curve_bonds())
    
        hist_data = pd.read_csv('mktdata/histdata/fixedincome/bond/benchmark_bond.csv')
        hist_data.columns = hist_data.columns.str.lower()        
        hist_data = hist_data.set_index('bond_id')        
        for bond in bonds:
            tmp = hist_data.loc[bond]
            tmp.loc[bond, 'date']=pd.to_datetime(tmp['date'])
            tmp = tmp.set_index('date')
            tmp = tmp.sort_index()
            tmp['change_in_percent'] = tmp['yield'].pct_change()
            tmp['change'] = tmp['yield'].diff()
            tmp.to_csv('mktdata/histdata/fixedincome/bond/'+bond.lower()+'.csv')
    
    def get_hist_data(self, bond_names, start, end, data_type='yield'):
        '''
            @args:
                1. bond_names: list of string
                2. start: string, start date
                3. end: string, end date
                4. data_type: string, {'yield', 'change', 'change_in_percent'}
            @return:
                pandas.DataFrame, index = {'date'}, columns = {data_type}
        '''
        start_date = to_datetime(start, '%Y-%m-%d')
        end_date = to_datetime(end, '%Y-%m-%d')
        data = pd.DataFrame()
        for name in bond_names:
            tmp = pd.read_csv(self.loc + name.lower() + '.csv')
            tmp['date'] = pd.to_datetime(tmp['date'])
            tmp = tmp.set_index('date')
            tmp = tmp.loc[start_date : end_date]
            data = data.append(tmp)
        return data[data_type]
