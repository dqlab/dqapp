# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 12:44:25 2021

@author: dzhu
"""
import pandas as pd

from utility import to_datetime
   
###############################################################################
class IrFlowHistDataManager:
    def __init__(self):
        data_loc = 'mktdata/histdata/interestrate/'
        
        mkt_data = pd.read_csv(data_loc + 'ir_flow_data.csv')
        mkt_data.columns = mkt_data.columns.str.lower()        
        mkt_data = mkt_data.set_index('mkt_inst_id')
        
        self.data = dict()
        for mkt_inst_id in set(mkt_data.index):            
            tmp = mkt_data.loc[mkt_inst_id][['date', 'mid']]
            #tmp['date'] = pd.to_datetime(tmp['date'])
            tmp = tmp.set_index('date')
            tmp = tmp.sort_index()
            tmp.loc[:,'change_in_percent'] = tmp['mid'].pct_change()
            tmp.loc[:,'change'] = tmp['mid'].diff()
            self.data[mkt_inst_id] = tmp
        
        #IBOR
        ibor_data = pd.read_csv(data_loc + 'ibor_index.csv')
        ibor_data.columns = ibor_data.columns.str.lower()        
        ibor_data = ibor_data.set_index('ibor_index_id')
        for ibor in set(ibor_data.index):            
            tmp = ibor_data.loc[ibor][['date', 'fixing_rate']]
            #tmp['date'] = pd.to_datetime(tmp['date'])
            tmp = tmp.set_index('date')
            tmp = tmp.sort_index()
            tmp.loc[:,'change_in_percent'] = tmp['fixing_rate'].pct_change()
            tmp.loc[:,'change'] = tmp['fixing_rate'].diff()
            tmp.rename(columns={'fixing_rate': 'mid'}, inplace=True)            
            self.data[ibor] = tmp 
        
    @staticmethod
    def create_mkt_inst_id(inst_type, inst_name, inst_term):
        if inst_type.lower() == 'deposit':
            inst_id = inst_name.upper()
        else:
            inst_id = inst_type.upper() + '_' + inst_name.upper() + '_' + inst_term.upper()
        return inst_id
        
    def get_data(self, instruments, start, end, data_type='mid'):
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
            inst_id = IrFlowHistDataManager.create_mkt_inst_id(instruments.iloc[i]['type'], instruments.iloc[i]['name'], instruments.iloc[i]['term'])
            tmp = pd.DataFrame(self.data[inst_id][data_type])
            tmp = tmp.loc[start : end]
            tmp = tmp.rename(columns={data_type: inst_id})            
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
            inst_id = IrFlowHistDataManager.create_mkt_inst_id(instruments.iloc[i]['type'], instruments.iloc[i]['name'], instruments.iloc[i]['term'])
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
            inst_id = IrFlowHistDataManager.create_mkt_inst_id(instruments.iloc[i]['type'], instruments.iloc[i]['name'], instruments.iloc[i]['term'])
            tmp = pd.DataFrame(self.data[inst_id][data_type])
            print(tmp)
            tmp = tmp.reindex(stressed_dates)
            tmp = tmp.rename(columns={data_type: inst_id})            
            data = pd.concat([data,tmp],axis=1)
        return data
###############################################################################
if __name__ == "__main__":
    ir_flow_hist_data_manger = IrFlowHistDataManager()
    instruments = pd.DataFrame({'inst_type': ['IR_VANILLA_SWAP']*3, 'inst_name': ['CNY_SHIBOR_3M']*3, 'inst_term': ['6M', '1Y', '2Y']})    
    print('Hist Data: ', ir_flow_hist_data_manger.get_data(instruments, '2021-07-22', '2021-07-22'))
    instruments = pd.DataFrame({'inst_type': ['DEPOSIT', 'IR_VANILLA_SWAP'], 'inst_name': ['SHIBOR_3M', 'CNY_SHIBOR_3M'], 'inst_term': ['3M', '1Y']})    
    print('Hist Data: ', list(ir_flow_hist_data_manger.get_data(instruments, '2021-07-22', '2021-07-22').loc['2021-07-22']))
    instruments = pd.DataFrame({'inst_type': ['DEPOSIT', 'IR_VANILLA_SWAP', 'IR_VANILLA_SWAP', 'IR_VANILLA_SWAP'], 'inst_name': ['FR_007', 'CNY_FR_007', 'CNY_FR_007', 'CNY_FR_007'], 'inst_term': ['3M', '1Y','2Y', '3Y']})    
    print('Hist Data: ', ir_flow_hist_data_manger.get_hist_data(instruments, '2021-05-21', -10))
    fr007=ir_flow_hist_data_manger.data['FR_007']
    s1y=ir_flow_hist_data_manger.data['IR_VANILLA_SWAP_CNY_FR_007_1Y']
    instruments = pd.DataFrame({'inst_type': ['IR_VANILLA_SWAP'], 'inst_name': ['CNY_FR_007'], 'inst_term': ['3Y']})
    stressed_dates = ['2021-07-07', '2021-07-08', '2021-07-09', '2021-07-12', '2021-07-13', '2021-07-14', '2021-07-15', '2021-07-16', '2021-07-19', '2021-07-20', '2021-07-21', '2021-07-22']
    print('Hist Data: ', ir_flow_hist_data_manger.get_stressed_data(instruments, stressed_dates))