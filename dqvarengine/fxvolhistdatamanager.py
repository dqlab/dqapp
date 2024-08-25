# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 12:37:49 2021

@author: dzhu
"""

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
import numpy as np

from utility import to_datetime

###############################################################################
class FxVolHistDataManager:
    def __init__(self):
        data_loc = 'mktdata/histdata/foreignexchange/fxvolatility/'

        self.data = dict()
        vol_data = pd.read_csv(data_loc + 'fx_volatility.csv')
        vol_data.columns = vol_data.columns.str.lower()
        for i in range(len(vol_data)):    
            inst_type = str(vol_data.iloc[i]['instrument_type'])
            ccy_pair = str(vol_data.iloc[i]['currency_pair'])
            inst_strike = str(vol_data.iloc[i]['strike'])
            inst_term = str(vol_data.iloc[i]['term'])
            mkt_inst_id = FxVolHistDataManager.create_mkt_inst_id(inst_type, ccy_pair, inst_strike, inst_term)
            vol_data.loc[i, 'mkt_inst_id'] = mkt_inst_id
        vol_data = vol_data.set_index('mkt_inst_id')        
        
        for mkt_inst_id in set(vol_data.index):            
            tmp = vol_data.loc[mkt_inst_id][['date', 'mid']]            
            tmp = tmp.set_index('date')
            tmp = tmp.sort_index()
            tmp['change_in_percent'] = tmp['mid'].pct_change()
            tmp['change'] = tmp['mid'].diff()
            self.data[mkt_inst_id] = tmp
      
    @staticmethod
    def create_mkt_inst_id(inst_type, ccy_pair, inst_strike, inst_term):
        inst_id = inst_type.upper() + '_' +  ccy_pair.upper()+ '_' +  inst_strike.upper()+ '_' +  inst_term.upper()
        return inst_id
    
    def get_data(self, instruments, start, end, data_type = 'mid'):
        '''
            @args:
                 1. instruments: pandas.DataFrame with columns = {'type', 'name', 'strike', 'term'}
            @return:
                pandas.DataFrame, index = {'date'}, columns = {data_type}
        '''
        cols = list()
        for inst in instruments:
            if 'type' in inst:
                cols.append('type')
            elif 'name' in inst or 'currency_pair' in inst:
                cols.append('name')
            elif 'strike' in inst:
                cols.append('strike')
            else:
                cols.append('term')
        instruments.columns = cols
        
        data = pd.DataFrame()
        for i in range(len(instruments)):            
            inst_id = FxVolHistDataManager.create_mkt_inst_id(instruments.iloc[i]['type'], instruments.iloc[i]['name'], instruments.iloc[i]['strike'], instruments.iloc[i]['term'])
            tmp = pd.DataFrame(self.data[inst_id][data_type])
            tmp = tmp.loc[start : end]
            tmp = tmp.rename(columns={'mid': inst_id})            
            data = pd.concat([data,tmp],axis=1)
        return data
    
    def get_vol_matrix(self, ccy_pair, terms, atm_inst_type, otm_inst_types, otm_inst_strikes, as_of_date, data_type = 'mid'):
        vol_matrix = list()
        for t in terms:            
            atm_inst_id = FxVolHistDataManager.create_mkt_inst_id(atm_inst_type, ccy_pair, 'atm', t)
            vol = float(self.data[atm_inst_id][data_type][as_of_date : as_of_date])
            vol_matrix.append(vol*1.0e-2)
            for inst_type in otm_inst_types:
                for inst_strike in otm_inst_strikes:
                    otm_inst_id = FxVolHistDataManager.create_mkt_inst_id(inst_type, ccy_pair, inst_strike, t)
                    vol = self.data[otm_inst_id][data_type][as_of_date : as_of_date].tolist()                    
                    vol_matrix.append(vol[0]*1.0e-2)                
        
        vol_matrix = np.array(vol_matrix)
        rows = len(terms)
        cols = 1 + len(otm_inst_types) * len(otm_inst_strikes)
        vol_matrix = vol_matrix.reshape((rows, cols))
        vol_matrix = np.transpose(vol_matrix)        
        vol_names = list()
        vol_names.append('ATM')        
        for inst_strike in otm_inst_strikes:
            vol_name_prefix = inst_strike[len(inst_strike)-1] + inst_strike[:(len(inst_strike)-1)]
            for inst_type in otm_inst_types:
                if inst_type.lower() == 'fx_risk_reversal':                        
                    vol_name = vol_name_prefix.upper() + '_' + 'RR'
                elif inst_type.lower() == 'fx_butterfly':
                    vol_name = vol_name_prefix.upper() + '_' + 'BF'
                else:
                    raise Exception('This instrument type is not supported yet!')
                vol_names.append(vol_name)
                        
        return vol_matrix, vol_names
###############################################################################
if __name__ == "__main__":
    fx_vol_hist_data_manger = FxVolHistDataManager()
    instruments = pd.DataFrame({'inst_type': ['FX_BUTTERFLY', 'FX_BUTTERFLY', 'FX_STRADDLE', 'FX_RISK_REVERSAL', 'FX_RISK_REVERSAL'], 'inst_name': ['USDCNY']*5, 'inst_strike': ['10D', '25D', 'ATM', '10D', '25D'], 'inst_term': ['1D', '1W', '1M', '1W', '1M']})   
    print('Hist Data: ', fx_vol_hist_data_manger.get_data(instruments, '2021-05-28', '2021-05-28'))   
    vol_mat, vol_names = fx_vol_hist_data_manger.get_vol_matrix('USDCNY', 
                                                     ['1D', '1W', '2W'], 
                                                     'FX_STRADDLE', 
                                                     ['FX_BUTTERFLY', 'FX_RISK_REVERSAL'],
                                                     ['25D', '10D'],
                                                     '2021-05-28')
    print('Vol Matrix:', vol_mat)
    print('Vol Names:', vol_names)