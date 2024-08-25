# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 07:58:40 2021

@author: dzhu
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 01:03:54 2021

@author: dzhu
"""
import pandas as pd

from utility import to_datetime

###############################################################################
class FxCashHistDataManager:
    def __init__(self):
        data_loc = 'mktdata/histdata/foreignexchange/fxcash/'

        self.data = dict()
        spot_data = pd.read_csv(data_loc + 'fx_spot.csv')
        spot_data.columns = spot_data.columns.str.lower()        
        spot_data = spot_data.set_index('mkt_inst_id')  
        for mkt_inst_id in set(spot_data.index):            
            tmp = spot_data.loc[mkt_inst_id][['date', 'mid']]            
            tmp = tmp.set_index('date')
            tmp = tmp.sort_index()
            tmp.loc[:, 'change_in_percent'] = tmp['mid'].pct_change()
            tmp.loc[:, 'change'] = tmp['mid'].diff()
            self.data[mkt_inst_id] = tmp
            
        swap_data = pd.read_csv(data_loc + 'fx_swap.csv')
        swap_data.columns = swap_data.columns.str.lower()        
        swap_data = swap_data.set_index('mkt_inst_id')  
        for mkt_inst_id in set(swap_data.index):            
            tmp = swap_data.loc[mkt_inst_id][['date', 'mid']]            
            tmp = tmp.set_index('date')
            tmp = tmp.sort_index()
            tmp.loc[:, 'change_in_percent'] = tmp['mid'].pct_change()
            tmp.loc[:, 'change'] = tmp['mid'].diff()
            self.data[mkt_inst_id] = tmp
      
    @staticmethod
    def create_mkt_inst_id(inst_type, inst_name, inst_term):
        inst_id = inst_type.upper() + '_' +  inst_name.upper()
        if inst_type.lower() == 'fx_spot':
            return inst_id
        else:
            inst_id = inst_id + '_' + inst_term.upper()
            return inst_id
    
    def get_data(self, instruments, start, end, data_type = 'mid'):
        '''
            @args:
                 1. instruments: pandas.DataFrame with columns = {'type', 'name', 'term'}
            @return:
                pandas.DataFrame, index = {'date'}, columns = {data_type}
        '''
        cols = list()
        for inst in instruments:
            if 'type' in inst:
                cols.append('type')
            elif 'name' in inst:
                cols.append('name')
            else:
                cols.append('term')
        instruments.columns = cols
        
        data = pd.DataFrame()
        for i in range(len(instruments)):            
            inst_id = FxCashHistDataManager.create_mkt_inst_id(instruments.iloc[i]['type'], instruments.iloc[i]['name'], instruments.iloc[i]['term'])
            tmp = pd.DataFrame(self.data[inst_id][data_type])
            tmp = tmp.loc[start : end]
            tmp = tmp.rename(columns={'mid': inst_id})            
            data = pd.concat([data,tmp],axis=1)
        return data
    
    def get_hist_data(self, instruments, base_date, num, data_type = 'change'):
        cols = list()
        for inst in instruments:
            if 'type' in inst:
                cols.append('type')
            elif 'name' in inst:
                cols.append('name')
            else:
                cols.append('term')
        instruments.columns = cols
        data = pd.DataFrame()
        for i in range(len(instruments)):  
            inst_id = FxCashHistDataManager.create_mkt_inst_id(instruments.iloc[i]['type'], instruments.iloc[i]['name'], instruments.iloc[i]['term'])
            tmp = pd.DataFrame(self.data[inst_id][data_type])
            base_index = tmp.index.get_loc(base_date)            
            if num < 0:
                tmp = tmp.iloc[base_index + num + 1 : base_index + 1]
            else:
                tmp = tmp.iloc[base_index : base_index + num + 1]
            tmp = tmp.rename(columns={data_type: inst_id})            
            data = pd.concat([data,tmp],axis=1)
        return data
    
    def get_stressed_data(self, instruments, stressed_dates, data_type = 'change'):
        cols = list()
        for inst in instruments:
            if 'type' in inst:
                cols.append('type')
            elif 'name' in inst:
                cols.append('name')
            else:
                cols.append('term')
        instruments.columns = cols
        data = pd.DataFrame()
        for i in range(len(instruments)):  
            inst_id = FxCashHistDataManager.create_mkt_inst_id(instruments.iloc[i]['type'], instruments.iloc[i]['name'], instruments.iloc[i]['term'])
            tmp = pd.DataFrame(self.data[inst_id][data_type])
            tmp = tmp.reindex(stressed_dates)
            tmp = tmp.rename(columns={data_type: inst_id})            
            data = pd.concat([data,tmp],axis=1)
        return data
###############################################################################
if __name__ == "__main__":
    fx_cash_hist_data_manger = FxCashHistDataManager()
    instruments = pd.DataFrame({'inst_type': ['FX_SWAP']*3, 'inst_name': ['USDCNY']*3, 'inst_term': ['SN', '1W', '1M']})   
    print('Hist Data: ', fx_cash_hist_data_manger.get_data(instruments, '2021-07-22', '2021-07-22'))   
    print('Hist Data: ', fx_cash_hist_data_manger.get_hist_data(instruments, '2021-07-22', -10))   
    instruments = pd.DataFrame({'inst_type': ['FX_SPOT'], 'inst_name': ['USDCNY'], 'inst_term': ['']})   
    print('Hist Data: ', fx_cash_hist_data_manger.get_data(instruments, '2021-07-22', '2021-07-22'))   
    print('Hist Data: ', fx_cash_hist_data_manger.get_hist_data(instruments, '2021-07-22', -10))   
    stress_changes = fx_cash_hist_data_manger.get_stressed_data(instruments, ['2021-05-21', '2021-07-22'], data_type = 'change')
    print(stress_changes)